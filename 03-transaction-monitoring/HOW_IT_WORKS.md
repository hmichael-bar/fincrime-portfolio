# How It Works: AML Transaction Monitoring Interview Prep

This is the study sheet behind the project. It explains the rules this simulator encodes, why each one exists, and how an L1 analyst is expected to think. Section 9 has interview questions with model answers.

> Everything in the project is synthetic. Legal references are summarised in plain language for study; check the primary sources (FinCEN, FFIEC BSA/AML Manual, eCFR) before relying on them at work.

---

## 1. The legal frame in one page

**Money laundering** means making criminal proceeds look legitimate. It is usually described in three stages:

| Stage | What happens | Example in this project |
|---|---|---|
| **Placement** | Dirty cash enters the financial system | Structured cash deposits (R01), funnel deposits (R03) |
| **Layering** | Funds are moved around to hide where they came from | Pass-through wires (R02), round-dollar shell payments (R05), mule-to-collector hops (R08) |
| **Integration** | Clean-looking money comes back out | "Trade" payments (R07), crypto purchases, property purchases |

**US framework**
- **Bank Secrecy Act (BSA), 1970.** Requires banks to keep records and file reports (CTRs, SARs) that help law enforcement. **FinCEN** (part of Treasury) administers it. The bank's own regulator (OCC, Federal Reserve, FDIC, NCUA, or a state regulator such as **NYDFS**) examines the bank for compliance.
- **USA PATRIOT Act, 2001 (Title III).** Added Customer Identification Programs, enhanced due diligence for foreign correspondent and private banking accounts, and information sharing under **314(a)** (government asks banks) and **314(b)** (banks share with each other under a safe harbor).
- **CDD Rule (2016, effective 2018).** Banks must identify the beneficial owners of legal-entity customers and understand the nature and purpose of each relationship. That is where the "expected activity" in a KYC profile comes from.
- **AML Act of 2020.** Modernised the BSA: whistleblower awards, the Corporate Transparency Act, and a push for risk-based, more effective programs.
- **NYDFS Part 504** (relevant for New York banks such as CFSB). Requires a documented transaction monitoring and sanctions filtering program, with an annual compliance certification to the regulator.

**The pillars of a BSA/AML program:** internal controls (policies, monitoring, systems), a designated BSA Officer, training, independent testing (audit), and risk-based customer due diligence.

**If you are interviewing in Doha:** Qatar's main law is **Law No. 20 of 2019 on Combating Money Laundering and Terrorism Financing**. Suspicious transaction reports (STRs) go to the **Qatar Financial Information Unit (QFIU)**. Banks are supervised by the **Qatar Central Bank**, and firms in the QFC by the **QFC Regulatory Authority**. The concepts carry over directly. Outside the US the report is usually called an STR rather than a SAR.

---

## 2. CTR vs SAR

| | **CTR**: Currency Transaction Report | **SAR**: Suspicious Activity Report |
|---|---|---|
| Trigger | **Cash** transactions over **$10,000** in one business day by or for one person (multiple cash transactions are added together) | Activity the bank **knows, suspects or has reason to suspect** is illegal, designed to evade the BSA, or has no business or apparent lawful purpose |
| Judgement needed? | **No.** It is automatic and objective. Most CTRs describe perfectly legal activity | **Yes.** It is the analyst's and investigator's judgement |
| Bank thresholds | Over $10,000 cash | Insider abuse: any amount. **$5,000+** if a suspect can be identified. **$25,000+** even without an identified suspect. **$5,000+** for possible money laundering or BSA violations |
| Deadline | 15 calendar days after the transaction | **30 calendar days** after initial detection of facts that may justify a SAR. Up to 60 days if no suspect is identified. Continuing activity: review every 90 days and file within about 120 days of the previous SAR |
| Tell the customer? | Allowed (it is routine) | **Never.** Disclosing a SAR is prohibited (31 U.S.C. 5318(g)(2)). Filers have safe-harbor protection |
| Records | 5 years | 5 years, along with the supporting documentation |

**How they fit together:** structuring is an attempt to dodge the **CTR**. The response is a **SAR**. A customer who deposits $9,500 twice to avoid a CTR has committed a crime even if the cash is clean.

---

## 3. Structuring: 31 U.S.C. 5324

**What the statute says, in plain words:** nobody may, *for the purpose of evading* a BSA reporting requirement such as the CTR:
1. cause or try to cause a bank to not file a required report,
2. cause or try to cause a bank to file a report with a material omission or misstatement, or
3. **structure** (or help structure) a transaction with one or more banks.

**Key points for interviews**
- **The source of the money does not matter.** Structuring clean money is still a crime. In *Ratzlaf v. United States* (1994) the Supreme Court required proof that the defendant knew structuring was illegal. Congress removed that requirement the same year, so today the government only has to show intent to evade the reporting requirement.
- **Penalties:** up to 5 years in prison, and up to 10 in aggravated cases (where it is combined with another federal crime, or part of a pattern of illegal activity over $100,000 in 12 months). The funds can be forfeited.
- **The analyst does not prove intent.** We report suspicion. Investigators and prosecutors decide intent.
- **Classic red flags** (FFIEC Manual): amounts just under $10K, the same person using several branches or days, several people ("smurfs") depositing into one account, a customer who asks about the reporting threshold or reduces a deposit after learning about it, and round amounts.
- **What is usually not structuring:** a business whose cash takings happen to vary and which regularly files CTRs (see disposition [ALT-00145](dispositions/ALT-00145_structuring_close.md)).

---

## 4. The typologies in this project

| Typology | What it is | Rule | Common legitimate lookalike (why we get false positives) |
|---|---|---|---|
| **Structuring** | Splitting cash under $10K to avoid CTRs | R01: 2 or more deposits of $8K to $10K in 5 days, total ≥ $10K | Cash businesses with variable takings; a private car sale paid in cash |
| **Rapid movement / pass-through** | Money comes in and leaves almost straight away, so the account is just a conduit | R02: ≥ $20K credit, ≥ 80% out within 3 days | Buying a house (brokerage to title company); trading in a car; importers paying suppliers as soon as customers pay |
| **Funnel account** | Cash deposited in many places by third parties, then withdrawn or wired elsewhere (common in drug-proceeds and US-Mexico TBML schemes) | R03: cash in 3 or more out-of-home states in a month, ≥ $10K | Truck drivers and travel nurses who deposit on the road (rarely 3 or more states) |
| **High-risk jurisdictions** | Flows to or from FATF black/grey-listed countries or known sanctions-evasion transshipment hubs | R04: monthly total thresholds by country tier; suppressed if the country is in the KYC profile | Family remittances, tuition from abroad, weddings and funerals overseas |
| **Round-dollar wires** | Repeated $10,000 / $25,000 / $50,000 wires to entities with vague purposes (shells, "consulting") | R05: 2 or more round wires ≥ $10K in a month | Property-management owner distributions, loan payoffs, brokerage transfers |
| **Dormant reactivation** | A quiet account suddenly moves large sums, which can indicate account takeover, a purchased account, or elder exploitation | R06: 90+ days without activity, then ≥ $15K in 30 days | Tax refunds, inheritances, insurance claims after a quiet period |
| **Trade-based ML (TBML)** | Moving value through trade: false invoices, over- or under-invoicing, third-party payments, goods unrelated to the business, free-zone intermediaries | R07: invoice wires meeting at least 2 of 4 indicators | Real importers with fixed-price orders and suppliers in grey-list countries |
| **Money mule network** | Accounts that receive scam or fraud proceeds from many victims and forward them to collectors, crypto or cash | R08: 10 or more senders, ≥ 80% out, plus new account, crypto or shared device. R10: shared device | Gig workers and landlords (many senders, but old accounts, no crypto, no shared devices) |
| **Catch-all** | Activity far above the KYC expected profile | R09: monthly volume ≥ 3x expected and ≥ $25K | Any big one-off life event |

**FATF lists:**
- The **black list** ("High-Risk Jurisdictions subject to a Call for Action": Iran, North Korea, Myanmar) means countermeasures or enhanced due diligence.
- The **grey list** ("Jurisdictions under Increased Monitoring") means the country has committed to fixing AML weaknesses. It does **not** mean the country is sanctioned.
- **Sanctions** are a separate legal regime (OFAC in the US). They are about *who* you deal with, not how risky a country's AML controls are.

---

## 5. How the detection stack works (plain language)

```
customers.csv + transactions.csv
        │
        ├──► Rules engine (src/rules.py) ─── 10 scenarios, thresholds in config/thresholds.json
        │        └─► alerts.csv: one alert per customer, per rule, per month
        │
        ├──► Anomaly model (src/anomaly.py) ─── 15 behaviour features per customer → Isolation Forest
        │        └─► anomaly score + "top drivers" (which features look most unusual)
        │
        └──► Combined risk score = 50% rule points + 50% anomaly percentile → orders the alert queue
                 │
                 ▼
        Analyst workbench (app/analyst_app.py) → disposition log (audit trail)
                 │
                 ▼
        Evaluation (src/evaluate.py) vs. hidden ground truth → precision, recall, tuning charts
```

- **Rules** are transparent and easy to explain to an examiner ("we alert when..."). They only catch patterns someone has already thought of.
- **The Isolation Forest** is an unsupervised model. It builds many random decision trees and measures how few splits it takes to isolate each customer from everyone else. Unusual customers get isolated quickly and receive a high anomaly score. It never sees the labels. In this run it reached **ROC AUC 0.97**, which means it ranks bad actors above good customers 97% of the time.
- **Why combine them:** the analysts' time is the scarce resource. Ranking the queue by rules plus anomaly score puts the real cases first. In this run, of the top 50 customers by combined score, **98% were bad actors**, against 76% for rules alone and 78% for the model alone.
- **A surprising result worth telling in an interview:** adding the static KYC risk rating into the ranking made it *worse* (top-50 precision fell from 98% to 70%). The rating describes *exposure* (cash business, import/export). Most bad actors were onboarded as ordinary low-risk individuals. Behaviour beat profile.

---

## 6. The alert → case → SAR workflow

```
DETECT ──► L1 TRIAGE ──────────► L2 INVESTIGATION ──► SAR DECISION ──► FILE ──► AFTER FILING
(system)   (analyst, SLA         (case: wider look-    (BSA Officer /     (FinCEN    • continuing-activity
           e.g. 5-10 days)       back, linked parties,  SAR committee)     BSA        review every 90 days
           • close: FP, with     RFIs, 314(b), open-   • file / no-file,  E-Filing,  • account action
             rationale           source research)       both documented   ≤30 days   (restrict / exit)
           • escalate                                                      from       • law-enforcement
                                                                           detection) requests, 314(a)
```

1. **Alert.** A rule or model fires. Nothing is suspicious yet; it is just a lead.
2. **L1 triage** (the job you are applying for). Review the KYC profile, the transactions and prior alerts. Either **close** with a written rationale, or **escalate**. The rationale must let an examiner reach the same conclusion without talking to you.
3. **Case (L2).** A deeper investigation: full look-back, linked accounts, counterparties, requests for information, information sharing with other banks under 314(b), open-source research.
4. **SAR decision.** A documented decision to file or not to file. A "no-file" decision must be justified too.
5. **Filing.** Within 30 days of detecting the facts. The narrative is the most important part (see `../04-sar-narratives/`).
6. **After filing.** Continuing-activity reviews, decisions to restrict or exit the relationship, and **no tipping off**.

---

## 7. Why false positives matter

- **Industry reality:** in many banks **over 90% of TM alerts are false positives**. Every one of them still costs analyst time, and each one has to be documented.
- **What it costs:** money (headcount), fatigue (real cases get worse attention), and delay (the 30-day SAR clock is running while real cases sit in a backlog).
- **But missing a case is worse.** Regulators punish weak monitoring with consent orders and penalties. Under-alerting is a bigger regulatory risk than over-alerting. Tuning has to be **risk-based, documented and tested**, not just a way to "reduce the queue".
- **How banks tune responsibly:**
  - **Above-the-line / below-the-line testing:** sample the activity just below a threshold to prove you are not missing suspicious cases before raising it.
  - **Segmentation:** apply different thresholds to different customer types (a deli is not a nurse).
  - **Use of the KYC profile:** for example, R04 suppresses countries already in the customer's profile.
  - **Model risk management:** independent validation, following the SR 11-7 / OCC 2011-12 guidance.
- **In this project's numbers** (`outputs/evaluation_report.md`):
  - Baseline thresholds: **869 alerts**, 60% precision, 98% of bad actors caught.
  - "Aggressive" preset: **1,602 alerts** (+84% workload), precision falls to 39%, **with no gain in detection**.
  - "Conservative" preset: **474 alerts**, 83% precision, but **3 bad actors missed**.
  - That is the trade-off you are expected to talk about.
  - Precision here is inflated because about 11% of the synthetic customers are bad actors (real banks: well under 1%). The *direction* of each trade-off is the lesson.

---

## 8. What a good L1 disposition contains
1. **What fired, and on which transactions** (IDs, dates, amounts).
2. **Who the customer is:** occupation or business, tenure, expected activity, risk rating.
3. **What you reviewed:** the look-back period and sources.
4. **Analysis:** red flags *and* mitigating factors, compared against the KYC profile.
5. **Decision plus rationale,** in neutral, factual language.
6. **Follow-up:** SAR recommendation, KYC update, tuning feedback.

Phrases to avoid: "looks fine", "customer is legit", "probably drug money". Write facts, not feelings.

---

## 9. Five likely interview questions with model answers

**Q1. What is the difference between a CTR and a SAR?**
> A CTR is an automatic report for cash transactions over $10,000 in a business day. No suspicion is involved, and most CTRs are about legitimate activity. A SAR is a judgement-based report when we know or suspect that activity is illegal, designed to evade the BSA, or has no apparent lawful purpose. Banks file it within 30 days of detection, above thresholds of $5,000 with a known suspect or $25,000 without one. The customer is never told. They connect through structuring: if someone splits cash to avoid the CTR, that is itself a reason to file a SAR.

**Q2. You get a structuring alert on a restaurant. How do you work it?**
> First, I check the KYC profile: expected cash activity, size, and how long it has been a customer. Then I look at the full history of cash deposits, not only the two that fired. Does the customer ever deposit over $10,000, meaning CTRs are being filed? Are the amounts uneven, with cents, the way takings naturally are, or round and clustered at $9,500 to $9,900? Is it one home branch or several branches on the same day? Does the timing match business days and weekends? Do the cash volumes match the card settlements and the size of the business? If it regularly crosses $10K and the pattern matches its takings, I close with that rationale and send tuning feedback. If deposits suddenly cluster just under $10K, at different branches, out of line with its history, I escalate.

**Q3. How do you decide between closing and escalating?**
> I ask whether I can explain the activity using facts I can document, mostly from the KYC profile and the transaction history. If there is a clear, lawful purpose that fits the customer (a car sale, a declared supplier, a recorded family payment), I close and write down the evidence. If the explanation needs me to assume things I cannot verify, or the red flags outweigh the mitigating factors, I escalate. When in doubt I escalate, because L2 can close a case but a closed alert is rarely reopened. I never contact the customer in a way that could tip them off.

**Q4. What is a money mule and how would you spot one?**
> A mule account receives fraud or scam proceeds from victims and passes them on, often to collector accounts, crypto or cash. Mules can be complicit or recruited unknowingly through fake job ads or romance scams. Signs: a new account; a sudden jump in incoming payments from many unrelated people, often with memos like "investment" or "fee"; money leaving within a day; payments to a few recipients or crypto exchanges; activity far above the profile; and device or IP links to other accounts. In my project the mule rule needed many senders plus fast outflow plus a secondary signal (new account, crypto, or a shared device). The secondary signal kept gig workers and landlords, who also have many senders, out of the queue.

**Q5. Our monitoring system produces 95% false positives. What would you do?**
> First I would find out where the false positives come from: which rules and which customer segments. In my project, the rapid-movement rule produced most of them, from importers and home buyers. Then I would test targeted changes: segment thresholds by customer type, use the KYC profile (for example, do not alert on countries the customer declared), add a secondary indicator, and rank the queue with a risk score so the best leads are worked first. Every change has to be tested before it goes live, including sampling below the new threshold to show we are not losing true positives, and documented for model risk management and the examiners. The aim is better alerts, not just fewer alerts.

**Bonus (for OFAC / sanctions roles). How is sanctions screening different from AML monitoring?**
> AML monitoring looks at *behaviour* over time and is risk-based. Sanctions compliance looks at *who* is involved, and it is strict liability: a violation can be penalised even without intent. OFAC screening checks names, entities, vessels and locations against lists like the SDN list. The **50 Percent Rule** blocks any entity owned 50% or more, in total, by blocked persons, even if the entity itself is not listed. A true match leads to **blocking** (freezing) or **rejecting** the transaction, depending on the program, and a report to OFAC within 10 business days. A FATF grey-listed country is not sanctioned. A sanctioned party in a "clean" country is.

---

## 10. Glossary
- **KYC / CDD / EDD:** Know Your Customer; Customer Due Diligence; Enhanced Due Diligence for higher-risk customers.
- **Expected activity:** what the customer said, at onboarding, they would do (volume, countries, cash). Monitoring compares behaviour against it.
- **RFI:** Request for Information, a question to the customer (usually through the relationship manager) to explain activity.
- **314(a) / 314(b):** information requests from the government / voluntary information sharing between banks.
- **PEP:** Politically Exposed Person.
- **FIU:** Financial Intelligence Unit, the national body that receives SARs/STRs (FinCEN in the US, QFIU in Qatar). At a bank, "FIU" also often means the internal investigations team.
- **Precision:** of the alerts generated, the share that were real. **Recall:** of the real cases, the share that alerted.
