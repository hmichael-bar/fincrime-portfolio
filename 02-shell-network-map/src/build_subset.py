"""Step 1: cut the "Cyprus corridor" out of the full ICIJ Offshore Leaks dump.

The full database has ~2 million nodes and ~3.3 million relationships. We
only need the part that touches Cyprus:

  1. Seeds   = every entity, officer, intermediary or address that ICIJ tags
               with country code CYP (or an entity incorporated in Cyprus).
  2. Core    = every *entity* (company/trust/foundation) that is a seed or is
               directly linked to a seed.
  3. Subset  = all structural relationships touching a core entity, plus the
               nodes at the other end (officers, intermediaries, addresses).

Output: data/processed/nodes.csv and data/processed/edges.csv
"""
import pandas as pd

from config import RAW_ICIJ, PROCESSED, SEED_COUNTRY, STRUCTURAL_RELS

NODE_FILES = {
    "entity": "nodes-entities.csv",
    "officer": "nodes-officers.csv",
    "intermediary": "nodes-intermediaries.csv",
    "address": "nodes-addresses.csv",
    "other": "nodes-others.csv",
}


def has_country(series: pd.Series, code: str) -> pd.Series:
    """ICIJ stores multiple countries as 'CYP;RUS'. True if `code` is one of them."""
    return series.fillna("").str.split(";").apply(lambda codes: code in codes)


def load_nodes() -> pd.DataFrame:
    frames = []
    for node_type, fname in NODE_FILES.items():
        df = pd.read_csv(RAW_ICIJ / fname, dtype=str)
        df["node_type"] = node_type
        if node_type == "address":
            # Address nodes keep the full address text in `address`; use it as the name.
            df["name"] = df["address"].fillna(df["name"])
        frames.append(df)
    nodes = pd.concat(frames, ignore_index=True)
    keep = ["node_id", "node_type", "name", "country_codes", "countries",
            "jurisdiction", "jurisdiction_description", "incorporation_date",
            "inactivation_date", "status", "service_provider", "sourceID"]
    return nodes[[c for c in keep if c in nodes.columns]]


def main() -> None:
    print("Loading ICIJ nodes ...")
    nodes = load_nodes()
    print(f"  {len(nodes):,} nodes in full database")

    seed_mask = has_country(nodes["country_codes"], SEED_COUNTRY) | nodes["jurisdiction"].eq(SEED_COUNTRY)
    seeds = set(nodes.loc[seed_mask, "node_id"])
    entity_ids = set(nodes.loc[nodes.node_type.eq("entity"), "node_id"])
    print(f"  {len(seeds):,} Cyprus-tagged seed nodes")

    print("Loading relationships ...")
    rels = pd.read_csv(RAW_ICIJ / "relationships.csv", dtype=str)
    rels = rels[rels.rel_type.isin(STRUCTURAL_RELS)]

    touching_seed = rels[rels.node_id_start.isin(seeds) | rels.node_id_end.isin(seeds)]
    core = (set(touching_seed.node_id_start) | set(touching_seed.node_id_end) | seeds) & entity_ids
    print(f"  {len(core):,} core entities (Cyprus-tagged or one hop from a Cyprus node)")

    edges = rels[rels.node_id_start.isin(core) | rels.node_id_end.isin(core)].copy()
    edges = edges.drop_duplicates(["node_id_start", "node_id_end", "link"])
    keep_ids = set(edges.node_id_start) | set(edges.node_id_end)
    sub_nodes = nodes[nodes.node_id.isin(keep_ids)].drop_duplicates("node_id").copy()
    sub_nodes["is_core_entity"] = sub_nodes.node_id.isin(core)
    sub_nodes["is_cyprus_seed"] = sub_nodes.node_id.isin(seeds)

    PROCESSED.mkdir(parents=True, exist_ok=True)
    sub_nodes.to_csv(PROCESSED / "nodes.csv", index=False)
    edges.to_csv(PROCESSED / "edges.csv", index=False)
    print(f"Saved subset: {len(sub_nodes):,} nodes, {len(edges):,} edges")
    print(sub_nodes.node_type.value_counts().to_string())


if __name__ == "__main__":
    main()
