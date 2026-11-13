"""Step 4: deep-dive on one sub-network - the Vassiliades / Ledra cluster.

Why this cluster? Screening (step 2) returned exact-name matches between
ICIJ nodes and designated parties:
  * Christodoulos G. Vassiliades - Cypriot lawyer designated by the US State
    Department on 12 Apr 2023 (Usmanov-related action) and sanctioned by the
    UK the same day.
  * Vassiliades & Co. (Malta) Limited, Ledra Nominees Limited and Ledra
    Trustees Limited - on the OFAC SDN list per OpenSanctions.
That links both of the portfolio's jurisdictions (Cyprus and Malta) in one
documented, public, post-leak sanctions action.

What we compute:
  * every ICIJ node in scope whose name matches the cluster (the "anchors")
  * every entity those anchors are attached to, and how (role)
  * the jurisdictions, leak sources and incorporation years of those entities
  * other officers of those entities by country (Russia / Gulf exposure)

IMPORTANT framing: the leaked records pre-date the 2023 designations
(Panama Papers data runs to 2015, Paradise Papers to ~2016). A company
administered by a firm that was LATER sanctioned is not itself sanctioned and
is not evidence of wrongdoing. The output is a list of entities an EDD
analyst would want to re-screen and look at under the OFAC 50 Percent Rule.
"""
import re
from collections import Counter

import pandas as pd

from config import PROCESSED, OUTPUTS, FOCUS_COUNTRIES
from screening import looks_corporate

ANCHOR_PATTERN = re.compile(r"VASSILIADES|\bLEDRA\b", re.I)


def main():
    nodes = pd.read_csv(PROCESSED / "nodes.csv", dtype=str).fillna("")
    edges = pd.read_csv(PROCESSED / "edges.csv", dtype=str).fillna("")
    hits = pd.read_csv(PROCESSED / "screening_hits_all.csv", dtype=str).fillna("")
    name = nodes.set_index("node_id").name.to_dict()
    ntype = nodes.set_index("node_id").node_type.to_dict()
    ctry = nodes.set_index("node_id").country_codes.to_dict()
    info = nodes.set_index("node_id")

    anchors = nodes[nodes.name.str.contains(ANCHOR_PATTERN) & nodes.node_type.ne("address")].copy()
    sanctioned_ids = set(hits[hits.list_tier.str.startswith("1") & hits.grade.str[0].isin(["A", "B"])].icij_node_id)
    anchors["screening_match"] = anchors.node_id.isin(sanctioned_ids)
    # Analyst discipline: a shared word is not a shared identity. "Ledra" is a
    # common Cypriot name (ancient Nicosia) and "Duval Vassiliades Solicitors"
    # is a different UK firm. Keep only nodes that (a) matched a sanctions list
    # entry or (b) are the Vassiliades law firm acting as ICIJ intermediary.
    # Everything else is written out separately for manual review.
    is_firm_intermediary = anchors.node_type.eq("intermediary") & anchors.name.str.upper().str.contains("CHRISTODOULOS")
    excluded = anchors[~(anchors.screening_match | is_firm_intermediary)]
    anchors = anchors[anchors.screening_match | is_firm_intermediary].copy()
    anchors["display_name"] = anchors.apply(
        lambda r: r["name"] if (looks_corporate(r["name"]) or r.node_type == "intermediary"
                                or "CHRISTODOULOS" in r["name"].upper())
        else "[individual - ICIJ node %s]" % r.node_id, axis=1)

    ids = set(anchors.node_id)
    # Anchor -> entity links (officer_of / intermediary_of), or the anchor is itself an entity.
    links = edges[edges.node_id_start.isin(ids) & edges.rel_type.isin(["officer_of", "intermediary_of"])]
    ent_ids = set(links.node_id_end) | set(anchors[anchors.node_type.eq("entity")].node_id)

    rows = []
    for eid in ent_ids:
        roles = links[links.node_id_end.eq(eid)]
        others = edges[edges.node_id_end.eq(eid) & edges.rel_type.eq("officer_of") & ~edges.node_id_start.isin(ids)]
        oc = Counter(c for o in others.node_id_start for c in ctry.get(o, "").split(";") if c)
        inc = info.at[eid, "incorporation_date"] if eid in info.index else ""
        rows.append({
            "entity_node_id": eid, "entity_name": name.get(eid, ""),
            "jurisdiction": info.at[eid, "jurisdiction_description"] if eid in info.index else "",
            "source": info.at[eid, "sourceID"] if eid in info.index else "",
            "incorporation_year": inc[-4:] if inc else "",
            "status": info.at[eid, "status"] if eid in info.index else "",
            "anchor_roles": "; ".join(sorted({f"{anchors.set_index('node_id').at[r.node_id_start, 'display_name']} ({r.link})"
                                               for r in roles.itertuples()})),
            "other_officer_countries": "; ".join(f"{FOCUS_COUNTRIES.get(c, c)}:{v}" for c, v in oc.most_common(4)),
            "has_russian_officer": "RUS" in oc,
        })
    ents = pd.DataFrame(rows).sort_values(["has_russian_officer", "entity_name"], ascending=[False, True])

    OUTPUTS.mkdir(exist_ok=True)
    anchors[["node_id", "node_type", "display_name", "country_codes", "sourceID", "screening_match"]] \
        .to_csv(OUTPUTS / "case_vassiliades_anchors.csv", index=False)
    ents.to_csv(OUTPUTS / "case_vassiliades_entities.csv", index=False)
    excluded[["node_id", "node_type", "name", "country_codes", "sourceID"]] \
        .to_csv(OUTPUTS / "case_vassiliades_excluded_for_review.csv", index=False)
    print(f"Excluded {len(excluded)} name-similar nodes for manual review: "
          + ", ".join(sorted(set(excluded.name))))

    print(f"Anchors: {len(anchors)} nodes ({anchors.screening_match.sum()} with sanctions-list name match)")
    print(anchors.node_type.value_counts().to_string())
    print(f"Entities attached to anchors: {len(ents)}")
    print("By leak source:\n" + ents.source.value_counts().to_string())
    print("By jurisdiction:\n" + ents.jurisdiction.value_counts().head(8).to_string())
    print("Incorporation years:\n" + ents.incorporation_year.replace("", "n/a").value_counts().sort_index().to_string())
    print(f"Entities with >=1 Russia-linked co-officer: {ents.has_russian_officer.sum()}")
    print("Role counts:\n" + links.link.value_counts().to_string())
    return anchors, ents


if __name__ == "__main__":
    main()
