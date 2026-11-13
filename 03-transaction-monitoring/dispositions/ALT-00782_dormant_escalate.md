# ALT-00782 | R06 Dormant Account Reactivation | ESCALATE: Possible Elder Exploitation / Mule Use

> **Synthetic case.** All names, accounts and transactions are fictional. *[simulated]* = a check this project does not model.

| Field | Value |
|---|---|
| Alert ID | ALT-00782 (related: R02, R04, R09 alerts on the same customer, May and Jun) |
| Rule | R06: 90 or more days without activity, then ≥ $15,000 within 30 days |
| Alert date | 2026-06-19 |
| Customer | C0479, Kwame Mansour, individual, **age 76, retired**, NJ (branch BR03, Paterson) |
| KYC | Account opened 2013-01-06. Expected monthly volume $3,200. Domestic only. Low risk. Income: Social Security and a small pension |
| Analyst / date | L1-ANALYST-01 / 2026-07-06 (prioritised: possible elder exploitation) |
| **Decision** | **Escalate. Suspicious reactivation; possible elder financial exploitation or account used as a mule** |

## 1. Why the alert fired
The account was **dormant for 301 days** (last activity 2025-07-24). On 2026-05-21 it suddenly started receiving large international wires that were turned into crypto and cash within days:

| Txn | Date | Type | Amount | Counterparty | Country |
|---|---|---|---|---|---|
| T044989 | May 21 | Wire in | $36,193.24 | Quick Funds Transfer Co | UAE |
| T045268 | May 22 | **Crypto buy** | $32,573.91 | SatoshiPay Kiosk | US |
| T047309 | May 28 | Cash deposit | $9,800.00 | BR03 | |
| T047392 | May 29 | Wire in | $22,336.17 | Orion Asset Partners Ltd | UAE |
| T047597 | May 29 | **Crypto buy** | $8,820.00 | BlockVault Markets | US |
| T048062 | May 31 | Teller cash withdrawal | $9,500.00 | BR03 | |
| T051115 | Jun 8 | Wire in | $77,527.80 | Orion Asset Partners Ltd | UAE |
| T051485 | Jun 9 | Wire out | $73,651.41 | Danube Reliance Trading | **Turkey** |

**Totals:** $136,057 in by international wire plus $9,800 in cash. Out: $41,394 to crypto, $73,651 by wire to Turkey, $9,500 in cash. Monthly volume was roughly **40 to 50x** his expected $3,200.

## 2. Review performed
- Full history, including the period before the dormancy (low-value pension and Social Security activity only).
- Social Security and pension credits resumed in June alongside the new activity. The account still holds the customer's benefits, so it is not being used purely by an outsider.
- Online-banking device DEV-393698 was used for the crypto purchases and the Turkey wire. It is the customer's registered device, but session details (IP address, location, any recent change of phone number or email) need to be checked *[simulated]*.
- Negative news and sanctions screening on all three foreign counterparties: no hits *[simulated]*. The names are generic and the counterparties have no visible business connection to the customer.

## 3. Red flags
1. Long-dormant account suddenly reactivated with high-value international wires (FFIEC dormant-account red flag).
2. **Pass-through:** each inbound wire is followed within 1 to 2 days by a crypto purchase, cash withdrawal or onward wire.
3. Elderly customer with a fixed income and no declared international ties receiving money from UAE "asset" and "funds transfer" companies with no stated purpose.
4. Patterns consistent with **elder financial exploitation** (FinCEN Advisory FIN-2022-A002): an older person either victimised (scammers send "investment returns" or "refunds", then direct the person to buy crypto) or recruited as an unwitting mule through a romance or lottery scam.
5. Teller withdrawal of $9,500 and a cash deposit of $9,800: both just under $10,000.

## 4. Decision and rationale
**Escalated.** The reactivation activity has no apparent economic purpose, conflicts sharply with the customer's profile, and moves foreign funds quickly into crypto, cash and a third-country wire. Whether the customer is a victim or a participant, the activity requires investigation and probably a SAR. The elder-exploitation angle makes it urgent, because further losses may be preventable.

## 5. Recommendations to L2
- **Urgent:** contact the customer through the phone number on file (not any newly added number) to check that he knows about the activity and is safe. Follow the bank's elder-abuse procedure, including a possible report to Adult Protective Services. Do not mention that a SAR may be filed.
- Consider a temporary hold on outgoing wires and crypto purchases under the bank's policy and any applicable state hold laws for senior customers.
- Review recent changes to the account (address, phone, email, online-banking enrolment).
- Decide on a SAR. If filed, include the elder-financial-exploitation key term the FinCEN advisory asks for ("EFE FIN-2022-A002") in the narrative.
