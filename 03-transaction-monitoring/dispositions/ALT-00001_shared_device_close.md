# ALT-00001 | R10 Shared Device | CLOSE: No Suspicious Activity

> **Synthetic case.** All names, accounts and transactions are fictional. *[simulated]* = a check this project does not model.

| Field | Value |
|---|---|
| Alert ID | ALT-00001 (related: ALT-00002, ALT-00003, the same device) |
| Rule | R10: one device used by 3 or more customers |
| Alert date | 2026-01-01 |
| Customers | C0036 Hannah Okafor (teacher, 55, NY), C0037 Ivan Moore (unemployed, 54, NY), C0038 Michael Scott (teacher, 41, GA) |
| Analyst / date | L1-ANALYST-01 / 2026-07-06 |
| **Decision** | **Close all three: no financial indicators of mule or fraud activity** |

## 1. Why the alert fired
Device DEV-653143 is linked to three customer profiles: it was registered at onboarding for all three and used for mobile banking by C0036 and C0038. Mule networks often run many accounts from a small set of phones, so the rule flags any device shared by 3 or more customers.

## 2. Review performed
- Six months of activity for all three customers.
- Funds flows **between** the three accounts, and to or from any common counterparties.
- Account tenure, and comparison with the mule-network pattern (new accounts, many senders, fast outflow, crypto).
- Address and phone match across the three profiles *[simulated: not in this dataset]*.

## 3. Analysis
| Mule indicator | C0036 | C0037 | C0038 |
|---|---|---|---|
| Account age | Since 2008 | Since 2022 | Since 2019 |
| Monthly volume vs expected | About $3K in, in line with $7.6K expected | 17 txns in 6 months, mostly benefit ACH and ATM | In line with expected |
| Many unrelated senders | No (3 small P2P in) | No | No |
| Fast outflow / crypto | No | No | No |
| Payments among the three | None | None | None |

On C0036's account the device carried only 13 low-value P2P payments ($47 to $291) to a stable set of friends. None of the three accounts shows any characteristic of a mule account. A shared device with long tenure, low value and no funds flow most often means a household or family member managing banking on one tablet, or an adult child (C0038, now in GA) who set up a parent's app.

## 4. Decision and rationale
All three alerts are closed. The device link alone is not suspicious: there are no linked funds flows, no new accounts, and no inflow or outflow pattern consistent with money mule or account-takeover activity.

## 5. Follow-up
- No SAR.
- Keep DEV-653143 on the device watch list: if a fourth profile, or a newly opened account, links to it, re-alert.
- **Tuning feedback:** R10 has low value on its own (its 3 false-positive alerts in this run are this household). Require one financial indicator as well (new account, many senders, or flows between the linked accounts), or feed R10 as a supporting factor into R08 instead of a standalone alert.
