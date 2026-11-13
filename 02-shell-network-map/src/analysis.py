"""Step 3: build the network graph and compute the investigative signals.

Signals computed (each written to outputs/ as a CSV):
  * centrality.csv          - which nodes hold the network together
  * hub_intermediaries.csv  - service providers that created/administer many entities
  * shared_addresses.csv    - addresses used by many entities ("mass registration")
  * nominee_patterns.csv    - officers holding board roles at many entities
  * ownership_cycles.csv    - circular ownership (A owns B owns ... owns A)
  * focus_links.csv         - entities with Russia/post-Soviet or Gulf officers
  * entity_risk_scores.csv  - simple additive red-flag score per entity
  * summary.json            - headline numbers used in the memo
"""
import json
import re
from collections import Counter, defaultdict

import networkx as nx
import pandas as pd

from config import (PROCESSED, OUTPUTS, FOCUS_COUNTRIES, GULF, POST_SOVIET,
                    OWNERSHIP_LINKS, DIRECTOR_LINKS, NOMINEE_MIN_ENTITIES)
from screening import looks_corporate, normalise

SECRECY_JURISDICTIONS = {  # entity jurisdiction codes commonly flagged in EDD
    "BVI", "SEY", "PMA", "NIUE", "BAH", "BLZ", "ANG", "SAM", "NEV", "CAYMN",
    "BM", "KY", "VG", "VGB", "SYC", "PAN", "WS", "COOK",
}


def load():
    nodes = pd.read_csv(PROCESSED / "nodes.csv", dtype=str).fillna("")
    edges = pd.read_csv(PROCESSED / "edges.csv", dtype=str).fillna("")
    hits = pd.read_csv(PROCESSED / "screening_hits_all.csv", dtype=str).fillna("")
    return nodes, edges, hits


def build_graph(nodes, edges) -> nx.MultiDiGraph:
    G = nx.MultiDiGraph()
    for n in nodes.itertuples(index=False):
        G.add_node(n.node_id, node_type=n.node_type, name=n.name,
                   countries=n.country_codes, jurisdiction=n.jurisdiction,
                   source=n.sourceID)
    for e in edges.itertuples(index=False):
        G.add_edge(e.node_id_start, e.node_id_end, rel_type=e.rel_type, link=e.link)
    return G


def is_individual(G, n) -> bool:
    d = G.nodes[n]
    return d["node_type"] == "officer" and not looks_corporate(d["name"])


def centrality(U: nx.Graph, G) -> pd.DataFrame:
    # Work on the largest connected component: centrality across disconnected
    # islands is not comparable.
    giant = U.subgraph(max(nx.connected_components(U), key=len)).copy()
    deg = nx.degree_centrality(giant)
    # Exact betweenness is O(n*m); a 2,000-node sample gives a stable ranking.
    btw = nx.betweenness_centrality(giant, k=min(2000, len(giant)), seed=42)
    pr = nx.pagerank(giant)
    rows = [{"node_id": n, "name": G.nodes[n]["name"], "node_type": G.nodes[n]["node_type"],
             "countries": G.nodes[n]["countries"], "degree": giant.degree(n),
             "degree_centrality": deg[n], "betweenness": btw[n], "pagerank": pr[n]}
            for n in giant.nodes]
    df = pd.DataFrame(rows).sort_values("betweenness", ascending=False)
    return df, giant


def hub_intermediaries(G) -> pd.DataFrame:
    rows = []
    for n, d in G.nodes(data=True):
        if d["node_type"] != "intermediary":
            continue
        served = {v for _, v, k in G.out_edges(n, data="rel_type") if k == "intermediary_of"}
        if not served:
            continue
        juris = Counter(G.nodes[v]["jurisdiction"] for v in served)
        rows.append({"node_id": n, "name": d["name"], "countries": d["countries"],
                     "entities_served": len(served),
                     "top_jurisdictions": "; ".join(f"{j or '??'}:{c}" for j, c in juris.most_common(3)),
                     "source": d["source"]})
    return pd.DataFrame(rows).sort_values("entities_served", ascending=False)


def shared_addresses(G) -> pd.DataFrame:
    rows = []
    for n, d in G.nodes(data=True):
        if d["node_type"] != "address":
            continue
        users = [u for u, _, k in G.in_edges(n, data="rel_type") if k == "registered_address"]
        ents = [u for u in users if G.nodes[u]["node_type"] == "entity"]
        if len(ents) < 5:
            continue  # small clusters are usually ordinary offices/homes
        rows.append({"node_id": n, "address": d["name"], "countries": d["countries"],
                     "entities_registered": len(ents), "other_users": len(users) - len(ents)})
    return pd.DataFrame(rows).sort_values("entities_registered", ascending=False)


def nominee_patterns(G, edges) -> pd.DataFrame:
    board = edges[edges.rel_type.eq("officer_of") & edges.link.isin(DIRECTOR_LINKS | OWNERSHIP_LINKS)]
    roles = board.groupby("node_id_start").agg(
        entities=("node_id_end", "nunique"),
        roles=("link", lambda s: "; ".join(f"{k}:{v}" for k, v in Counter(s).most_common(4))))
    roles = roles[roles.entities >= NOMINEE_MIN_ENTITIES].reset_index()
    roles["name"] = roles.node_id_start.map(lambda n: G.nodes[n]["name"])
    roles["countries"] = roles.node_id_start.map(lambda n: G.nodes[n]["countries"])
    roles["officer_kind"] = roles.node_id_start.map(lambda n: "individual" if is_individual(G, n) else "corporate")
    roles["nominee_keyword"] = roles.name.str.contains(r"NOMINEE|SECRETAR|DIRECTORS|TRUSTEE", case=False)
    return roles.rename(columns={"node_id_start": "node_id"}).sort_values("entities", ascending=False)


def ownership_cycles(G, edges) -> pd.DataFrame:
    """Find circular ownership.

    ICIJ often records a company twice: once as an *entity* node and once as
    an *officer* node (when it is a shareholder of another company). To see
    loops we first merge officer nodes into entity nodes with the same
    normalised name (entity resolution), then search for directed cycles.
    """
    own = edges[edges.rel_type.eq("officer_of") & edges.link.isin(OWNERSHIP_LINKS)]
    ent_by_key = defaultdict(list)
    for n, d in G.nodes(data=True):
        if d["node_type"] == "entity":
            ent_by_key[normalise(d["name"])].append(n)

    def resolve(n):
        d = G.nodes[n]
        if d["node_type"] == "officer" and looks_corporate(d["name"]):
            same = ent_by_key.get(normalise(d["name"]), [])
            if len(same) == 1:  # only merge when the match is unambiguous
                return same[0]
        return n

    D = nx.DiGraph()
    for e in own.itertuples(index=False):
        a, b = resolve(e.node_id_start), resolve(e.node_id_end)
        if a != b:
            D.add_edge(a, b, link=e.link)
    rows = []
    for cyc in nx.simple_cycles(D, length_bound=6):
        rows.append({"length": len(cyc),
                     "node_ids": " -> ".join(cyc + [cyc[0]]),
                     "names": " -> ".join(G.nodes[n]["name"] for n in cyc + [cyc[0]])})
    resolved = sum(1 for n in G.nodes if resolve(n) != n)
    return pd.DataFrame(rows, columns=["length", "node_ids", "names"]), D, resolved


def focus_links(G) -> pd.DataFrame:
    rows = []
    for n, d in G.nodes(data=True):
        if d["node_type"] != "entity":
            continue
        officers = [u for u, _, k in G.in_edges(n, data="rel_type") if k == "officer_of"]
        codes = Counter(c for u in officers for c in G.nodes[u]["countries"].split(";") if c)
        ps = sum(v for c, v in codes.items() if c in POST_SOVIET)
        gulf = sum(v for c, v in codes.items() if c in GULF)
        if ps or gulf:
            rows.append({"node_id": n, "name": d["name"], "jurisdiction": d["jurisdiction"],
                         "source": d["source"], "officers": len(officers),
                         "post_soviet_officer_links": ps, "gulf_officer_links": gulf,
                         "officer_countries": "; ".join(f"{FOCUS_COUNTRIES.get(c, c)}:{v}" for c, v in codes.most_common(5))})
    return pd.DataFrame(rows).sort_values(["post_soviet_officer_links", "gulf_officer_links"], ascending=False)


def risk_scores(G, hits, nominees, addresses, cycles_D, cycle_df, focus) -> pd.DataFrame:
    """Additive red-flag score. Weights are judgement calls, documented here:
        +4 linked to a party whose sanctions-list match the analyst marked probable/possible
        +1 linked to an unreviewed grade-A/B sanctions or PEP name match (alert only)
        +2 has a high-volume (nominee-pattern) officer
        +1 registered at an address shared by 20+ entities
        +1 incorporated in a secrecy jurisdiction
        +1 has Russia/post-Soviet or Gulf officer links
        +2 sits on a circular-ownership loop
    Analyst-cleared false positives score nothing.
    """
    reviewed = pd.read_csv(OUTPUTS / "screening_results_reviewed.csv", dtype=str).fillna("")
    confirmed = set(reviewed[reviewed.disposition.isin(["probable match", "possible match"])].icij_node_id)
    alerts = set(reviewed[reviewed.disposition.eq("not yet reviewed")].icij_node_id)
    nominee_ids = set(nominees.node_id)
    busy_addr = set(addresses[addresses.entities_registered >= 20].node_id)
    in_cycle = {n for ids in cycle_df.node_ids for n in ids.split(" -> ")}
    focus_ids = set(focus.node_id)
    rows = []
    for n, d in G.nodes(data=True):
        if d["node_type"] != "entity":
            continue
        nbrs = set(G.predecessors(n)) | set(G.successors(n)) | {n}
        flags, score = [], 0
        if nbrs & confirmed:
            score += 4; flags.append("linked to reviewed sanctions match")
        elif nbrs & alerts:
            score += 1; flags.append("unreviewed sanctions/PEP name alert")
        if nbrs & nominee_ids:
            score += 2; flags.append("high-volume officer")
        if nbrs & busy_addr:
            score += 1; flags.append("mass-registration address")
        if d["jurisdiction"].upper() in SECRECY_JURISDICTIONS:
            score += 1; flags.append("secrecy jurisdiction")
        if n in focus_ids:
            score += 1; flags.append("Russia/Gulf officer links")
        if n in in_cycle:
            score += 2; flags.append("circular ownership")
        if score:
            rows.append({"node_id": n, "name": d["name"], "jurisdiction": d["jurisdiction"],
                         "source": d["source"], "risk_score": score, "flags": "; ".join(flags)})
    return pd.DataFrame(rows).sort_values("risk_score", ascending=False)


def main():
    nodes, edges, hits = load()
    G = build_graph(nodes, edges)
    U = nx.Graph(G.to_undirected())
    print(f"Graph: {G.number_of_nodes():,} nodes, {G.number_of_edges():,} edges, "
          f"{nx.number_connected_components(U):,} connected components")

    cent, giant = centrality(U, G)
    hubs = hub_intermediaries(G)
    addrs = shared_addresses(G)
    noms = nominee_patterns(G, edges)
    cyc_df, D, resolved = ownership_cycles(G, edges)
    focus = focus_links(G)
    risk = risk_scores(G, hits, noms, addrs, D, cyc_df, focus)

    OUTPUTS.mkdir(exist_ok=True)
    # Privacy: never publish a private individual's name in the outputs.
    # Individuals are shown by ICIJ node id unless they are a reviewed
    # public-figure (sanctioned/PEP) match.
    public = set(pd.read_csv(OUTPUTS.parent / "data" / "reviewed_public_figures.csv", dtype=str).icij_node_id) \
        if (OUTPUTS.parent / "data" / "reviewed_public_figures.csv").exists() else set()

    def mask(df, id_col="node_id", name_col="name"):
        df = df.copy()
        ind = df[id_col].map(lambda n: is_individual(G, n) and n not in public)
        df.loc[ind, name_col] = "[individual - ICIJ node " + df.loc[ind, id_col] + "]"
        return df

    mask(cent.head(200)).to_csv(OUTPUTS / "centrality_top200.csv", index=False)
    hubs.to_csv(OUTPUTS / "hub_intermediaries.csv", index=False)  # intermediaries are firms/professionals
    addrs.to_csv(OUTPUTS / "shared_addresses.csv", index=False)
    mask(noms).to_csv(OUTPUTS / "nominee_patterns.csv", index=False)
    cyc_df.to_csv(OUTPUTS / "ownership_cycles.csv", index=False)
    focus.to_csv(OUTPUTS / "focus_links.csv", index=False)
    risk.to_csv(OUTPUTS / "entity_risk_scores.csv", index=False)

    strong = hits[hits.grade.str[0].isin(["A", "B"])]
    summary = {
        "nodes": G.number_of_nodes(), "edges": G.number_of_edges(),
        "node_types": nodes.node_type.value_counts().to_dict(),
        "core_entities": int((nodes.is_core_entity == "True").sum()),
        "connected_components": nx.number_connected_components(U),
        "giant_component_nodes": giant.number_of_nodes(),
        "entity_sources": nodes[nodes.node_type == "entity"].sourceID.value_counts().head(8).to_dict(),
        "entity_jurisdictions": nodes[nodes.node_type == "entity"].jurisdiction_description.value_counts().head(10).to_dict(),
        "malta_registry_entities": int(((nodes.sourceID == "Paradise Papers - Malta corporate registry") & (nodes.node_type == "entity")).sum()),
        "hub_intermediaries_top10": hubs.head(10)[["name", "countries", "entities_served"]].to_dict("records"),
        "shared_address_clusters_5plus": len(addrs),
        "shared_address_clusters_20plus": int((addrs.entities_registered >= 20).sum()),
        "nominee_officers": len(noms),
        "nominee_officers_corporate": int((noms.officer_kind == "corporate").sum()),
        "nominee_officers_individual": int((noms.officer_kind == "individual").sum()),
        "ownership_edges": D.number_of_edges(),
        "officer_nodes_resolved_to_entities": resolved,
        "ownership_cycles": len(cyc_df),
        "entities_with_post_soviet_officers": int((focus.post_soviet_officer_links > 0).sum()),
        "entities_with_gulf_officers": int((focus.gulf_officer_links > 0).sum()),
        "screening_hits_raw": len(hits),
        "screening_hits_grade_AB": len(strong),
        "screening_hits_by_tier_AB": strong.list_tier.value_counts().to_dict(),
        "entities_scored": len(risk),
        "entities_score_ge_6": int((risk.risk_score >= 6).sum()),
    }
    (OUTPUTS / "summary.json").write_text(json.dumps(summary, indent=2, default=int))
    print(json.dumps(summary, indent=2, default=int))
    return G


if __name__ == "__main__":
    main()
