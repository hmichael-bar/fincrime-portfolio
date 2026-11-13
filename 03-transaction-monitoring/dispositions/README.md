# Worked Alert Dispositions (L1)

> **Synthetic.** Ten alerts taken from `../outputs/alerts.csv` and worked the way an L1 transaction-monitoring analyst would. Every number in them comes from the synthetic dataset. Checks this project cannot model (sanctions screening, negative news, CTR lookups, RFIs) are marked *[simulated]*.

**Timeline assumption:** the simulator scores all six months in one batch, so the scenario is a **look-back review**. The bank (fictional) runs its newly tuned scenarios on 2026-07-01 over January to June 2026 activity, as banks often do after a system change or a regulator's finding. That is why every disposition is dated July 2026, and why the SARs in project 04 are filed in late July.

| # | Alert | Rule | Customer | Decision | What it shows |
|---|---|---|---|---|---|
| 1 | [ALT-00145](ALT-00145_structuring_close.md) | R01 Structuring | Cohen Deli LLC | **Close (FP)** | A business that files CTRs every few weeks is not avoiding them |
| 2 | [ALT-00132](ALT-00132_rapid_movement_close.md) | R02 Rapid movement | Rideshare driver | **Close (FP)** | Rapid movement with a clear purpose (selling one car, buying another) |
| 3 | [ALT-00036](ALT-00036_high_risk_geo_close.md) | R04 High-risk geography | Bus operator | **Close after RFI** | Grey list is not a sanction, but you still screen. One-off, self-funded family wire. KYC update |
| 4 | [ALT-00027](ALT-00027_tbml_close.md) | R07 TBML | Textile importer | **Close (FP)** | Repeated amounts explained by standing orders to a declared supplier |
| 5 | [ALT-00001](ALT-00001_shared_device_close.md) | R10 Shared device | Household of 3 | **Close** | A device link without any linked money flows is weak evidence |
| 6 | [ALT-00153](ALT-00153_structuring_escalate.md) | R01 Structuring | Administrative assistant | **Escalate, SAR** | Classic structuring: multiple branches, just under $10K, cash sent to another bank. Basis for **SAR 1** |
| 7 | [ALT-00120](ALT-00120_funnel_escalate.md) | R03 Funnel | Registered nurse | **Escalate** | Third-party cash in 6 states, wired to Mexico, Guatemala and China |
| 8 | [ALT-00256](ALT-00256_mule_escalate.md) | R08 Mule | 19-year-old tutor | **Escalate, SAR + network** | 198 victims, then the mule, then collectors and crypto. Basis for **SAR 2** |
| 9 | [ALT-00117](ALT-00117_tbml_escalate.md) | R07 TBML | Used-clothing importer | **Escalate + sanctions referral** | Goods mismatch, free-zone counterparties, third-party payers in evasion corridors |
| 10 | [ALT-00782](ALT-00782_dormant_escalate.md) | R06 Dormant | 76-year-old retiree | **Escalate (urgent)** | Possible elder financial exploitation or unwitting mule |

## How each disposition is structured
1. **Header:** alert, rule, customer, risk rating, analyst, decision.
2. **Why it fired:** the triggering transactions, shown as a table.
3. **Review performed:** the look-back period, the data sources checked, and simulated external checks.
4. **Analysis:** red flags weighed against mitigating factors.
5. **Decision and rationale:** written so that an examiner can follow the reasoning without asking the analyst.
6. **Follow-up:** SAR recommendation, KYC updates, and **tuning feedback** to the model owner.

The tuning feedback in the false-positive closures is how a monitoring program improves over time: L1 analysts are the people who see why a rule misfires.
