# ALT-00027 | R07 Trade-Based ML: Invoice Pattern | CLOSE: False Positive

> **Synthetic case.** All names, accounts and transactions are fictional. *[simulated]* = a check this project does not model.

| Field | Value |
|---|---|
| Alert ID | ALT-00027 |
| Rule | R07: invoice-referenced wires meeting at least 2 of: free-zone/high-risk counterparty, goods inconsistent with KYC, identical repeated amounts, third-party payer |
| Alert date | 2026-01-11 |
| Customer | C0043, Wilson International LLC, textile importer, CA |
| KYC risk rating | High (import/export) |
| Analyst / date | L1-ANALYST-01 / 2026-07-07 |
| **Decision** | **Close: false positive. A declared supplier and declared goods, under a standing order** |

## 1. Why the alert fired
| Txn | Date | Type | Amount | Counterparty | Country | Memo |
|---|---|---|---|---|---|---|
| T003378 | 2026-01-11 | Wire out | $36,865.64 | Saigon Garment JSC | Vietnam | INV-4724 textiles |

Conditions met: (1) Vietnam is on the grey list in the reference snapshot, and (2) the identical amount of $36,865.64 recurs.

## 2. Customer profile (KYC)
- Textile importer, account opened 2021-10-11. Expected goods: **textiles**.
- Expected countries: **China, Turkey, Vietnam**. Expected monthly volume: $474,800.

## 3. Review performed
- All 19 outgoing wires over 6 months, by supplier, amount and memo.
- Incoming flows: 53 ACH credits from US retail and distributor buyers ($857,939).
- Comparison of suppliers against KYC; sanctions screening of the supplier: no match *[simulated]*.

## 4. Analysis
| R07 condition | Finding |
|---|---|
| High-risk counterparty | Vietnam is a declared supplier country, and Saigon Garment JSC is a supplier documented at onboarding. Vietnam is also one of the world's largest garment exporters, so a textile importer paying there is expected. |
| Goods mismatch | **None.** The memo says textiles, which matches KYC. |
| Repeated identical amount | $36,865.64 appears 9 times across all three declared suppliers (China ×3, Turkey ×4, Vietnam ×2). This is a fixed contract price per container order, not unusual for a standing purchase agreement. In TBML the warning sign is a repeated amount with no link to goods or quantity, often paid by third parties. That is not the case here. |
| Third-party payments | None. Buyers are US businesses paying by ACH, and the customer pays its suppliers directly. |
| Volume | Outgoing supplier wires ($852K over 6 months) are funded by customer receipts ($858K), which fits a functioning trading business. |

## 5. Decision and rationale
Closed as a false positive. The wire goes to a supplier and country documented in KYC, for goods matching the customer's line of business. The repeated amount is explained by standing-order pricing, and no third-party funding is involved.

## 6. Follow-up
- No SAR.
- **Tuning feedback:** R07's "high-risk counterparty" condition should not count grey-list countries that are already in the customer's KYC profile for the same goods. That one change would have prevented this alert and most of R07's 26 false-positive alerts in this run.
- Sample check at the next periodic review: obtain one invoice and bill of lading for a $36,865.64 payment, to confirm that quantity and unit price match the market.
