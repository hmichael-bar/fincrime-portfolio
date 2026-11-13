# ALT-00036 | R04 High-Risk Jurisdiction Wire | CLOSE: False Positive (after RFI)

> **Synthetic case.** All names, accounts and transactions are fictional. *[simulated]* = a check this project does not model. The RFI answer below is invented for illustration.

| Field | Value |
|---|---|
| Alert ID | ALT-00036 |
| Rule | R04: wires to or from FATF grey/black-list or corridor countries |
| Alert date | 2026-01-15 |
| Customer | C0064, Fatima Rivera, individual, age 56, bus operator, NY |
| KYC risk rating | Low |
| Analyst / date | L1-ANALYST-01 / opened 2026-07-07, closed 2026-07-14 after RFI |
| **Decision** | **Close: false positive. A one-off family support payment, explained and documented** |

## 1. Why the alert fired
| Txn | Date | Type | Amount | Counterparty | Country | Memo |
|---|---|---|---|---|---|---|
| T004008 | 2026-01-13 | ACH in | $31,842.73 | Own Savings, Pinnacle Bank | US | TRANSFER FROM SAVINGS |
| T004547 | 2026-01-15 | Wire out | $30,183.09 | Rosa Ibrahim (individual) | **Haiti** | FAMILY SUPPORT - HURRICANE |

Haiti was on the FATF list of jurisdictions under increased monitoring (the "grey list") in this project's reference snapshot. The customer's KYC profile shows no expected international activity.

## 2. Review performed
- Six months of activity, and the source of funds for the wire.
- **Sanctions screening** of the beneficiary name against OFAC SDN and consolidated lists: no match *[simulated]*. A grey listing is not a sanction. Haiti does have OFAC designations of individuals (gang leaders and their financiers), so screening the beneficiary is required, not optional.
- Negative news on the beneficiary: none *[simulated]*.
- Request for information (RFI) through the branch *[simulated]*. The customer said the beneficiary is her sister, and the money paid for roof and wall repairs to the family home after storm damage. She provided the contractor's estimate and a photo of the transfer receipt.

## 3. Analysis
| Factor | Assessment |
|---|---|
| Source of funds | Traceable. The money came from her own savings account at another US bank 2 days earlier, not from cash or unknown third parties. |
| Pattern | A single wire. There were no other international wires before or after, and no splitting into smaller amounts. |
| Beneficiary | An individual family member, not a business, exchange house or shell company. |
| Proportionality | $30K is large for her income, but it is consistent with spending savings on a family emergency. Her other activity (payroll, rent, utilities) is unchanged. |
| Narrative fit | The memo, the RFI answer and the documents agree with each other. |

## 4. Decision and rationale
Closed as a false positive. This is a single, self-funded family-support wire whose purpose is documented. There was no sanctions match and no pattern of high-risk-jurisdiction activity. The grey-list exposure is explained.

## 5. Follow-up
- No SAR. RFI response and documents saved to the case file.
- **KYC update requested:** add Haiti (family remittances) to the expected countries, so that any future recurring support payments are judged against an accurate profile.
