"""
Generic name normalisation applied to BOTH the customer name and every list name.

The golden rule of screening: whatever you do to one side, do to the other.
If the list says "QADHAFI, Muammar" and the customer says "Muammar Qaddafi",
both must be reduced to the same shape before any fuzzy comparison happens.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

from . import arabic

# Legal-form words that carry no identifying value for entity names.
LEGAL_FORMS = {
    "llc", "ltd", "limited", "co", "company", "corp", "corporation", "inc", "incorporated",
    "sa", "sarl", "sas", "srl", "spa", "gmbh", "ag", "plc", "lp", "llp", "bv", "nv", "oy",
    "ab", "as", "jsc", "ojsc", "cjsc", "pjsc", "ooo", "zao", "oao", "pao", "fze", "fzco",
    "fzc", "fzllc", "dmcc", "wll", "est", "establishment", "sdn", "bhd", "pte", "pvt",
    "pty", "kft", "doo", "sal", "saog", "saoc", "tic", "san", "ve", "as",
}
# Generic business words: common to thousands of company names, so they say little
# about identity. Dropped from entity scoring (kept if nothing else would remain).
ENTITY_GENERIC = {
    "trading", "trade", "general", "group", "holding", "holdings", "international", "intl",
    "services", "service", "solutions", "industries", "industrial", "enterprises", "enterprise",
    "investment", "investments", "commercial", "import", "export", "imports", "exports",
    "sole", "proprietorship", "partnership", "global", "company", "contracting", "logistics",
}
STOPWORDS = {"the", "and", "of", "for", "de", "del", "la", "le", "du", "des", "von", "van", "&"}


@dataclass
class NormalizedName:
    original: str
    tokens: list[str]                 # scoring tokens (canonical)
    text: str                         # tokens joined by space
    sorted_text: str                  # tokens sorted alphabetically
    skeletons: list[str]              # phonetic key per token
    notes: list[str] = field(default_factory=list)
    arabic_script: bool = False


def strip_accents(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    return "".join(ch for ch in s if not unicodedata.combining(ch))


def reorder_last_first(name: str) -> str:
    """OFAC lists individuals as 'LAST, First Middle'. Convert to 'First Middle LAST'."""
    if name.count(",") == 1:
        last, first = [p.strip() for p in name.split(",")]
        if first and last:
            return f"{first} {last}"
    return name


def basic_tokens(name: str) -> list[str]:
    s = strip_accents(name).lower()
    # dotted acronyms: "l.l.c." -> "llc", "s.a." -> "sa"
    s = re.sub(r"\b((?:[a-z]\.){2,})", lambda m: m.group(1).replace(".", ""), s)
    s = s.replace("’", "").replace("'", "").replace("`", "").replace("ʿ", "").replace("ʾ", "")
    s = re.sub(r"[\-_/.,;:()\[\]\"]", " ", s)
    s = re.sub(r"[^a-z0-9& ]", " ", s)
    return [t for t in s.split() if t]


def normalize_name(name: str, is_entity: bool = False, reorder: bool = True,
                   arabic_rules: bool = True) -> NormalizedName:
    """arabic_rules=False gives a plain baseline (used to measure what the Arabic module adds)."""
    original = name or ""
    notes: list[str] = []
    script = arabic.has_arabic_script(original)
    work = original
    if script and arabic_rules:
        work = arabic.transliterate_arabic(original)
        notes.append(f"Arabic script transliterated to '{work}'")
    if reorder and not is_entity:
        work = reorder_last_first(work)

    toks = basic_tokens(work)
    if not arabic_rules:
        noise = (LEGAL_FORMS | STOPWORDS | ENTITY_GENERIC) if is_entity else STOPWORDS
        toks = [t for t in toks if t not in noise] or toks
        return NormalizedName(original, toks, " ".join(toks), " ".join(sorted(toks)),
                              [t for t in toks], notes, script)
    if is_entity:
        noise = LEGAL_FORMS | STOPWORDS | ENTITY_GENERIC
        dropped = [t for t in toks if t in noise]
        toks = [t for t in toks if t not in noise] or toks
        if dropped:
            notes.append("Ignored legal-form / generic words: " + ", ".join(dropped))
        # entity names still benefit from Arabic canonicalisation (e.g. "Al Qadhafi Foundation")
        ar = arabic.normalize_arabic_tokens(toks)
        toks = ar.tokens or toks
        notes.extend(n for n in ar.notes if not n.startswith("Removed title"))
    else:
        toks = [t for t in toks if t not in STOPWORDS] or toks
        ar = arabic.normalize_arabic_tokens(toks)
        toks = ar.tokens or toks
        notes.extend(ar.notes)

    return NormalizedName(
        original=original,
        tokens=toks,
        text=" ".join(toks),
        sorted_text=" ".join(sorted(toks)),
        skeletons=[arabic.skeleton(t) for t in toks],
        notes=notes,
        arabic_script=script,
    )
