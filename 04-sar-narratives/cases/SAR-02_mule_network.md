# SAR Sample 2: Money Mule Account Feeding a Collector Network

> ⚠️ **FICTIONAL / SYNTHETIC.** The subjects, the bank (Meridian Harbor Bank) and all transactions come from the synthetic dataset in `../03-transaction-monitoring` (customers C0221, C0057 and C0106; alert ALT-00256). Investigative facts marked *[simulated]* are invented to show the process. This is not a real filing.

## 1. Case summary

| Field | Value |
|---|---|
| Case number | MHB-FIU-2026-0419 |
| Filing type | Initial report |
| Source | TM alert ALT-00256 (R08 money mule), with R10 shared-device alerts. Escalated by L1 on 07/08/2026 |
| Subject 1 | Olivia Moore, age 19, tutor, El Paso, TX. Account MHB63896470, opened 01/09/2026 |
| Subject 2 | Leila Khan, age 31, tutor, FL. Account opened 11/06/2025 (collector) |
| Subject 3 | Rosa Farouk, age 36, rideshare driver, NY. Account opened 11/10/2025 (collector) |
| Activity period | 02/22/2026 to 06/30/2026 |
| Amount | **$494,634.70** received by Subject 1 from 198 individuals. Downstream amounts are listed in Section 4 |
| SAR categories | Fraud: consumer fraud / mass-marketing scam proceeds. Money laundering: suspicious receipt of funds from multiple unrelated parties; funds transfers with no apparent economic purpose. Other: account appears to be used as a funnel or mule account |
| SAR filed | 07/29/2026 (L2 determination on 07/17/2026) |
| Related | 7 further linked accounts reported in separate SARs *[simulated]* |

**In one paragraph:** a 19-year-old customer opened an account in January 2026. From 02/22/2026 it received 198 payments from 198 different people, totalling $494,635, with memos typical of scam victims ("crypto profit release fee", "tax release fee", "romance - for you"). Most of each payment left within a day:
- $207,030 went by P2P to two other MHB customers;
- $132,581 went to crypto exchanges and kiosks;
- $45,495 was withdrawn in cash.

The two recipients, the collectors, also took in money from seven more young, recently opened accounts. All ten accounts are run from three shared phones. The collectors sent $1.18 million by wire to Hong Kong and the UAE and bought $381,000 in crypto.

## 2. Red flags
1. New account (opened 01/09/2026) with a sudden change in activity from 02/22/2026.
2. Many unrelated senders (198 people, each paying once) against an expected $6,600 a month. Monthly inflows reached $159,723 in June.
3. Memos consistent with advance-fee, investment, rental and romance scams.
4. Fast pass-through: about 78% of inflows left the account, mostly within 1 day, through a small set of channels (two people, three crypto venues, cash).
5. Device DEV-M00001 is shared with three other customers, including Collector Leila Khan.
6. Collectors with incomes inconsistent with the amounts, who send money to trading companies in Hong Kong and the UAE with the memo "GOODS".

## 3. Investigation steps taken
| # | Step | Result |
|---|---|---|
| 1 | Reviewed the alert and full account history | Change of behaviour on 02/22/2026 (Table 1) |
| 2 | Analysed inbound senders and memos | 198 unique senders; scam-type memos (Table 2) |
| 3 | Traced outbound funds | Two collector accounts at MHB, three crypto venues, ATM cash (Table 3) |
| 4 | Linked accounts by device and P2P flows | Network of 10 accounts on 3 devices (Table 4) |
| 5 | Reviewed the collectors' activity | Inflows from 8 mule accounts; wires to HK and UAE; crypto (Table 5) |
| 6 | Checked fraud claims *[simulated]* | 11 victim reports from other banks name Subject 1's account as the recipient |
| 7 | Reviewed onboarding *[simulated]* | Accounts opened online within minutes of each other from the same IP range |
| 8 | Sanctions and negative-news screening *[simulated]* | No sanctions match. Beneficiaries have no web presence |
| 9 | Coordinated with the Fraud team | Outgoing payments restricted; victim refunds under review; relationships referred for exit |

## 4. Supporting transactions
Full CSVs are in `../supporting_data/` (all files starting `SAR-02_`).

**Table 1: Subject 1 monthly flow from 02/22/2026**

| Month | In from individuals | Senders | To collectors | Crypto | Cash |
|---|---|---|---|---|---|
| Feb 2026 | $21,705.31 | 11 | $14,941.97 | $0.00 | $3,000.00 |
| Mar 2026 | $120,148.52 | 49 | $64,097.12 | $21,357.38 | $12,960.68 |
| Apr 2026 | $78,759.98 | 35 | $26,790.26 | $28,432.70 | $8,534.51 |
| May 2026 | $114,297.63 | 46 | $51,583.18 | $28,128.16 | $6,000.00 |
| Jun 2026 | $159,723.26 | 57 | $49,617.41 | $54,663.08 | $15,000.00 |
| **Total** | **$494,634.70** | **198** | **$207,029.94** | **$132,581.32** | **$45,495.19** |

**Table 2: inbound memos.** Shipping fee 25; rent deposit 24; gift 21; invoice 21; investment 21; loan repayment 19; blank 18; tax release fee 17; crypto profit release fee 16; "romance - for you" 14; lesson 2.

Sample of the first payments:

| Txn | Date | Type | Amount | Sender | Memo |
|---|---|---|---|---|---|
| T016353 | 02/22/2026 | P2P in | $3,042.19 | Emily Williams | rent deposit |
| T016431 | 02/22/2026 | P2P in | $1,667.92 | Emily Gonzalez | gift |
| T016939 | 02/24/2026 | ACH in | $2,958.22 | Marcus Ibrahim | gift |
| T017348 | 02/25/2026 | P2P in | $3,461.15 | David Rivera | loan repayment |
| T017428 | 02/25/2026 | P2P in | $1,492.87 | Amira Jackson | crypto profit release fee |
| T017706 | 02/26/2026 | ACH in | $4,672.65 | Hye-jin Ali | gift |

**Table 3: where Subject 1's money went** (payments of $1,000 or more)

| Channel | Recipient | Count | Amount |
|---|---|---|---|
| P2P | Leila Khan (Subject 2) | 17 | $108,659.63 |
| P2P | Rosa Farouk (Subject 3) | 17 | $98,370.31 |
| Crypto | SatoshiPay Kiosk | 7 | $50,809.56 |
| Crypto | BlockVault Markets | 10 | $45,826.23 |
| Crypto | CoinHarbor Exchange | 7 | $35,945.53 |
| Cash | ATM, El Paso TX | 16 | $45,495.19 |

**Table 4: linked accounts**

| Customer | Age | Occupation | State | Opened | Device |
|---|---|---|---|---|---|
| C0057 Leila Khan (collector) | 31 | Tutor | FL | 11/06/2025 | DEV-M00001 |
| C0106 Rosa Farouk (collector) | 36 | Rideshare driver | NY | 11/10/2025 | DEV-M00002 |
| C0221 Olivia Moore | 19 | Tutor | TX | 01/09/2026 | DEV-M00001 |
| C0317 Carlos Reyes | 20 | Freelance photographer | NY | 01/11/2026 | DEV-M00001 |
| C0484 Maria Scott | 21 | Student | NJ | 12/18/2025 | DEV-M00001 |
| C0255 Rachel Sanchez | 19 | Unemployed | NJ | 11/20/2025 | DEV-M00002 |
| C0416 Elena Miller | 23 | Student | NY | 10/24/2025 | DEV-M00002 |
| C0197 Hector Johnson | 23 | Student | NY | 01/31/2026 | DEV-M00003 |
| C0316 Andre Ortiz | 20 | Student | AZ | 02/05/2026 | DEV-M00003 |
| C0454 Ines Nguyen | 24 | Freelance designer | NJ | 10/14/2025 | DEV-M00003 |

**Table 5: collectors**

| | Leila Khan (C0057) | Rosa Farouk (C0106) |
|---|---|---|
| P2P received from the 8 linked accounts | 136 payments, $785,289.16 | 142 payments, $898,948.65 |
| Wires to Golden Crest General Trading LLC (UAE) | 21, $300,419.09 | 13, $230,545.21 |
| Wires to Kowloon Bayview Ltd (Hong Kong) | 15, $242,688.50 | 21, $405,892.65 |
| Crypto purchases | 39, $178,658.59 | 36, $202,333.19 |

## 5. SAR narrative (Part V)

> Meridian Harbor Bank (MHB) is filing this SAR to report suspected money mule activity and the laundering of probable fraud proceeds involving three MHB customers: Olivia Moore (Subject 1), Leila Khan (Subject 2) and Rosa Farouk (Subject 3). Between 02/22/2026 and 06/30/2026, Subject 1's personal checking account MHB63896470 received $494,634.70 in 198 P2P and ACH payments from 198 different individuals. Most of these funds were forwarded within one day to Subjects 2 and 3, to cryptocurrency platforms, or withdrawn in cash. Subjects 2 and 3 received a further $1,684,237.81 from Subject 1 and seven other recently opened MHB accounts, and sent the funds abroad by wire and to cryptocurrency platforms. The activity was identified through transaction monitoring alert ALT-00256 and a review of all linked accounts. Some inbound payments reference cryptocurrency investment fees (FIN-2023-PIGBUTCHERING).
>
> Subject 1, age 19, opened the account online on 01/09/2026, stating she was a tutor with expected activity of about $6,600 a month. Until 02/21/2026 the account received only small tutoring payments and weekly payouts from TaskHub Inc. Starting on 02/22/2026 it received payments from individuals with no apparent connection to the subject, usually between $250 and $4,800, with memos including "shipping fee," "rent deposit," "investment," "tax release fee," "crypto profit release fee" and "romance - for you." Monthly inflows rose from $21,705.31 in February to $159,723.26 in June 2026. MHB received 11 fraud claims from other financial institutions identifying the account as the recipient of payments from scam victims.
>
> Subject 1 forwarded the funds almost immediately. Between 02/23/2026 and 06/30/2026 she sent 17 P2P payments totalling $108,659.63 to Subject 2 and 17 P2P payments totalling $98,370.31 to Subject 3, bought $132,581.32 in cryptocurrency through SatoshiPay Kiosk, BlockVault Markets and CoinHarbor Exchange, and made 16 ATM withdrawals totalling $45,495.19 in El Paso, TX. For example, she received $3,042.19 and $1,667.92 on 02/22/2026 and sent $4,108.79 to Subject 3 on 02/23/2026.
>
> Subject 1's online banking was accessed from a mobile device also used by Subject 2 and two other MHB customers. Subjects 2 and 3 are linked by device and payment flows to seven other accounts opened between 10/14/2025 and 02/05/2026, mostly held by students aged 19 to 24. Between 02/02/2026 and 06/29/2026, Subject 2 received 136 P2P payments totalling $785,289.16 from these accounts. Between 01/30/2026 and 06/29/2026, Subject 3 received 142 payments totalling $898,948.65 from them. Subject 2, a tutor, sent 36 wires totalling $543,107.59 to Golden Crest General Trading LLC (United Arab Emirates) and Kowloon Bayview Ltd (Hong Kong) with the memo "GOODS," and bought $178,658.59 in cryptocurrency. Subject 3, a rideshare driver, sent 34 wires totalling $636,437.86 to the same two companies and bought $202,333.19 in cryptocurrency. MHB found no business relationship explaining these payments.
>
> The volume of payments from unrelated individuals, the scam-related memos, the victim fraud claims, the immediate onward transfer of funds, the shared devices and the account holders' stated occupations indicate that the accounts were used to collect and launder fraud proceeds. MHB has restricted outgoing payments on all linked accounts, is processing victim claims, and intends to close the relationships. Related SARs are being filed on the other linked account holders. Supporting documentation is retained by MHB and is available to law enforcement on request. Contact: MHB BSA/AML Investigations, case MHB-FIU-2026-0419.

## 6. Why this narrative works
- It names **each subject's role** (mule or collector), so a reader can follow the flow of money.
- **The scam is explained by facts** (the memos and the victim claims). The narrative does not try to name the specific fraudster.
- **Amounts are traced all the way through:** from victims, to the mule, to the collectors, to offshore wires and crypto.
- It **names the beneficiaries abroad**, which helps law enforcement work with foreign financial intelligence units.
- It **states the actions taken** (restrictions, related SARs) and makes **no mention of the customer being contacted**.
