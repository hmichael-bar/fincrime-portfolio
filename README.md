# Financial Crime & Sanctions Portfolio

**H. Michael Bar Bourenane** · Columbia SIPA (MIA, Cyber Policy & Security Assessment) · native Arabic (Levantine, Maghrebi, Gulf) and Hebrew

Six working projects covering the core tasks of an AML, sanctions and KYC analyst. Each one runs on real public data or clearly labelled synthetic data, and each folder has its own README, run instructions and a `HOW_IT_WORKS.md` explainer.

**Portfolio site:** https://hmichael-bar.github.io

| # | Project | What it shows |
|---|---|---|
| 01 | [OFAC sanctions screening engine](01-sanctions-screening/) | Fuzzy name matching against the live SDN list, an Arabic-name transliteration module, secondary-identifier checks, the 50% Rule, threshold tuning |
| 02 | [Cyprus shell-company network map](02-shell-network-map/) | ICIJ Offshore Leaks graph analysis: hub intermediaries, nominee patterns, circular ownership, sanctions/PEP screening, EDD memo |
| 03 | [Transaction monitoring simulator](03-transaction-monitoring/) | Synthetic bank with 8 hidden typologies, 10 detection rules, Isolation Forest, precision/recall, tuning, analyst workbench, 10 alert dispositions |
| 04 | [SAR narratives](04-sar-narratives/) | Three fictional SARs to FinCEN guidance (structuring, mule network, free-zone TBML) and a how-to guide |
| 05 | [Sanctions-evasion typology reports](05-typology-reports/) | Shadow-fleet shipping, TBML via Gulf free zones, crypto off-ramps, with sourced red flags |
| 06 | [Adverse media screener](06-adverse-media-screener/) | English and Arabic negative-news screening with severity scoring and sourced reports |

## Data and privacy

- Customer, account and transaction data in projects 01, 03 and 04 is fictional.
- Sanctions, leak and news data come from public sources (OFAC, OpenSanctions, ICIJ Offshore Leaks, GDELT, Google News). Large raw files are not committed; each README shows how to download them.
- Project 02 never names private individuals. The raw name-screening hits from the leak data are withheld from this repository for that reason.
- There are legitimate uses for offshore companies and trusts. Appearing in leak data does not imply wrongdoing.

These are portfolio and teaching projects, not production compliance systems or legal advice. Built in Python with AI-assisted development.
