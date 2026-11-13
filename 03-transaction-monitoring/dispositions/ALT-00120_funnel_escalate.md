# ALT-00120 | R03 Funnel Account | ESCALATE to L2

> **Synthetic case.** All names, accounts and transactions are fictional. *[simulated]* = a check this project does not model.

| Field | Value |
|---|---|
| Alert ID | ALT-00120 (related: 11 more R03/R09 alerts, Feb to Jun) |
| Rule | R03: cash deposits in 3 or more states outside the home state within a month, total ≥ $10,000 |
| Alert date | 2026-01-31 |
| Customer | C0114, Sofia Mensah, individual, age 64, registered nurse. Home: NJ (branch BR03, Paterson) |
| KYC risk rating | Low. Expected monthly volume: $13,100. Expected cash: Low. No international activity expected |
| Analyst / date | L1-ANALYST-01 / 2026-07-08 |
| **Decision** | **Escalate to L2. Funnel account indicators; recommend SAR consideration** |

## 1. Why the alert fired
Between Jan 15 and Jan 31, 2026: **11 cash deposits in 5 states**, none of them her home state, totalling **$46,324**:

| Txn | Date | Amount | Branch (state) |
|---|---|---|---|
| T004655 | Jan 15 | $3,864.68 | BR18 Chicago (IL) |
| T004851 | Jan 16 | $6,344.17 | BR17 Atlanta (GA) |
| T005599 | Jan 18 | $2,237.77 | BR10 El Paso (TX) |
| T005948 | Jan 20 | $6,148.57 | BR11 Phoenix (AZ) |
| T005962 | Jan 20 | $4,407.16 | BR14 San Diego (CA) |
| T006626 | Jan 22 | $5,691.54 | BR09 Houston (TX) |
| T007454 | Jan 25 | $4,588.49 | BR14 San Diego (CA) |
| T008426 | Jan 29 | $4,335.76 | BR09 Houston (TX) |
| T008642 | Jan 29 | $4,579.31 | BR18 Chicago (IL) |
| T008813 | Jan 30 | $2,186.69 | BR12 Tucson (AZ) |
| T008945 | Jan 31 | $1,939.71 | BR09 Houston (TX) |

The Jan 20 deposits were made in Phoenix and San Diego **27 minutes apart**, about 350 miles from each other, so one person cannot have made both. Different people are depositing into her account.

## 2. Look-back (6 months)
**Cash in:** 117 deposits, $462,022, made **only** at out-of-state branches:

| State | Deposits | Amount |
|---|---|---|
| TX | 23 | $97,672 |
| FL | 22 | $97,153 |
| IL | 20 | $75,308 |
| AZ | 18 | $74,093 |
| GA | 20 | $71,455 |
| CA | 14 | $46,341 |

**Money out:**
| Destination | Count | Amount |
|---|---|---|
| Wires to Importadora Quetzal Ltda (Guatemala) | 5 | $92,085 |
| Wires to Comercializadora del Norte SA (Mexico) | 5 | $81,971 |
| Wires to Yiwu Bright Star Trading (China) | 4 | $62,025 |
| Teller cash withdrawals at home branch BR03 (NJ) | 9 | $76,525 |

Her payroll (about $2,900 biweekly) continues normally alongside this activity.

## 3. Red flags
1. **Funnel account pattern** (FinCEN Advisory FIN-2014-A005): cash deposited in many distant locations by apparent third parties, then withdrawn or wired out in another place.
2. Physically impossible timing: same-day deposits hundreds of miles apart.
3. Cash volume of about $77K a month against an expected $13.1K total, from a salaried nurse with "Low" expected cash.
4. Wires labelled "MERCHANDISE" to trading companies in Mexico, Guatemala and China, which is consistent with trade-based settlement of drug or smuggling proceeds (the funnel-account and TBML link described in the advisory). The customer has no declared business.
5. All deposits are individually under $10K (none triggered a CTR), and the amounts vary, which looks like an attempt to blend in.

## 4. Mitigating factors considered
None identified. A nurse could in principle take travel assignments, but KYC lists no such work, her payroll comes from a single employer, and travel would not explain deposits in two states within half an hour.

## 5. Decision and rationale
**Escalated.** The account is receiving large volumes of out-of-area third-party cash and moving it to foreign trading companies and cash withdrawals, with no business purpose and in conflict with the customer's profile. This matches the funnel-account typology.

## 6. Recommendations to L2
- Pull deposit tickets and teller video for a sample of the deposits, to identify who made them.
- Check the foreign beneficiaries against prior SARs and 314(a) lists, and search negative news *[simulated]*.
- Consider restricting cash deposits at non-home branches pending investigation (the bank's policy on accepting third-party cash).
- If confirmed, file a SAR. Do not contact the customer.
