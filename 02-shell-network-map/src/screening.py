"""Step 2: screen names in the Cyprus subset against OpenSanctions.

OpenSanctions' "default" collection merges 300+ sources: OFAC SDN, EU, UK,
UN and other sanctions lists, plus PEP (politically exposed person) data.
We keep only records that are (a) sanctioned or (b) PEPs, and only people,
companies and organisations.

Matching works like a basic screening engine:
  1. Normalise names (upper-case, strip accents/punctuation, drop titles
     and legal suffixes like LTD/LIMITED, sort the tokens).
  2. Exact match on the normalised key  -> score 100.
  3. Otherwise fuzzy match (rapidfuzz token_sort_ratio) inside a "block" of
     candidates that share a token, keeping scores >= MATCH_THRESHOLD.
  4. Grade each hit by name strength and country corroboration.

A name match is NOT an identification. Every hit is a lead for an analyst to
disposition (true match / false positive) using dates of birth, addresses,
etc. The memo only discusses hits that were manually reviewed.
"""
import re
import unicodedata
from collections import defaultdict

import pandas as pd
import pycountry
from rapidfuzz import fuzz

from config import RAW_OS, PROCESSED, OUTPUTS, MATCH_THRESHOLD

CORP_WORDS = r"\b(LIMITED|LTD|INC|CORP|CORPORATION|LLC|L\.L\.C|S\.A|SA|AG|GMBH|PLC|LLP|BV|NV|SRL|SPA|CO|COMPANY|HOLDINGS?|TRUST|FOUNDATION|NOMINEES?|SERVICES|INVESTMENTS?|GROUP|ENTERPRISES?|INTERNATIONAL|MANAGEMENT|CONSULTING|TRADING|CAPITAL|VENTURES?|PARTNERS|ASSOCIATES|BANK|FUND|SECRETARIAL|DIRECTORS|OVERSEAS|GLOBAL)\b"
LEGAL_SUFFIXES = {"LIMITED", "LTD", "INC", "CORP", "CORPORATION", "LLC", "SA", "AG",
                  "GMBH", "PLC", "LLP", "BV", "NV", "SRL", "SPA", "CO", "COMPANY", "THE"}
TITLES = {"MR", "MRS", "MS", "MISS", "DR", "SIR", "LORD", "LADY", "HE", "SHEIKH", "PROF"}

# Which OpenSanctions source datasets count as what. We use explicit lists
# because OpenSanctions also carries debarment, enforcement and research
# datasets that are NOT sanctions (e.g. FINRA actions, Medicaid exclusions).
CORE_SANCTIONS = {   # the lists a US bank screens against first
    "US OFAC Specially Designated Nationals (SDN) List",
    "US OFAC Consolidated (non-SDN) List",
    "EU Financial Sanctions Files (FSF)",
    "EU Council Official Journal Sanctioned Entities",
    "UK FCDO Sanctions List",
    "UN Security Council Consolidated Sanctions",
}
OTHER_SANCTIONS = {  # other national / allied lists
    "Swiss SECO Sanctions/Embargoes", "Canadian Consolidated Autonomous Sanctions List",
    "Australian Sanctions Consolidated List", "Japan Economic Sanctions and List of Eligible People",
    "New Zealand Russia Sanctions", "Ukraine NSDC State Register of Sanctions",
    "French National Asset Freezing System", "Monaco National Fund Freezing List",
    "Belgian Financial Sanctions", "Polish List of Persons and Entities Subject to Sanctions",
    "Latvia FIU Sanctions and Asset Freezes", "Estonia International Sanctions Act List",
    "Lithuanian International Sanctions", "Czech Republic National Sanctions",
    "Qatar Unified Record of Persons and Entities on Sanction List",
    "Türkiye Asset Freezing Sanctions List (MASAK)", "Hong Kong Targeted Financial Sanctions (Cap. 537)",
}
PEP_DATASET_HINTS = ("Politically Exposed", "PEP position annotations", "EveryPolitician",
                     "Legislators", "World Leaders", "Heads of State", "Members of Parliament",
                     "Public Officials")


def classify(datasets: str) -> str:
    ds = set(datasets.split(";"))
    if ds & CORE_SANCTIONS:
        return "1 - US/EU/UK/UN sanctions"
    if ds & OTHER_SANCTIONS:
        return "2 - other national sanctions"
    if any(h in datasets for h in PEP_DATASET_HINTS):
        return "3 - PEP"
    return ""


def looks_corporate(name: str) -> bool:
    return bool(re.search(CORP_WORDS, name.upper()))


def normalise(name: str) -> str:
    if not isinstance(name, str):
        return ""
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Z0-9 ]", " ", s.upper())
    tokens = [t for t in s.split() if t not in TITLES and t not in LEGAL_SUFFIXES]
    return " ".join(sorted(tokens))


def alpha3_to_alpha2(codes: str) -> set:
    out = set()
    for c in (codes or "").split(";"):
        try:
            out.add(pycountry.countries.get(alpha_3=c).alpha_2.lower())
        except AttributeError:
            pass
    return out


def load_watchlist() -> pd.DataFrame:
    cols = ["id", "schema", "name", "aliases", "countries", "dataset", "birth_date"]
    os_df = pd.read_csv(RAW_OS, dtype=str, usecols=cols)
    os_df = os_df[os_df.schema.isin(["Person", "Company", "LegalEntity", "Organization"])]
    os_df["list_tier"] = os_df.dataset.fillna("").apply(classify)
    os_df = os_df[os_df.list_tier.ne("")].copy()
    for c in ["name", "aliases", "countries", "dataset", "birth_date"]:
        os_df[c] = os_df[c].fillna("")

    # Explode aliases so each spelling becomes its own searchable row.
    os_df["all_names"] = (os_df.name.fillna("") + ";" + os_df.aliases.fillna("")).str.split(";")
    wl = os_df.explode("all_names")
    wl = wl[wl.all_names.str.strip().ne("")]
    wl["key"] = wl.all_names.apply(normalise)
    wl = wl[wl.key.str.len() >= 5]
    wl = wl.drop_duplicates(["id", "key"])
    # How many *different* watchlist records share this exact name key?
    # >1 means the name is ambiguous (e.g. "Maxim Ivanov") and needs more data.
    wl["key_freq"] = wl.groupby("key").id.transform("nunique")
    return wl


def screen() -> pd.DataFrame:
    nodes = pd.read_csv(PROCESSED / "nodes.csv", dtype=str)
    subjects = nodes[nodes.node_type.isin(["officer", "entity", "intermediary", "other"])].copy()
    subjects["country_codes"] = subjects.country_codes.fillna("")
    subjects["key"] = subjects.name.apply(normalise)
    subjects = subjects[subjects.key.str.len() >= 5]

    print("Loading OpenSanctions watchlist ...")
    wl = load_watchlist()
    print(f"  {wl.id.nunique():,} sanctioned/PEP records, {len(wl):,} name variants")

    # Index watchlist by full key (exact) and by each token (blocking).
    exact = defaultdict(list)
    block = defaultdict(list)
    for row in wl.itertuples(index=False):
        exact[row.key].append(row)
        for tok in row.key.split():
            if len(tok) >= 4:
                block[tok].append(row)

    hits = []
    for s in subjects.itertuples(index=False):
        s_tokens = s.key.split()
        is_person = s.node_type == "officer" and not looks_corporate(s.name)
        if is_person and len(s_tokens) < 2:
            continue  # single-token person names are too ambiguous to screen
        candidates = {}
        for r in exact.get(s.key, []):
            candidates[(r.id, r.key)] = (r, 100.0)
        # Block on the rarest-looking (longest) token to keep comparisons cheap.
        long_toks = sorted([t for t in s_tokens if len(t) >= 4], key=len, reverse=True)[:2]
        for tok in long_toks:
            pool = block.get(tok, [])
            if len(pool) > 5000:   # very common token (e.g. "TRADING"): skip fuzzy
                continue
            for r in pool:
                if (r.id, r.key) in candidates:
                    continue
                score = fuzz.token_sort_ratio(s.key, r.key)
                if score >= MATCH_THRESHOLD:
                    candidates[(r.id, r.key)] = (r, score)
        for r, score in candidates.values():
            # A person must not be matched to a company and vice versa.
            if is_person and r.schema != "Person":
                continue
            if not is_person and r.schema == "Person":
                continue
            s_c = alpha3_to_alpha2(s.country_codes)
            r_c = set((r.countries or "").split(";")) - {""}
            country_match = bool(s_c & r_c)
            n_tok = len(s_tokens)
            unique_name = r.key_freq == 1
            if score == 100 and unique_name and (country_match or n_tok >= 3):
                grade = "A - strong (exact unique name + country or 3+ name tokens)"
            elif score == 100 or (score >= 96 and country_match):
                grade = "B - moderate (needs DOB/ID check)"
            else:
                grade = "C - weak (fuzzy name only)"
            hits.append({
                "icij_node_id": s.node_id, "icij_type": s.node_type, "icij_name": s.name,
                "icij_countries": s.country_codes, "icij_source": s.sourceID,
                "os_id": r.id, "os_name": r.name, "os_matched_alias": r.all_names,
                "os_schema": r.schema, "os_countries": r.countries, "os_birth_date": r.birth_date,
                "list_tier": r.list_tier,
                "os_datasets": r.dataset, "score": round(score, 1), "watchlist_name_freq": r.key_freq,
                "country_match": country_match, "grade": grade,
                "os_url": f"https://www.opensanctions.org/entities/{r.id}/",
            })
    out = pd.DataFrame(hits)
    if not out.empty:
        out = (out.sort_values(["grade", "list_tier", "score"], ascending=[True, True, False])
                  .drop_duplicates(["icij_node_id", "os_id"]))
    OUTPUTS.mkdir(exist_ok=True)
    out.to_csv(PROCESSED / "screening_hits_all.csv", index=False)
    print(f"  {len(out):,} raw hits")
    if not out.empty:
        print(pd.crosstab(out.grade, out.list_tier).to_string())
    return out


if __name__ == "__main__":
    screen()
