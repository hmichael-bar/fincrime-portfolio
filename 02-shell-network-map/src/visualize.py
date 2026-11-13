"""Step 5: interactive network maps (pyvis -> self-contained HTML).

Two maps, because one 43,000-node hairball helps nobody:

1. outputs/cyprus_corridor_overview.html  - the "infrastructure" view.
   Nodes are the top intermediaries, mass-registration addresses and
   high-volume officers. An edge between two of them means they touch the
   same companies; edge width = number of shared companies. This shows which
   service providers, addresses and nominees work together.

2. outputs/case_vassiliades_network.html  - the drill-down.
   The designated Vassiliades/Ledra nodes (duplicates merged), every company
   they are attached to in the leaks, and the Russia-linked co-officers.

Privacy rule: private individuals are never labelled by name; they appear as
"Individual (country)". Firms, intermediaries and designated parties are named.
"""
import itertools
from collections import Counter, defaultdict

import pandas as pd
from pyvis.network import Network

from config import PROCESSED, OUTPUTS
from screening import looks_corporate, normalise

COLORS = {"entity": "#5B8FF9", "officer": "#5AD8A6", "intermediary": "#F6BD16",
          "address": "#9270CA", "sanctioned": "#E8684A", "malta": "#FF9D4D",
          "individual": "#A0A7B4"}

CAVEAT = ("There are legitimate uses for offshore companies and trusts. ICIJ does not "
          "intend to suggest or imply that any people, companies or other entities included "
          "in the ICIJ Offshore Leaks Database have broken the law or otherwise behaved "
          "improperly. Name matches to sanctions/PEP lists are leads for review, not identifications.")


def legend_html(title, items, subtitle):
    chips = "".join(f'<span style="display:inline-flex;align-items:center;margin-right:14px">'
                    f'<span style="width:12px;height:12px;border-radius:50%;background:{c};'
                    f'display:inline-block;margin-right:6px"></span>{t}</span>' for t, c in items)
    return (f'<div style="font-family:system-ui,-apple-system,Segoe UI,sans-serif;padding:14px 18px;'
            f'background:#0f172a;color:#e2e8f0">'
            f'<div style="font-size:18px;font-weight:600">{title}</div>'
            f'<div style="font-size:13px;opacity:.85;margin:4px 0 8px">{subtitle}</div>'
            f'<div style="font-size:13px">{chips}</div>'
            f'<div style="font-size:11px;opacity:.7;margin-top:8px;max-width:1100px">{CAVEAT} '
            f'Source: ICIJ Offshore Leaks Database (ODbL / CC BY-SA); OpenSanctions (CC BY-NC).</div></div>')


def save(net, path, header):
    net.toggle_physics(True)
    net.set_options("""{"physics":{"barnesHut":{"gravitationalConstant":-9000,"springLength":140,
      "springConstant":0.02,"damping":0.25},"stabilization":{"iterations":400}},
      "interaction":{"hover":true,"navigationButtons":true,"tooltipDelay":120},
      "edges":{"smooth":false,"color":{"opacity":0.45}}}""")
    html = net.generate_html()
    html = html.replace("<body>", "<body style='margin:0;background:#0b1220'>" + header, 1)
    path.write_text(html, encoding="utf-8")
    print(f"  wrote {path.name}")


def load():
    nodes = pd.read_csv(PROCESSED / "nodes.csv", dtype=str).fillna("")
    edges = pd.read_csv(PROCESSED / "edges.csv", dtype=str).fillna("")
    hits = pd.read_csv(PROCESSED / "screening_hits_all.csv", dtype=str).fillna("")
    return nodes, edges, hits


def overview(nodes, edges, hits):
    info = nodes.set_index("node_id")
    hubs = pd.read_csv(OUTPUTS / "hub_intermediaries.csv", dtype=str).head(15)
    addrs = pd.read_csv(OUTPUTS / "shared_addresses.csv", dtype=str).head(12)
    noms = pd.read_csv(OUTPUTS / "nominee_patterns.csv", dtype=str).head(20)
    # Only analyst-reviewed probable/possible matches are drawn - never raw alerts.
    rev = pd.read_csv(OUTPUTS / "screening_results_reviewed.csv", dtype=str).fillna("")
    sanc_ids = set(rev[rev.disposition.isin(["probable match", "possible match"])].icij_node_id)

    infra = {}
    for r in hubs.itertuples():
        infra[r.node_id] = ("intermediary", r.name, int(r.entities_served))
    for r in addrs.itertuples():
        infra[r.node_id] = ("address", r.address[:70], int(r.entities_registered))
    for r in noms.itertuples():
        infra[r.node_id] = ("officer", r.name, int(r.entities))

    # Which companies does each infrastructure node touch?
    touches = defaultdict(set)
    for e in edges.itertuples(index=False):
        if e.node_id_start in infra:
            touches[e.node_id_start].add(e.node_id_end)
        if e.node_id_end in infra and e.rel_type == "registered_address":
            pass
        if e.node_id_end in infra:
            touches[e.node_id_end].add(e.node_id_start)
    # Add designated-party nodes that touch the same companies (ties sanctions to infrastructure).
    sanc_touch = defaultdict(set)
    for e in edges[edges.node_id_start.isin(sanc_ids)].itertuples(index=False):
        sanc_touch[e.node_id_start].add(e.node_id_end)

    net = Network(height="820px", width="100%", bgcolor="#0b1220", font_color="#e2e8f0", cdn_resources="in_line")
    for nid, (kind, label, n) in infra.items():
        ind = kind == "officer" and not looks_corporate(info.at[nid, "name"])
        color = COLORS["individual"] if ind else COLORS[kind]
        net.add_node(nid, label=label[:40], color=color, size=10 + n ** 0.5, font={"size": 16, "color": "#e2e8f0"},
                     title=f"{label}\n{kind} | {info.at[nid, 'country_codes']}\n{n} companies in scope",
                     shape="dot" if kind != "address" else "square")
    for a, b in itertools.combinations(infra, 2):
        shared = len(touches[a] & touches[b])
        if shared >= 3:
            net.add_edge(a, b, value=shared, title=f"{shared} shared companies")
    # Merge designated-party duplicates by normalised name for readability.
    merged = defaultdict(set)
    for sid, comps in sanc_touch.items():
        merged[normalise(info.at[sid, "name"])] |= comps
    for key, comps in merged.items():
        links = [(nid, len(comps & touches[nid])) for nid in infra if len(comps & touches[nid]) >= 2]
        if not links:
            continue
        label = next(info.at[s, "name"] for s in sanc_touch if normalise(info.at[s, "name"]) == key)
        sid = "S:" + key
        net.add_node(sid, label=label[:40], color=COLORS["sanctioned"], size=14, shape="diamond", font={"size": 16, "color": "#e2e8f0"},
                     title=f"{label}\nAnalyst-reviewed probable/possible match to a US/EU/UK/UN sanctions list entry (OpenSanctions)\n{len(comps)} companies in scope")
        for nid, w in links:
            net.add_edge(sid, nid, value=w, title=f"{w} shared companies", color="#E8684A")
    header = legend_html(
        "Cyprus corridor: the offshore infrastructure map",
        [("Intermediary (company formation agent / law firm)", COLORS["intermediary"]),
         ("Mass-registration address", COLORS["address"]), ("High-volume corporate officer", COLORS["officer"]),
         ("High-volume individual officer (name withheld)", COLORS["individual"]),
         ("Reviewed sanctions-list match", COLORS["sanctioned"])],
        "Top 15 intermediaries, 12 shared addresses and 20 high-volume officers in the Cyprus subset of the ICIJ data. "
        "Edge width = companies two nodes have in common. Hover for details; scroll to zoom.")
    save(net, OUTPUTS / "cyprus_corridor_overview.html", header)


def case_map(nodes, edges):
    info = nodes.set_index("node_id")
    anchors = pd.read_csv(OUTPUTS / "case_vassiliades_anchors.csv", dtype=str).fillna("")
    ents = pd.read_csv(OUTPUTS / "case_vassiliades_entities.csv", dtype=str).fillna("")
    anchor_key = {r.node_id: normalise(r.display_name) for r in anchors.itertuples()}
    key_label = {}
    for r in anchors.itertuples():
        key_label.setdefault(anchor_key[r.node_id], (r.display_name, r.screening_match == "True"))
    ent_ids = set(ents.entity_node_id)

    net = Network(height="860px", width="100%", bgcolor="#0b1220", font_color="#e2e8f0", cdn_resources="in_line")
    deg = Counter()
    links = edges[edges.node_id_start.isin(anchor_key) & edges.node_id_end.isin(ent_ids)]
    for r in links.itertuples():
        deg[anchor_key[r.node_id_start]] += 1
    for key, (label, matched) in key_label.items():
        if deg[key] == 0 and key not in {normalise(info.at[e, "name"]) for e in ent_ids}:
            continue
        net.add_node("A:" + key, label=label[:38], shape="diamond", size=16 + deg[key] ** 0.5 * 2,
                     font={"size": 22, "color": "#ffffff", "strokeWidth": 3, "strokeColor": "#0b1220"},
                     color=COLORS["sanctioned"] if matched else COLORS["intermediary"],
                     title=f"{label}\n{'Name matches US sanctions list entry (OpenSanctions)' if matched else 'Law-firm intermediary record'}\n{deg[key]} links to companies")
    for r in ents.itertuples():
        malta = r.jurisdiction == "Malta"
        net.add_node(r.entity_node_id, label=r.entity_name[:30], size=7, shape="dot",
                     color=COLORS["malta"] if malta else COLORS["entity"],
                     title=(f"{r.entity_name}\n{r.jurisdiction or 'jurisdiction n/a'} | inc. {r.incorporation_year or 'n/a'} | {r.status or ''}\n"
                            f"Leak: {r.source}\nOther officers: {r.other_officer_countries or 'none recorded'}"))
    seen = set()
    for r in links.itertuples():
        k = ("A:" + anchor_key[r.node_id_start], r.node_id_end)
        if k in seen:
            continue
        seen.add(k)
        net.add_edge(*k, title=r.link)
    # Russia-linked co-officers for companies that have them (names withheld unless corporate).
    rus = ents[ents.has_russian_officer == "True"].entity_node_id
    co = edges[edges.node_id_end.isin(rus) & edges.rel_type.eq("officer_of") & ~edges.node_id_start.isin(anchor_key)]
    for r in co.itertuples():
        nm, cc = info.at[r.node_id_start, "name"], info.at[r.node_id_start, "country_codes"]
        if "RUS" not in cc.split(";"):
            continue
        corp = looks_corporate(nm)
        net.add_node(r.node_id_start, label=nm[:30] if corp else f"Individual ({cc})", size=6,
                     color=COLORS["officer"] if corp else COLORS["individual"],
                     title=(nm if corp else "Private individual - name withheld") + f"\n{cc}\nrole: {r.link}")
        net.add_edge(r.node_id_start, r.node_id_end, title=r.link, color="#5AD8A6")
    header = legend_html(
        "Case study: the Vassiliades / Ledra cluster across Cyprus, Malta and the BVI",
        [("Designated party (name match, merged duplicates)", COLORS["sanctioned"]),
         ("Law-firm intermediary record", COLORS["intermediary"]),
         ("Company, Malta registry", COLORS["malta"]), ("Company, other jurisdictions", COLORS["entity"]),
         ("Russia-linked co-officer (company)", COLORS["officer"]),
         ("Russia-linked co-officer (individual, name withheld)", COLORS["individual"])],
        "Leak records (1990s to 2018) pre-date the April 2023 US/UK designations. Being administered by a "
        "later-designated firm does not make a company sanctioned. It makes the company a re-screening priority.")
    save(net, OUTPUTS / "case_vassiliades_network.html", header)


def main():
    nodes, edges, hits = load()
    overview(nodes, edges, hits)
    case_map(nodes, edges)


if __name__ == "__main__":
    main()
