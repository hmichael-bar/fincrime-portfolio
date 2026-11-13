"""Step 2b: apply the analyst's manual dispositions to the screening hits.

An automated screen produces alerts; an analyst decides which are real.
`data/analyst_review.csv` records those decisions (probable match / possible
match / ambiguous / false positive) with a one-line rationale, keyed on the
normalised name. This mirrors how a bank documents alert dispositions so a
reviewer or examiner can see *why* each alert was closed or escalated.

Outputs:
  outputs/screening_results_reviewed.csv - grade A/B hits with disposition
  data/reviewed_public_figures.csv       - ICIJ node ids we may name in outputs
"""
import pandas as pd

from config import PROCESSED, OUTPUTS, ROOT
from screening import normalise

NAMEABLE = {"probable match", "possible match", "ambiguous"}


def main():
    hits = pd.read_csv(PROCESSED / "screening_hits_all.csv", dtype=str).fillna("")
    review = pd.read_csv(ROOT / "data" / "analyst_review.csv", dtype=str).fillna("")
    review["key"] = review.icij_name_key.apply(normalise)
    review = review.drop_duplicates("key")

    hits = hits[hits.grade.str[0].isin(["A", "B"])].copy()
    hits["key"] = hits.icij_name.apply(normalise)
    out = hits.merge(review[["key", "disposition", "rationale"]], on="key", how="left")
    out["disposition"] = out.disposition.fillna("not yet reviewed")
    out["rationale"] = out.rationale.fillna("")

    cols = ["disposition", "list_tier", "grade", "icij_name", "icij_type", "icij_countries", "icij_source",
            "icij_node_id", "os_name", "os_countries", "os_birth_date", "score", "country_match",
            "os_url", "rationale"]
    out = out.sort_values(["disposition", "list_tier", "icij_name"])[cols]
    # Privacy: unreviewed person hits are written with the name withheld.
    from screening import looks_corporate
    person_unrev = out.icij_type.eq("officer") & ~out.icij_name.apply(looks_corporate) & \
        ~out.disposition.isin(NAMEABLE)
    out.loc[person_unrev, "icij_name"] = "[individual - name withheld; see ICIJ node id]"
    OUTPUTS.mkdir(exist_ok=True)
    out.to_csv(OUTPUTS / "screening_results_reviewed.csv", index=False)

    nameable = out[out.disposition.isin(NAMEABLE)][["icij_node_id", "disposition"]].drop_duplicates()
    nameable.to_csv(ROOT / "data" / "reviewed_public_figures.csv", index=False)

    summary = out.drop_duplicates("icij_node_id").groupby(["disposition", "list_tier"]).size()
    print("Reviewed screening results (unique ICIJ nodes):")
    print(summary.to_string())


if __name__ == "__main__":
    main()
