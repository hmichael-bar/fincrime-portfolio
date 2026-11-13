# 05 · Sanctions Evasion Typology Reports

Three analyst-grade typology reports, plus a one-page red-flag cheat sheet. They are written the way a bank's financial intelligence unit or a sanctions-advisory firm would brief compliance teams: **how the scheme works → red flags → real cases → detection and screening controls**, with every factual claim tied to a public source.

| # | Report | Markdown | PDF |
|---|---|---|---|
| 1 | **Shadow fleet oil shipping**: STS transfers, AIS spoofing, flag-hopping, the Russian price cap, Iranian crude | [md](01_shadow_fleet_oil_shipping.md) | [pdf](pdf/01_shadow_fleet_oil_shipping.pdf) |
| 2 | **TBML through Gulf free zones**: over/under-invoicing, front companies, dual-use transshipment (UAE; Qatar where relevant) | [md](02_tbml_gulf_free_zones.md) | [pdf](pdf/02_tbml_gulf_free_zones.pdf) |
| 3 | **Crypto off-ramps**: OTC desks, nested exchanges, mixers, Hydra, Garantex → Grinex → A7A5 | [md](03_crypto_offramps_sanctions_evasion.md) | [pdf](pdf/03_crypto_offramps_sanctions_evasion.pdf) |
| 4 | **Red-flags cheat sheet** (one landscape page combining all three) | [md](04_red_flags_cheat_sheet.md) | [pdf](pdf/04_red_flags_cheat_sheet.pdf) |
| ★ | **Interview prep**: 5 likely questions with model answers | [HOW_IT_WORKS.md](HOW_IT_WORKS.md) | n/a |

## How these connect to the rest of the portfolio

- **Report 1 ↔ Malta dark-fleet case study:** same STS and flag-hopping mechanics. Project 02 found a Cyprus ship manager directing 36 single-ship Malta companies, the corporate structure shadow fleets rely on.
- **Report 2 ↔ Cyprus money-laundering case study and Project 02:** the Cyprus–UAE pairing (a Cyprus shell in the *Petrov* export-control case; a UAE "FZE" among the top Cyprus intermediaries).
- **Report 3 ↔ Russia sanctions:** Garantex and A7A5 show how the ruble economy rebuilt its own off-ramps after 2022.

## Sourcing standard

- **Primary sources first**: OFAC/Treasury press releases and advisories, FinCEN alerts and orders, DOJ releases, FATF/Egmont, IMO, UN Security Council, European Commission.
- **Think tanks and specialists** for analysis and scale estimates: C4ADS (*Oil and Water*), RUSI, KSE Institute, Elliptic. Industry estimates are labelled as such.
- **Every citation was checked** in November 2026: titles, dates and figures were confirmed against the source or reliable coverage of it, and links were tested. Where only secondary coverage was available (e.g. the *Suez Rajan* plea, via AP), the report says so.
- **Allegations stay allegations.** Indictments (Garantex, Petrov) are described as charges, with the presumption of innocence noted.
- **Fast-moving facts are dated.** Price-cap levels and the 2026 US general licences change often. The reports give the date of each figure and tell the reader to check the current regime.

## Rebuilding the PDFs

PDFs are rendered from the Markdown with Python-Markdown and headless Google Chrome (no LaTeX).

```bash
cd 05-typology-reports
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python tools/build_pdfs.py          # writes pdf/*.pdf
```

*Educational analysis from public sources. Not legal advice.*
