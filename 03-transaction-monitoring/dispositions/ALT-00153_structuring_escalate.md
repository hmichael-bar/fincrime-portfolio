# ALT-00153 | R01 Structuring | ESCALATE: Recommend SAR

> **Synthetic case.** All names, accounts and transactions are fictional. *[simulated]* = a check this project does not model. This case continues as **SAR Sample 1** in `../04-sar-narratives/`.

| Field | Value |
|---|---|
| Alert ID | ALT-00153 (related: 5 more R01/R09 alerts on the same customer, Feb to Jun) |
| Rule | R01: cash deposits of $8,000 to $9,999, 2 or more in 5 days, total ≥ $10,000 |
| Alert date | 2026-02-05 |
| Customer | C0298, Olivia Ali, individual, age 51, administrative assistant, NJ (home branch BR04, Hoboken) |
| KYC risk rating | Low. Expected cash activity: **Low**. Expected monthly volume: $11,300 |
| Analyst / date | L1-ANALYST-01 / 2026-07-07 |
| **Decision** | **Escalate to L2. Recommend SAR (structuring, 31 U.S.C. 5324)** |

## 1. Why the alert fired
Five cash deposits in three days, at three branches in two states:

| Txn | Date / time | Amount | Branch |
|---|---|---|---|
| T010336 | 2026-02-03 10:53 | $9,920.00 | BR07 Manhattan, NY |
| T010490 | 2026-02-03 14:55 | $9,900.00 | BR04 Hoboken, NJ |
| T011021 | 2026-02-05 09:04 | $9,690.00 | BR07 Manhattan, NY |
| T011081 | 2026-02-05 11:26 | $9,420.00 | BR06 Queens, NY |
| T011147 | 2026-02-05 13:57 | $9,000.00 | BR06 Queens, NY |
| **Total** | | **$47,930.00** | 3 branches |

## 2. Look-back (full 6 months)
The same pattern repeats three times. Each time the cash is pushed out to an account at another bank within days:

| Episode | Dates | Deposits | Total cash | Branches used | Outflow |
|---|---|---|---|---|---|
| 1 | Feb 3 to 5 | 5 | $47,930 | 3 | Feb 8: ACH $17,729.83 to "Self, ext. acct, Pinnacle Bank" |
| 2 | Apr 24 to 26 | 5 | $41,670 | 5 | Apr 29: ACH $29,568.32 to the same external account |
| 3 | Jun 11 to 14 | 4 | $36,740 | 4 | Jun 16: ACH $18,272.52 to the same external account |
| **Total** | | **14** | **$126,340** | **8 different branches** | **$65,570.67** |

- **Not one deposit reached $10,000**, so no CTR was ever filed.
- Every deposit is a round or near-round amount between $8,170 and $9,920.
- Her legitimate income is biweekly payroll of about $2,800 (13 credits, $36,588 over 6 months). Between episodes her account looks completely ordinary.

## 3. Red flags
1. Repeated cash deposits just under the $10,000 CTR threshold (FFIEC BSA/AML Manual, structuring red flags).
2. Several deposits on the same day at **different branches** (Feb 3: NY and NJ; Feb 5: two NY branches, three deposits). This is a classic way to stop any single teller from seeing the full amount.
3. Cash volume ($126K) is about **3.5x her annual payroll** for the period and inconsistent with an occupation that does not generate cash and an expected cash activity of "Low".
4. Quick transfer of the cash to another institution: possible layering, and it keeps balances low at this bank.
5. The pattern repeats at roughly two-month intervals, which suggests a deliberate routine rather than a one-off.

## 4. Mitigating factors considered
- Long-tenured customer (since 2010) with no prior alerts or SARs *[simulated]*.
- No source of the cash has been identified. No RFI was sent, to avoid **tipping off** the customer. A legitimate explanation (for example, sale of an asset) would not explain splitting the money across branches and days.

## 5. Decision and rationale
**Escalated.** The deposits are structured to stay under the CTR threshold, spread across multiple branches and days, in a pattern that repeats three times and totals $126,340, with the money then sent out to another bank. Structuring is a crime under 31 U.S.C. 5324 even if the cash itself comes from a legitimate source. The activity has no apparent lawful purpose given the customer's profile. A SAR is recommended.

## 6. Recommendations to L2
- File a SAR covering 2026-02-03 to 2026-06-16. The 30-day filing clock starts when L2 confirms the activity is suspicious.
- Send a 314(b) request to Pinnacle Bank (the receiving institution) if both banks participate *[simulated]*.
- Pull teller video and deposit-slip details for the 14 deposits, to check whether a third party made any of them.
- Flag the account for enhanced monitoring. The relationship manager must **not** tell the customer about the review (SAR confidentiality, 31 U.S.C. 5318(g)(2)).
