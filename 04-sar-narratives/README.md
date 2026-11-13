# 04 · SAR Narratives

**Three Suspicious Activity Report (SAR) case files written to FinCEN's narrative guidance, plus a one-page guide to writing SAR narratives.** Two cases come from real alerts in the [transaction monitoring simulator](../03-transaction-monitoring/), so every figure traces back to a transaction ID. The third is a stand-alone sanctions-evasion / trade-based money laundering case.

> ⚠️ **Everything here is FICTIONAL / SYNTHETIC.** The bank (Meridian Harbor Bank), the people, the companies, the accounts and the transactions are invented. Investigative facts that the dataset cannot contain (teller video, victim claims, freight records) are marked *[simulated]*. None of these are real filings.

## Contents

| File | Case | Source | Amount |
|---|---|---|---|
| [`cases/SAR-01_structuring.md`](cases/SAR-01_structuring.md) | Structuring: 14 cash deposits just under $10K at 8 branches, sent on to another bank | Project 03, alert ALT-00153 (customer C0298) | $126,340 |
| [`cases/SAR-02_mule_network.md`](cases/SAR-02_mule_network.md) | Money mule account: 198 scam victims, two collectors, then Hong Kong / UAE wires and crypto | Project 03, alert ALT-00256 (C0221, C0057, C0106) | $494,635 into the mule; $1.68M into the collectors |
| [`cases/SAR-03_tbml_gulf_freezone.md`](cases/SAR-03_tbml_gulf_freezone.md) | TBML and export-control evasion through a UAE free-zone front company | Stand-alone fictional case | $1,400,218 |
| [`HOW_TO_WRITE_A_SAR_NARRATIVE.md`](HOW_TO_WRITE_A_SAR_NARRATIVE.md) | One-page guide: structure, 5 Ws, style rules, 10 common mistakes, before/after example | | |
| [`supporting_data/`](supporting_data/) | CSVs and tables extracted from project 03 for SARs 1 and 2 | `tools/extract_case_data.py` | |
| [`pdf/`](pdf/) | Formatted PDFs of all three cases and the guide, plus one combined file | `tools/build_pdf.py` | |

## How each case file is organised
1. **Case summary:** subjects, accounts, dates, amount, SAR categories, filing date.
2. **Red flags:** each one tied to a regulatory source (FFIEC Manual, FinCEN advisories, FATF).
3. **Investigation steps taken:** what was checked and what was found.
4. **Supporting transaction tables.**
5. **The SAR narrative (Part V):** introduction, chronological body, conclusion. Facts, not opinions.
6. **Why this narrative works:** a short self-review against the who / what / when / where / why / how checklist.

## Points worth raising in an interview
- **Structuring is a crime even when the money is clean** (31 U.S.C. 5324). SAR 1 never speculates about where the cash came from.
- **Mule cases are network cases.** SAR 2 follows the money from the victims, to the mule, to the collectors, and on to offshore accounts and crypto, and names each subject's role.
- **Sanctions vs AML.** In SAR 3 nobody matched a sanctions list, so nothing was blocked. The suspicious *behaviour* (third-party payers, rebates, re-export to Russia) is reported by SAR, using FinCEN's key term `FIN-2022-RUSSIABIS`.
- **Timeline.** Project 03 runs as a look-back review on 2026-07-01 over January to June activity, so SARs 1 and 2 are filed in late July 2026, within 30 days of the investigator's decision that the activity is suspicious.

## Rebuild
```bash
cd 04-sar-narratives
../03-transaction-monitoring/.venv/bin/python tools/extract_case_data.py   # refresh supporting tables from project 03
../03-transaction-monitoring/.venv/bin/python tools/build_pdf.py           # markdown → HTML → PDF (headless Google Chrome)
```

## Sources used for the format
- FinCEN, *Guidance on Preparing a Complete & Sufficient Suspicious Activity Report Narrative* (2003)
- FFIEC BSA/AML Examination Manual: suspicious activity reporting; appendix on red flags
- FinCEN/BIS joint alerts on Russian export-control evasion (FIN-2022-Alert003, FIN-2023-Alert004)
- FATF, *Trade-Based Money Laundering: Risk Indicators* (2021)
