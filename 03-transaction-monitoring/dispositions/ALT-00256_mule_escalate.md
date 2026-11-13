# ALT-00256 | R08 Money Mule Activity | ESCALATE: Recommend SAR + Network Review

> **Synthetic case.** All names, accounts and transactions are fictional. *[simulated]* = a check this project does not model. This case continues as **SAR Sample 2** in `../04-sar-narratives/`.

| Field | Value |
|---|---|
| Alert ID | ALT-00256 (related: R09/R10 alerts on the same customer; R08/R10 alerts on linked customers) |
| Rule | R08: 10 or more distinct inbound senders in a month, ≥ 80% moved out, plus a secondary indicator (new account / crypto / shared device) |
| Alert date | 2026-02-28 |
| Customer | C0221, Olivia Moore, individual, **age 19**, tutor, TX (branch BR10, El Paso) |
| Account opened | **2026-01-09** (50 days before the alert) |
| KYC risk rating | Low. Expected monthly volume: $6,600 |
| Analyst / date | L1-ANALYST-01 / 2026-07-08 |
| **Decision** | **Escalate. Probable money mule account; network of linked accounts identified** |

## 1. Why the alert fired
February 2026: **24 distinct senders** paid in $25,725 and 80% left the account the same month. The account was 50 days old, and its registered phone (**DEV-M00001**) is shared with **3 other customers**.

The change happened on **Feb 22**. Before that date the account received only small tutoring payments ($31 to $241) and a weekly TaskHub payout. From Feb 22 onward, unrelated people sent $1,000 to $4,700 at a time, with memos such as *"crypto profit release fee"*, *"rent deposit"*, *"gift"* and *"loan repayment"*. The money was forwarded within a day:

| Txn | Date | Type | Amount | Counterparty | Memo |
|---|---|---|---|---|---|
| T016353 | Feb 22 | P2P in | $3,042.19 | Emily Williams | rent deposit |
| T016431 | Feb 22 | P2P in | $1,667.92 | Emily Gonzalez | gift |
| T016862 | Feb 23 | **P2P out** | **$4,108.79** | **Rosa Farouk (bank customer C0106)** | |
| T016939 | Feb 24 | ACH in | $2,958.22 | Marcus Ibrahim | gift |
| T017298 | Feb 25 | **P2P out** | **$4,522.27** | **Leila Khan (bank customer C0057)** | |
| T017348 | Feb 25 | P2P in | $3,461.15 | David Rivera | loan repayment |
| T017428 | Feb 25 | P2P in | $1,492.87 | Amira Jackson | crypto profit release fee |
| T017667 | Feb 26 | **P2P out** | **$6,310.91** | **Leila Khan (C0057)** | |
| T017706 | Feb 26 | ACH in | $4,672.65 | Hye-jin Ali | gift |
| T017734 | Feb 26 | ATM withdrawal | $3,000.00 | BR10 El Paso | |

## 2. Look-back (Feb 22 to Jun 30)
| Measure | Value |
|---|---|
| Inbound payments of $250 or more from individuals | **198 payments from 198 different people**, $494,635 |
| Sent to Leila Khan (C0057) | 17 P2P, $108,660 |
| Sent to Rosa Farouk (C0106) | 17 P2P, $98,370 |
| Crypto purchases (3 exchanges / kiosks) | 24, $132,581 |
| ATM cash withdrawals | 16, $45,495 |
| Monthly volume vs KYC expected | Up to about 25x ($163K in during June vs $6.6K expected) |

Memo mix on inbound payments: shipping fee (25), rent deposit (24), gift (21), invoice (21), investment (21), loan repayment (19), tax release fee (17), crypto profit release fee (16), "romance - for you" (14). **These memos read like messages from scam victims** (advance-fee, investment, romance and rental scams), not like payment for tutoring.

## 3. Network
The shared-device link and the P2P flows tie this account to 9 other customers:

| Device | Customers |
|---|---|
| DEV-M00001 | **C0057 Leila Khan** (collector), C0221 Olivia Moore, C0317 Carlos Reyes, C0484 Maria Scott |
| DEV-M00002 | **C0106 Rosa Farouk** (collector), C0255 Rachel Sanchez, C0416 Elena Miller |
| DEV-M00003 | C0197 Hector Johnson, C0316 Andre Ortiz, C0454 Ines Nguyen |

All 10 accounts were opened between Oct 2025 and Feb 2026. The two "collector" accounts receive P2P from several of the others and send money on through **international wires (Hong Kong, UAE) and crypto purchases**. The structure is fan-in from victims, then mule accounts, then collectors, then offshore and crypto.

## 4. Red flags (FinCEN / FBI money-mule indicators)
1. New account (under 60 days old) with a sudden surge of incoming payments from many unrelated individuals.
2. Fast pass-through: most money leaves within 1 day, by P2P to a small set of recipients, crypto purchases or ATM cash.
3. Inbound memos consistent with fraud-victim payments.
4. Several customers controlled from the same device.
5. Volume far above what is expected for a 19-year-old part-time tutor.

## 5. Decision and rationale
**Escalated.** The account is acting as a money mule: it receives probable fraud proceeds from many victims and forwards them to collector accounts and crypto. The account holder may be a willing participant or recruited and unwitting (for example through a fake job offer). Either way, the activity is suspicious and must be reported. The linked accounts should be investigated as one network.

## 6. Recommendations to L2
- **One network case** covering the 10 linked customers. SARs for each subject, or a joint SAR that lists all subjects.
- Coordinate with the fraud team: consider freezing outgoing payments and recalling or returning funds to identifiable victims, according to bank policy.
- Review account opening for C0221 (ID documents, IP address, onboarding device) for possible synthetic or borrowed identity *[simulated]*.
- Consider exiting the relationships after the SAR decision. Do not tip off the customer.
