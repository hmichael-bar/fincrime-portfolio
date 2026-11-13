# ALT-00132 | R02 Rapid Movement of Funds | CLOSE: False Positive

> **Synthetic case.** All names, accounts and transactions are fictional. *[simulated]* = a check this project does not model.

| Field | Value |
|---|---|
| Alert ID | ALT-00132 |
| Rule | R02: credit ≥ $20,000 with ≥ 80% leaving within 3 days |
| Alert date | 2026-01-31 |
| Customer | C0432, Karim Clark, individual, age 65, rideshare driver, NJ |
| KYC risk rating | Low |
| Analyst / date | L1-ANALYST-01 / 2026-07-06 |
| **Decision** | **Close: false positive. A documented vehicle sale and purchase** |

## 1. Why the alert fired
| Txn | Date | Type | Amount | Counterparty | Memo |
|---|---|---|---|---|---|
| T008498 | 2026-01-29 | ACH in | $34,097.31 | AutoBid Online Car Buyer (US) | VEHICLE PURCHASE PAYOUT |
| T009056 | 2026-01-31 | Wire out | $38,613.68 | Route 17 Auto Mall (US) | VEHICLE PURCHASE |

Outflows within 3 days were 114% of the credit.

## 2. Customer profile (KYC)
Rideshare driver, account opened 2024-02-29, expected monthly volume $7,300, domestic only. His usual activity is weekly platform payouts and many small P2P receipts from riders and clients.

## 3. Review performed
- Six months of activity, the counterparties on both legs, and his balance before and after.
- Related alert R09 (January volume 5x expected), which comes from the same two transactions.
- Negative news on the counterparties: none *[simulated]*. Both are domestic auto-sector businesses.

## 4. Analysis
- **Economic purpose is clear.** The credit comes from an online car-buying platform and the memo says it is a vehicle payout. The debit two days later goes to an auto dealer, also with a vehicle memo. In other words, he sold one car and bought another.
- **It fits his occupation.** For a rideshare driver the vehicle is the tool of the trade, and replacing it is an expected one-off event.
- **His own money covers the difference.** The outgoing wire is about $4,500 larger than the incoming credit, and existing balance covered the gap. Laundering pass-throughs usually skim a fee and forward less, not more.
- **There is no third party, foreign party or layering.** Both counterparties are US businesses, and nothing else unusual happened before or after.
- February to June: his activity returns to baseline (about $4K a month in and out).

## 5. Decision and rationale
Closed as a false positive, and related alert R09 for January is closed for the same reason. The rapid movement is one vehicle trade-in transaction with a clear lawful purpose, consistent with the customer's occupation, involving only domestic commercial counterparties. There is no pattern.

## 6. Follow-up
- No SAR. No KYC change, since this is a one-off event.
- **Tuning feedback:** R02 fires on large one-off consumer purchases (cars, home closings). Consider a whitelist of counterparty categories (title companies, auto dealers, brokerages the customer already uses) that lowers the score instead of suppressing the alert.
