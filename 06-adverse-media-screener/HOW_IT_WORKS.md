# How It Works – Interview Prep Sheet

## The logic in five steps

1. **Build search strings, like an analyst would.** For each name variant: the name alone, and the name plus an OR-list of risk words (`"Rami Makhlouf" (sanctions OR laundering OR fraud …)`). Both are run in English and in Arabic (`"رامي مخلوف" (عقوبات OR غسيل OR فساد …)`).
2. **Collect from free sources.** Google News RSS (English and Arabic editions) and the GDELT news index, which also translates foreign-language press. Every query and its status is logged, because an examiner may ask what you searched.
3. **Classify each headline.** Which risk category (money laundering, sanctions, fraud, bribery/corruption, terrorism financing, organised crime)? Which legal stage (allegation → charged → convicted/penalised/designated)? Is the subject actually named? Is there exculpatory wording, such as an acquittal or a lifted sanction?
4. **Score severity (0–100)** = how serious the category is × how far the legal process has gone × how clearly the subject is named. Example: *"CBUAE imposes sanctions on Bank Melli Iran"* = sanctions (90) × penalty stage (1.0) × named in headline (1.0) = **90**.
5. **De-duplicate and rate.** Syndicated copies of one story merge into one finding. The subject gets HIGH / MEDIUM / LOW / NONE with a reason. The analyst reads the top findings and documents a conclusion.

## Key compliance concepts

| Concept | Plain English |
|---|---|
| **Adverse media** (negative news) | Public reporting linking a customer to crime or misconduct. It is a risk *indicator*, not proof. It is screened at onboarding, at periodic review and when events trigger a review. |
| **Predicate offences** | The underlying crimes whose proceeds get laundered: fraud, corruption, drug trafficking, tax crimes and so on. The six categories map to FATF's designated predicate offences, which is why they are the ones that matter for AML. |
| **Credible vs. non-credible** | Weigh the source (Reuters vs an anonymous blog), corroboration (one outlet vs many) and recency. A conviction outweighs an allegation. An allegation from 2009 that was later dismissed weighs less than a fresh indictment. |
| **Namesake / false positive** | Same name, different person. Confirm identity with DOB, location, employer or photo before attaching a story to a customer file. |
| **EDD & PEPs** | High-risk customers and politically exposed persons get deeper and more frequent adverse-media review. Corruption news about a PEP is a central concern. |
| **What happens next** | Material adverse media can lead to: enhanced due diligence, a source-of-wealth or source-of-funds request, a higher risk rating, a SAR if it links to account activity, or an exit decision. The rationale is documented in every case. |

## Five likely interview questions

**1. "How do you run an adverse-media check on a new corporate customer?"**
I search the company, its directors and beneficial owners, and known aliases, in every relevant language. I use a name plus risk-terms search string and a reasonable look-back (often 3–5 years for serious crimes). I discard namesakes, read the credible hits in full, and summarise each one: what is alleged, by whom, what stage it has reached, and whether it involves our customer directly. Then I record my conclusion and any risk-rating change.

**2. "You get 300 hits. How do you prioritise?"**
First I de-duplicate, because syndicated stories inflate the count. Here, 201 articles on Bank Melli became 113 stories. Then I sort by severity: the most serious categories (terrorism financing, sanctions, laundering), the most advanced legal stage (convictions and penalties before allegations), and stories that name the subject in the headline. I read from the top down and spot-check the rest for anything the scoring missed.

**3. "Why search in Arabic if the customer's documents are in English?"**
Because the reporting may not be in English. For Rami Makhlouf, the most serious recent finding, a report on the UAE seizing his funds, appeared only in Arabic. The Arabic query returned twice as many articles as the English one. An English-only search would have under-rated him.

**4. "What are the limits of automated adverse-media screening?"**
It reads keywords, not meaning. It flagged *"Binance blocks MEXC transfers after FinCEN money laundering designation"* as adverse for Binance, but in that story MEXC is the designated party and Binance is complying. It also misses risk that appears only in the article body, and it cannot judge source credibility. The tool narrows the haystack. The analyst still makes the call and documents it.

**5. "A long-standing customer appears in a fresh news story about a bribery investigation. What do you do?"**
I confirm it is the same person or entity. I assess credibility and seriousness, and check whether our accounts could be involved: unusual flows, links to the counterparties named in the story. I escalate per policy, which normally means an event-driven review, EDD and possibly a higher risk rating. If the activity in our accounts looks connected to the alleged conduct, I refer it for SAR consideration. I do not alert the customer to the investigation (no tipping off).
