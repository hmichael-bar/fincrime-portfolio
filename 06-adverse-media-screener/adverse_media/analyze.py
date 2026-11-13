"""
Turn raw articles into scored adverse-media findings.

For every article:
  1. Relevance  - is the subject actually named in the headline/snippet?
  2. Categories - which risk categories' keywords appear (English + Arabic)?
  3. Stage      - is it an allegation, a charge, or a conviction/penalty/designation?
  4. Severity   - 0-100 = category weight x stage multiplier x relevance multiplier
                  (+ small bonus for multiple categories, - discount if exculpatory).
Then de-duplicate syndicated copies of the same story and rate the subject overall.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone

from rapidfuzz import fuzz

from .keywords import CATEGORIES, MITIGATING, NEGATORS, STAGES
from .sources import Article

RELEVANCE_MULT = {"title": 1.0, "snippet": 0.85, "partial": 0.6, "none": 0.35}

_AR_DIACRITICS = re.compile(r"[ً-ٰٟـ]")


def norm_ar(s: str) -> str:
    """Normalise Arabic spelling so keywords match regardless of hamza/ta marbuta/diacritics."""
    s = _AR_DIACRITICS.sub("", s or "")
    return (s.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ى", "ي")
             .replace("ة", "ه").replace("ؤ", "و").replace("ئ", "ي"))


def norm_latin(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", (s or "").lower())).strip()


# Pre-compile keyword patterns
_EN = {c: [re.compile(r"\b" + p, re.I) for p in d["en"]] for c, d in CATEGORIES.items()}
_AR = {c: [norm_ar(p) for p in d["ar"]] for c, d in CATEGORIES.items()}
_STAGE_EN = {s: [re.compile(r"\b" + p, re.I) for p in d["en"]] for s, d in STAGES.items()}
_STAGE_AR = {s: [norm_ar(p) for p in d["ar"]] for s, d in STAGES.items()}
_MIT_EN = [re.compile(r"\b" + p, re.I) for p in MITIGATING["en"]]
_MIT_AR = [norm_ar(p) for p in MITIGATING["ar"]]
_NEG_EN = [re.compile(p, re.I) for p in NEGATORS["en"]]
_NEG_AR = [norm_ar(p) for p in NEGATORS["ar"]]
STAGE_NONE_MULT = 0.75

GENERIC = {"bank", "company", "co", "ltd", "llc", "inc", "group", "the", "of", "and", "al", "el",
           "bin", "ibn", "corp", "holding", "holdings", "international", "sa", "plc"}


@dataclass
class Subject:
    name: str
    aliases: list[str] = field(default_factory=list)
    arabic_names: list[str] = field(default_factory=list)
    kind: str = "person"          # person | entity

    @property
    def all_names(self) -> list[str]:
        return [self.name] + self.aliases + self.arabic_names


@dataclass
class Finding:
    article: Article
    relevance: str
    categories: dict[str, list[str]]       # category -> matched terms
    stage: str
    mitigating: list[str]
    severity: float
    also_reported_by: list[str] = field(default_factory=list)

    @property
    def is_adverse(self) -> bool:
        return bool(self.categories) and self.relevance != "none" and self.severity >= 40

    def to_dict(self) -> dict:
        d = self.article.to_dict()
        d.update({"relevance": self.relevance, "stage": self.stage, "severity": round(self.severity),
                  "categories": {CATEGORIES[c]["label"]: terms for c, terms in self.categories.items()},
                  "mitigating_terms": self.mitigating, "also_reported_by": self.also_reported_by})
        return d


# --------------------------------------------------------------------------
def relevance(subject: Subject, text_title: str, text_snip: str) -> str:
    t_lat, s_lat = norm_latin(text_title), norm_latin(text_snip)
    t_ar, s_ar = norm_ar(text_title), norm_ar(text_snip)
    for name in subject.all_names:
        if re.search(r"[؀-ۿ]", name):
            n = norm_ar(name)
            if n in t_ar:
                return "title"
            if n in s_ar:
                return "snippet"
        else:
            n = norm_latin(name)
            if not n:
                continue
            # fuzzy containment tolerates Makhlouf/Makhluf, possessives, etc.
            if n in t_lat or (len(n) > 6 and fuzz.partial_ratio(n, t_lat) >= 92):
                return "title"
            if n in s_lat or (len(n) > 6 and fuzz.partial_ratio(n, s_lat) >= 92):
                return "snippet"
    # partial: the distinctive word of the name (usually the surname) appears
    for name in subject.all_names:
        if re.search(r"[؀-ۿ]", name):
            toks = [norm_ar(t) for t in name.split() if len(t) > 3]
            hay = t_ar + " " + s_ar
        else:
            toks = [t for t in norm_latin(name).split() if t not in GENERIC and len(t) > 3]
            hay = t_lat + " " + s_lat
        if toks and toks[-1] in hay.split():
            return "partial"
    return "none"


def classify(text: str) -> tuple[dict, str, list]:
    cats: dict[str, list[str]] = {}
    ar = norm_ar(text)
    for c in CATEGORIES:
        hits = [m.group(0) for p in _EN[c] for m in [p.search(text)] if m]
        hits += [k for k in _AR[c] if k in ar]
        if hits:
            cats[c] = sorted(set(h.lower() for h in hits))
    stage = "none"
    for s in STAGES:  # ordered most -> least serious
        if any(p.search(text) for p in _STAGE_EN[s]) or any(k in ar for k in _STAGE_AR[s]):
            stage = s
            break
    mit = [m.group(0) for p in _MIT_EN for m in [p.search(text)] if m] + [k for k in _MIT_AR if k in ar]
    if mit and (any(p.search(text) for p in _NEG_EN) or any(k in ar for k in _NEG_AR)):
        mit = []   # "refuses to lift sanctions", "رفض رفع العقوبات" -> still adverse
    return cats, stage, mit


def score_article(subject: Subject, a: Article) -> Finding:
    text = f"{a.title}. {a.snippet}"
    cats, stage, mit = classify(text)
    rel = relevance(subject, a.title, a.snippet)
    if not cats:
        return Finding(a, rel, {}, stage, mit, 0.0)
    base = max(CATEGORIES[c]["weight"] for c in cats)
    mult = STAGES[stage]["multiplier"] if stage in STAGES else STAGE_NONE_MULT
    sev = base * mult * RELEVANCE_MULT[rel] + min(10, 5 * (len(cats) - 1))
    if mit:
        sev *= 0.7
    return Finding(a, rel, cats, stage, mit, min(100.0, sev))


# --------------------------------------------------------------------------
def _title_key(t: str) -> str:
    return norm_ar(norm_latin(t))


def deduplicate(findings: list[Finding]) -> list[Finding]:
    """Merge the same story reported by several outlets / found by several queries."""
    findings = sorted(findings, key=lambda f: (-f.severity, f.article.published or datetime.min.replace(tzinfo=timezone.utc)))
    kept: list[Finding] = []
    seen_urls: dict[str, Finding] = {}
    for f in findings:
        url = f.article.url.split("?")[0].rstrip("/")
        if url in seen_urls:
            dup = seen_urls[url]
            dup.article.found_via = sorted(set(dup.article.found_via + f.article.found_via))
            continue
        key = _title_key(f.article.title)
        match = None
        for k in kept:
            kk = _title_key(k.article.title)
            if key == kk or (len(key.split()) >= 5 and fuzz.token_set_ratio(key, kk) >= 90):
                match = k
                break
        if match:
            src = f.article.source or f.article.url.split("/")[2]
            if src and src != match.article.source and src not in match.also_reported_by:
                match.also_reported_by.append(src)
            match.article.found_via = sorted(set(match.article.found_via + f.article.found_via))
            continue
        kept.append(f)
        seen_urls[url] = f
    return kept


def overall_rating(findings: list[Finding]) -> tuple[str, str]:
    adverse = [f for f in findings if f.is_adverse]
    strong = [f for f in adverse if f.severity >= 60]
    if any(f.severity >= 80 for f in adverse) or len(strong) >= 3:
        return "HIGH", "Credible, serious adverse media naming the subject (conviction/penalty/designation-level or repeated)."
    if any(f.severity >= 55 for f in adverse):
        return "MEDIUM", "Adverse allegations naming the subject; analyst review and source verification required."
    if adverse:
        return "LOW", "Weak or indirect adverse references; review to rule out namesakes."
    return "NONE", "No adverse media found in the searched sources and time window."
