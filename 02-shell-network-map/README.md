# 02 · Shell Company Network Map: The Cyprus Corridor

**Question:** Who builds and runs the offshore structures that route through Cyprus (and Malta), and where do they touch sanctioned parties?

**Answer, in one line:** A handful of Cyprus corporate-service providers created thousands of BVI and Seychelles companies for mostly Russian and CIS clients. One designated network, the Vassiliades / Ledra law-firm group (US and UK designations of 12 April 2023), shows up across **four leak sets and the Malta company registry** and is attached to **278 companies**.

| Deliverable | File |
|---|---|
| Findings memo (EDD style, 3 pages) | [`FINDINGS_MEMO.md`](FINDINGS_MEMO.md) · [`FINDINGS_MEMO.pdf`](FINDINGS_MEMO.pdf) (rendered with `../05-typology-reports/tools/build_pdfs.py`) |
| Interactive infrastructure map | [`outputs/cyprus_corridor_overview.html`](outputs/cyprus_corridor_overview.html) |
| Interactive case-study map | [`outputs/case_vassiliades_network.html`](outputs/case_vassiliades_network.html) |
| Interview prep | [`HOW_IT_WORKS.md`](HOW_IT_WORKS.md) |
| All result tables | [`outputs/`](outputs/) (CSV + `summary.json`) |

> **Caveat (ICIJ):** There are legitimate uses for offshore companies and trusts. ICIJ does not intend to suggest or imply that any people, companies or other entities included in the ICIJ Offshore Leaks Database have broken the law or otherwise behaved improperly. Name matches to sanctions or PEP lists in this project are **leads for review, not identifications**.

---

## Data sources

| Source | What it is | Licence |
|---|---|---|
| [ICIJ Offshore Leaks Database](https://offshoreleaks.icij.org/pages/database) bulk CSV (`full-oldb.LATEST.zip`, build of 9 Sep 2026) | ~2M nodes (companies, officers, intermediaries, addresses) and ~3.3M relationships from the Panama, Paradise, Pandora, Bahamas and 2013 Offshore Leaks | ODbL (database), CC BY-SA (contents) |
| [OpenSanctions "default"](https://www.opensanctions.org/datasets/default/) `targets.simple.csv` | Sanctions lists (OFAC SDN, EU, UK, UN and 40+ others) plus PEP data, merged and de-duplicated | CC BY-NC 4.0 (non-commercial use) |

The primary source (ICIJ) downloaded without problems, so no fallback was needed. The raw files (~1.4 GB) are **not** committed. `data/raw/` is git-ignored, and the commands below re-download them.

## How to run it

```bash
cd 02-shell-network-map
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

# download data (~550 MB)
mkdir -p data/raw/icij data/raw/opensanctions
curl -L -o data/raw/icij/full-oldb.zip https://offshoreleaks-data.icij.org/offshoreleaks/csv/full-oldb.LATEST.zip
unzip -o data/raw/icij/full-oldb.zip -d data/raw/icij
curl -L -o data/raw/opensanctions/targets.simple.csv https://data.opensanctions.org/datasets/latest/default/targets.simple.csv

# run everything (~2 minutes on a laptop)
.venv/bin/python src/pipeline.py
```

## What each step does

| Step | Script | Plain-English explanation |
|---|---|---|
| 1 | `src/build_subset.py` | Takes every node ICIJ tags with Cyprus, adds every company one link away, then adds those companies' other officers, agents and addresses. Result: **43,065 nodes and 73,116 edges** (from ~2M nodes). |
| 2 | `src/screening.py` | Checks every company, officer and intermediary name against ~600k sanctioned and PEP records. Names are cleaned (case, accents, "LTD", "MR"), then matched exactly or fuzzily. Each hit is graded A/B/C by name strength, name rarity and whether the country agrees. |
| 2b | `src/review.py` + `data/analyst_review.csv` | Records the analyst's decision on each important alert (probable match, possible, ambiguous or false positive), with a reason. This is the same audit trail a bank keeps. |
| 3 | `src/analysis.py` | Builds a `networkx` graph and computes centrality, hub intermediaries, shared-address clusters, nominee-director patterns, circular ownership, Russia/Gulf officer links and a simple additive risk score per company. |
| 4 | `src/case_study.py` | Pulls out every company linked to the Vassiliades / Ledra network and profiles it (roles, jurisdictions, dates, Russian co-officers). Name-similar but unrelated records are excluded and logged. |
| 5 | `src/visualize.py` | Writes two self-contained interactive `pyvis` maps (hover, zoom, drag). |

All tunable choices (scope country, thresholds, which relationship types count as "ownership") live in `src/config.py`.

## Headline numbers (from `outputs/summary.json`)

- **18,297** companies in scope: BVI 5,958 · Seychelles 1,709 · **Malta 1,688** · Bahamas 1,219 · Panama 748
- Top 5 intermediaries administer **8,673** of them. The largest (Consulco International, Cyprus/UAE) administers **3,168**.
- **51** addresses host 20+ companies each. **109** officers hold 25+ appointments.
- **1,730** companies have an officer in Russia/Ukraine/Belarus/Kazakhstan, and **991** have one in a GCC state.
- Screening: **1,291** raw alerts → **854** grade A/B → **28** names dispositioned probable/possible, **23** cleared as false positives.
- **4** mutual-shareholding loops (circular ownership).

## Ethics and privacy choices

- **Private individuals are never named** in outputs or maps. They appear as `[individual - ICIJ node 12345]`. Only companies, professional intermediaries and public figures (sanctioned persons or PEPs, after manual review) are named.
- Raw name alerts are **not** treated as findings. Only analyst-reviewed matches are drawn on the maps or discussed in the memo.
- The leak data is dated (to 2015–2018). Findings describe historical structures, not current ownership.

## Folder layout

```
02-shell-network-map/
├── README.md, FINDINGS_MEMO.md/.pdf, HOW_IT_WORKS.md, requirements.txt
├── src/            pipeline code (run src/pipeline.py)
├── data/
│   ├── analyst_review.csv          manual alert dispositions (committed)
│   ├── reviewed_public_figures.csv generated: who may be named
│   ├── raw/                        downloaded data (git-ignored)
│   └── processed/                  generated subset + raw hits (git-ignored)
└── outputs/        maps (.html), result tables (.csv), summary.json
```
