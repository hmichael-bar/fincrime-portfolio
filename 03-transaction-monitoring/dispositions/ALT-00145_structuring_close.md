# ALT-00145 | R01 Structuring | CLOSE: False Positive

> **Synthetic case.** Customer, bank and transactions are fictional (Meridian Harbor Bank, synthetic dataset). Checks marked *[simulated]* are things a real analyst would do in internal systems that this project does not model.

| Field | Value |
|---|---|
| Alert ID | ALT-00145 |
| Rule | R01: cash deposits $8,000 to $9,999, 2 or more in 5 days, total ≥ $10,000 |
| Alert date | 2026-02-02 |
| Customer | C0104, Cohen Deli LLC (business). Beneficial owner: Elena Cohen |
| KYC risk rating | High (cash-intensive business) |
| Analyst / date | L1-ANALYST-01 / 2026-07-06 |
| **Decision** | **Close: false positive. Activity is consistent with the customer's business** |

## 1. Why the alert fired
Two cash deposits at the home branch (BR02, Newark NJ) on consecutive days:

| Txn | Date | Type | Amount | Branch | Memo |
|---|---|---|---|---|---|
| T009490 | 2026-02-01 | Cash deposit | $9,802.05 | BR02 | DAILY RECEIPTS |
| T010090 | 2026-02-02 | Cash deposit | $9,120.77 | BR02 | DAILY RECEIPTS |

Total $18,922.82: both deposits are below the $10,000 CTR threshold, and together they exceed it.

## 2. Customer profile (KYC)
- Deli / bodega, account opened 2011-10-04 (more than 14 years of relationship).
- Expected cash activity: **High**. Expected monthly volume: $440,300.
- No international activity expected and none seen.

## 3. Review performed
- Six months of activity (Jan to Jun 2026), all transaction types.
- Distribution of cash deposit amounts, branch usage and timing.
- Prior alerts and dispositions on the customer: one other alert (R02, related to card-settlement timing). No prior SARs *[simulated]*.
- CTR history *[simulated, derived from data]*: the customer regularly deposits over $10,000.

## 4. Analysis
| Question | Finding |
|---|---|
| Does the customer avoid the $10K threshold? | **No.** In 6 months the customer made **21 cash deposits of $10,000 or more** (total $280,979), each of which would generate a CTR. People who are structuring avoid CTRs, and this customer triggers them every few weeks. |
| Are the amounts engineered? | No. The amounts include cents ($9,802.05, $9,120.77) and the median deposit is $6,097. Structured deposits are usually round or just-under amounts such as $9,500 or $9,900. Only 11 of 105 deposits fell in the $8K to $10K band, which is about what the business's normal spread of deposit sizes would produce. |
| Multiple branches? | No. All 105 deposits were made at the home branch, BR02. |
| Consistent with profile? | Yes. Monthly credits ran $168K to $233K against an expected $440K of total monthly volume. The card-processor settlements, supplier payments, payroll and sales tax payments all fit an operating food retailer. |
| Weekend timing | 1 Feb 2026 is a Sunday. Weekend receipts deposited on Sunday and Monday are normal for a deli. |

**Red flags present:** two sub-$10K cash deposits in 2 days.
**Mitigating factors:** frequent over-threshold deposits (CTRs are being filed), non-round amounts, single home branch, long relationship, activity consistent with KYC.

## 5. Decision and rationale
Closed as a false positive. The deposits reflect the normal day-to-day variation in the cash receipts of a high-volume deli. The customer does not avoid currency reporting. Over the review period it made 21 deposits that generated CTRs. There is no indication of structuring under 31 U.S.C. 5324.

## 6. Follow-up
- No SAR. No KYC update needed.
- **Tuning feedback:** R01 produces repeat false positives on cash-intensive businesses whose deposits often exceed $10K. Proposal: suppress R01 when the customer had 2 or more CTR-reportable deposits in the prior 30 days, or score R01 against the customer's own deposit distribution.
