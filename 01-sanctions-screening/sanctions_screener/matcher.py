"""
The screening engine: compares one customer against every SDN / non-SDN name
and alias, scores each candidate 0-100, explains the score and suggests a
disposition.

Score = weighted blend of four signals (all 0-100):

  token_sort   30%  rapidfuzz token_sort_ratio - edit similarity after sorting words,
                    so "QADHAFI Muammar" == "Muammar Qadhafi"
  jaro_winkler 20%  Jaro-Winkler on the sorted string - tolerant of typos, rewards
                    matching prefixes (good for short names)
  token_align  35%  word-by-word alignment: each customer word is paired with its
                    best list word (exact, fuzzy, or same phonetic skeleton)
  phonetic     15%  token_sort_ratio on consonant skeletons (mhmd kdf) - catches
                    transliteration variants not in the variant table

If every word of the shorter name is found in the longer name (e.g. the list
carries extra middle names), a "subset" score is also computed and the higher
of the two is used. An exact match after normalisation scores 100.
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime

from rapidfuzz import fuzz, process
from rapidfuzz.distance import JaroWinkler

from .loader import IndexedName, ListEntry, load_lists
from .normalize import NormalizedName, normalize_name

DEFAULT_THRESHOLD = 85
TRUE_MATCH_SCORE = 90
WEIGHTS = {"token_sort": 0.30, "jaro_winkler": 0.20, "token_align": 0.35, "phonetic": 0.15}

TRUE_MATCH = "True Match"
POTENTIAL = "Potential Match - escalate"
FALSE_POSITIVE = "False Positive"
NO_MATCH = "No Match"


# --------------------------------------------------------------------------
@dataclass
class Hit:
    score: float
    entry: ListEntry
    matched_name: str
    name_type: str
    components: dict
    reasons: list[str] = field(default_factory=list)
    secondary: list[str] = field(default_factory=list)
    disposition: str = ""
    disposition_reason: str = ""

    def to_dict(self) -> dict:
        e = self.entry
        return {
            "score": round(self.score, 1),
            "disposition": self.disposition,
            "disposition_reason": self.disposition_reason,
            "list": "SDN" if e.source == "SDN" else "Consolidated (non-SDN)",
            "uid": e.uid,
            "matched_name": self.matched_name,
            "matched_on": "primary name" if self.name_type == "primary" else f"alias ({self.name_type})",
            "primary_name": e.name,
            "type": e.sdn_type,
            "programs": e.programs,
            "dob": e.dobs,
            "pob": e.pobs,
            "nationality": e.nationalities,
            "address_countries": e.countries,
            "title": e.title,
            "reasons": self.reasons,
            "secondary_checks": self.secondary,
            "score_components": {k: round(v, 1) for k, v in self.components.items()},
        }


@dataclass
class ScreenResult:
    query: str
    normalized: NormalizedName
    hits: list[Hit]
    threshold: float
    ownership_note: str = ""

    @property
    def top(self) -> Hit | None:
        return self.hits[0] if self.hits else None

    @property
    def disposition(self) -> str:
        if self.ownership_note and "50% Rule" in self.ownership_note:
            return POTENTIAL if not self.hits or self.hits[0].disposition != TRUE_MATCH else TRUE_MATCH
        if not self.hits:
            return NO_MATCH
        order = [TRUE_MATCH, POTENTIAL, FALSE_POSITIVE]
        return min((h.disposition for h in self.hits), key=order.index)


# --------------------------------------------------------------------------
def _token_sim(a: str, b: str, ska: str, skb: str, initials: bool = True) -> tuple[float, str]:
    """Similarity of two single tokens + how they matched."""
    if a == b:
        return 100.0, "exact"
    if len(a) == 1 or len(b) == 1:          # middle initial: "V." vs "Vladimirovich"
        if not initials:
            return 0.0, "none"
        return (85.0, "initial") if a[0] == b[0] else (0.0, "none")
    r = fuzz.ratio(a, b)
    # Same consonant skeleton (laden/ladin, qasem/kassem). Require some spelling
    # overlap too, otherwise unrelated names collide (bashar/bushra -> bsr).
    if ska and ska == skb and len(ska) >= 2 and r >= 65 and abs(len(a) - len(b)) <= 2:
        return max(r, 88.0), "phonetic"
    jw = JaroWinkler.normalized_similarity(a, b) * 100
    best = max(r, jw - 5)  # JW is generous on short strings; discount slightly
    return best, "fuzzy"


def _align(q: NormalizedName, n: NormalizedName, initials: bool = True):
    """Greedy word-to-word alignment. Returns (pairs, unmatched_long, short_is_query)."""
    q_items = list(zip(q.tokens, q.skeletons))
    n_items = list(zip(n.tokens, n.skeletons))
    short_is_query = len(q_items) <= len(n_items)
    short, long_ = (q_items, n_items) if short_is_query else (n_items, q_items)
    used = set()
    pairs = []
    for tok, sk in short:
        best = (0.0, None, "none")
        for j, (ltok, lsk) in enumerate(long_):
            if j in used:
                continue
            s, how = _token_sim(tok, ltok, sk, lsk, initials)
            if s > best[0]:
                best = (s, j, how)
        if best[1] is not None and best[0] >= 75:
            used.add(best[1])
            pairs.append((tok, long_[best[1]][0], best[0], best[2]))
        else:
            pairs.append((tok, None, 0.0, "none"))
    unmatched_long = [t for j, (t, _) in enumerate(long_) if j not in used]
    return pairs, unmatched_long, short_is_query, len(short), len(long_)


def score_names(q: NormalizedName, n: NormalizedName, initials: bool = True) -> tuple[float, dict, list]:
    """initials=True lets a single letter match a name starting with it (individuals only)."""
    if not q.tokens or not n.tokens:
        return 0.0, {}, []
    pairs, unmatched_long, short_is_query, n_short, n_long = _align(q, n, initials)
    if q.sorted_text == n.sorted_text:
        comps = {"token_sort": 100, "jaro_winkler": 100, "token_align": 100, "phonetic": 100}
        return 100.0, comps, pairs

    ts = fuzz.token_sort_ratio(q.sorted_text, n.sorted_text)
    jw = JaroWinkler.normalized_similarity(q.sorted_text, n.sorted_text) * 100
    cov_short = sum(p[2] for p in pairs) / n_short
    matched = sum(1 for p in pairs if p[1] is not None)
    frac_long = matched / n_long
    align = cov_short * (0.7 + 0.3 * frac_long)
    phon = fuzz.token_sort_ratio(" ".join(sorted(q.skeletons)), " ".join(sorted(n.skeletons)))
    weighted = (WEIGHTS["token_sort"] * ts + WEIGHTS["jaro_winkler"] * jw +
                WEIGHTS["token_align"] * align + WEIGHTS["phonetic"] * phon)
    comps = {"token_sort": ts, "jaro_winkler": jw, "token_align": align, "phonetic": phon}

    score = weighted
    # Subset rule: every word of the shorter (>=2-word) name found in the longer one.
    full_words = sum(1 for p in pairs if p[3] != "initial")
    if n_short >= 2 and full_words >= 2 and all(p[2] >= 85 for p in pairs):
        subset = cov_short * (0.85 + 0.15 * frac_long)
        comps["subset"] = subset
        score = max(score, subset)
    # A one-word name can never be more than a weak match against a multi-word name.
    if min(len(q.tokens), len(n.tokens)) == 1 and max(len(q.tokens), len(n.tokens)) > 1:
        score = min(score, 80.0)
    return min(score, 99.0), comps, pairs


# --------------------------------------------------------------------------
_MONTHS = "%d %b %Y"


def _parse_customer_dob(dob: str):
    dob = (dob or "").strip()
    if not dob:
        return None, None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d %b %Y", "%d %B %Y"):
        try:
            d = datetime.strptime(dob, fmt)
            return d.date(), d.year
        except ValueError:
            pass
    m = re.search(r"(1[89]\d\d|20\d\d)", dob)
    return None, (int(m.group(1)) if m else None)


def _list_dates(entry: ListEntry):
    out = []
    for d in entry.dobs:
        d = d.replace("alt.", "").replace("circa", "").strip()
        try:
            out.append(datetime.strptime(d, _MONTHS).date())
        except ValueError:
            pass
    return out


def _country_set(entry: ListEntry) -> set[str]:
    s = {c.lower() for c in entry.nationalities + entry.countries}
    for p in entry.pobs:
        s.add(p.split(",")[-1].strip().lower())
    return {c for c in s if c}


def secondary_checks(entry: ListEntry, cust_type: str, dob: str, nationality: str):
    """Compare secondary identifiers. Returns (support, conflict, notes)."""
    support, conflict, notes = [], [], []
    is_ind_list = entry.sdn_type == "individual"

    if cust_type == "individual" and not is_ind_list:
        conflict.append("type")
        art = "an" if entry.sdn_type[:1] in "aeiou" else "a"
        notes.append(f"Type mismatch: customer is an individual, list entry is {art} {entry.sdn_type}")
    elif cust_type == "entity" and is_ind_list:
        notes.append("Customer is an entity but the list entry is an individual: name overlap may "
                     "indicate ownership/control - check beneficial owners (50% Rule)")

    c_date, c_year = _parse_customer_dob(dob)
    years = entry.dob_years
    if c_year and years and is_ind_list:
        list_dates = _list_dates(entry)
        same_year_full = [d for d in list_dates if d.year == c_year]
        year_only_listed = any(re.fullmatch(r"(alt\. )?(circa )?\d{4}", d.strip()) or
                               re.search(r"\bto\b", d) for d in entry.dobs)
        if c_date and c_date in list_dates:
            support.append("dob")
            notes.append(f"DOB exact match ({c_date.isoformat()})")
        elif c_year in years and c_date and same_year_full and not year_only_listed:
            conflict.append("dob")
            notes.append(f"Full DOB differs: customer {c_date.isoformat()} vs list "
                         f"{'; '.join(entry.dobs)} (same year only)")
        elif c_year in years:
            support.append("dob_year")
            notes.append(f"DOB year match only ({c_year}; list: {'; '.join(entry.dobs)}) - "
                         "obtain full DOB / ID document")
        elif any(abs(c_year - y) <= 1 for y in years):
            notes.append(f"DOB within 1 year ({c_year} vs list {'; '.join(entry.dobs)}) - inconclusive")
        else:
            conflict.append("dob")
            notes.append(f"DOB conflict: customer {c_year} vs list {'; '.join(entry.dobs)}")
    elif c_year and is_ind_list and not years:
        notes.append("List entry has no DOB - cannot use DOB to clear or confirm")
    elif not c_year and is_ind_list and years:
        notes.append(f"Customer DOB missing - request it (list DOB: {'; '.join(entry.dobs)})")

    countries = _country_set(entry)
    if nationality and countries:
        nat = nationality.strip().lower()
        if any(nat in c or c in nat for c in countries):
            support.append("nationality")
            notes.append(f"Nationality/country consistent ({nationality})")
        else:
            notes.append(f"Nationality differs: customer {nationality} vs list "
                         f"{', '.join(sorted(countries))} (weak - people hold several nationalities)")
    return support, conflict, notes


def suggest_disposition(score: float, threshold: float, support: list, conflict: list,
                        cust_type: str, entry: ListEntry) -> tuple[str, str]:
    if score < threshold:
        return NO_MATCH, "Below threshold"
    if "type" in conflict:
        return FALSE_POSITIVE, "Name similar but entity type differs (individual vs entity/vessel)"
    if "dob" in conflict:
        return FALSE_POSITIVE, "Name similar but date of birth does not match the list entry"
    if score >= TRUE_MATCH_SCORE and "dob" in support:
        return TRUE_MATCH, "Strong name match confirmed by exact date of birth - block/reject and report"
    if score >= TRUE_MATCH_SCORE and "dob_year" in support and "nationality" in support:
        return TRUE_MATCH, "Strong name match, birth year and nationality consistent - block/reject and report"
    if score >= 97 and "nationality" in support and not entry.dob_years:
        return TRUE_MATCH, "Near-exact name and matching nationality; list has no DOB to compare"
    return POTENTIAL, "Name match not resolved by secondary identifiers - analyst review required"


# --------------------------------------------------------------------------
class Screener:
    def __init__(self, include_consolidated: bool = True, threshold: float = DEFAULT_THRESHOLD,
                 arabic_rules: bool = True):
        self.arabic_rules = arabic_rules
        self.entries, self.names = load_lists(include_consolidated, arabic_rules=arabic_rules)
        self.threshold = threshold
        self._sorted = [n.norm.sorted_text for n in self.names]
        self._skel = [" ".join(sorted(n.norm.skeletons)) for n in self.names]
        self._tok_index: dict[str, list[int]] = defaultdict(list)
        for i, n in enumerate(self.names):
            for t in set(n.norm.tokens) | {"~" + s for s in n.norm.skeletons if s}:
                self._tok_index[t].append(i)

    @property
    def stats(self) -> dict:
        src = Counter(e.source for e in self.entries.values())
        return {"entries": len(self.entries), "sdn_entries": src.get("SDN", 0),
                "consolidated_entries": src.get("CONS", 0), "names_incl_aliases": len(self.names)}

    # ---- candidate generation (fast, C++ rapidfuzz) ----
    def _candidates(self, q: NormalizedName) -> set[int]:
        cands: set[int] = set()
        for _, _, idx in process.extract(q.sorted_text, self._sorted, scorer=fuzz.token_sort_ratio,
                                         limit=50, score_cutoff=55):
            cands.add(idx)
        for _, _, idx in process.extract(q.sorted_text, self._sorted,
                                         scorer=JaroWinkler.normalized_similarity,
                                         limit=30, score_cutoff=0.80):
            cands.add(idx)
        qs = " ".join(sorted(q.skeletons))
        for _, _, idx in process.extract(qs, self._skel, scorer=fuzz.token_sort_ratio,
                                         limit=50, score_cutoff=65):
            cands.add(idx)
        # inverted index: names sharing >= 2 words (or skeletons) with the query
        if len(q.tokens) >= 2:
            counts: Counter = Counter()
            for tok, sk in set(zip(q.tokens, q.skeletons)):
                postings = set(self._tok_index.get(tok, [])) | set(self._tok_index.get("~" + sk, []))
                counts.update(postings)
            cands.update(i for i, c in counts.most_common(600) if c >= 2)
        return cands

    def screen(self, name: str, cust_type: str = "individual", dob: str = "",
               nationality: str = "", threshold: float | None = None, max_hits: int = 5,
               owners: str = "") -> ScreenResult:
        threshold = self.threshold if threshold is None else threshold
        cust_type = (cust_type or "individual").strip().lower()
        if cust_type not in ("individual", "entity"):
            cust_type = "entity" if cust_type in ("company", "organization", "organisation", "business") else "individual"
        q = normalize_name(name, is_entity=(cust_type == "entity"), arabic_rules=self.arabic_rules)

        best: dict[str, Hit] = {}
        for idx in self._candidates(q):
            iname: IndexedName = self.names[idx]
            score, comps, pairs = score_names(q, iname.norm, initials=(cust_type == "individual"))
            if score < min(threshold, 70):
                continue
            prev = best.get(iname.entry_uid)
            if prev and (prev.score > score or (prev.score == score and prev.name_type == "primary")):
                continue
            entry = self.entries[iname.entry_uid]
            hit = Hit(score=score, entry=entry, matched_name=iname.name,
                      name_type=iname.name_type, components=comps)
            hit.reasons = self._explain(q, iname, pairs, score)
            best[iname.entry_uid] = hit

        # ties: prefer primary-name matches, then SDN over non-SDN
        hits = sorted(best.values(), key=lambda h: (-round(h.score, 1), h.name_type != "primary",
                                                    h.entry.source != "SDN"))
        hits = [h for h in hits if h.score >= threshold][:max_hits]
        for h in hits:
            support, conflict, notes = secondary_checks(h.entry, cust_type, dob, nationality)
            h.secondary = notes
            h.disposition, h.disposition_reason = suggest_disposition(
                h.score, threshold, support, conflict, cust_type, h.entry)

        res = ScreenResult(query=name, normalized=q, hits=hits, threshold=threshold)
        if owners and cust_type == "entity":
            res.ownership_note = self._fifty_percent(owners, threshold)
        return res

    # ---- 50% rule ----
    def _fifty_percent(self, owners: str, threshold: float) -> str:
        """owners: 'Name|pct; Name|pct'. Aggregates ownership by owners that hit the list."""
        total, flagged = 0.0, []
        for part in [p for p in owners.split(";") if p.strip()]:
            nm, _, pct = part.partition("|")
            try:
                pct_v = float(pct.strip().rstrip("%") or 0)
            except ValueError:
                pct_v = 0.0
            r = self.screen(nm.strip(), "individual", threshold=threshold, max_hits=1)
            if r.top and r.top.disposition in (TRUE_MATCH, POTENTIAL):
                total += pct_v
                flagged.append(f"{nm.strip()} ({pct_v:g}%) ~ {r.top.entry.name} "
                               f"[{', '.join(r.top.entry.programs)}] score {r.top.score:.0f}")
        if not flagged:
            return "Beneficial owners screened: no owner matched the list."
        verdict = ("50% Rule: aggregate ownership by possible SDNs is "
                   f"{total:g}% - if confirmed, the entity is itself BLOCKED even though it is not named on the list."
                   if total >= 50 else
                   f"Owners with possible list matches hold {total:g}% (<50%): entity not blocked by the "
                   "50% Rule, but treat as high-risk and monitor.")
        return verdict + " Owners flagged: " + "; ".join(flagged)

    # ---- explanation ----
    @staticmethod
    def _explain(q: NormalizedName, n: IndexedName, pairs, score: float) -> list[str]:
        r: list[str] = []
        if n.name_type != "primary":
            r.append(f"Matched list alias ({n.name_type}) '{n.name}', not only the primary name")
        if q.sorted_text == n.norm.sorted_text:
            r.append("Identical after normalisation" + (" (word order differs)" if q.text != n.norm.text else ""))
        for tok_a, tok_b, s, how in pairs:
            if tok_b is None:
                r.append(f"No counterpart for '{tok_a}'")
            elif how == "phonetic" and tok_a != tok_b:
                r.append(f"'{tok_a}' ~ '{tok_b}' sound alike (skeleton match), {s:.0f}%")
            elif how == "initial":
                r.append(f"Initial '{tok_a if len(tok_a) == 1 else tok_b}' consistent with "
                         f"'{tok_b if len(tok_a) == 1 else tok_a}'")
            elif how == "fuzzy":
                r.append(f"'{tok_a}' ~ '{tok_b}' spelling similarity {s:.0f}%")
        for note in q.notes:
            r.append("Customer name: " + note)
        for note in n.norm.notes:
            if "transliteration" in note or "cognate" in note or "Joined" in note or "Normalised" in note:
                r.append("List name: " + note)
        q_set, n_set = set(q.tokens), set(n.norm.tokens)
        extra = sorted(n_set - q_set)
        if extra and len(n_set) > len(q_set):
            r.append("List name has additional name parts: " + ", ".join(extra))
        return r
