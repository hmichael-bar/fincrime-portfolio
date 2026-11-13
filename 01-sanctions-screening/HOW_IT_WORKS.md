# How It Works – Interview Prep Sheet

## The logic in five steps

1. **Load the lists.** OFAC publishes the SDN list as CSV files: names, aliases (a.k.a./f.k.a.) and addresses. DOB, place of birth and nationality sit in a free-text "remarks" field, so the loader parses them out. Every alias becomes its own searchable name (about 41,000 in total).
2. **Normalise both sides the same way.** Uppercase/lowercase, accents and punctuation are removed, `LAST, First` is flipped, and legal forms (LLC, FZE) are dropped. The **Arabic module** then strips titles (Sheikh, Haji, Dr.), drops particles (al-, bin, ibn), joins compounds (*Abdel Rahman* → *abdrahman*), and maps each spelling to one canonical form (*Mohamed* → *muhammad*, *Gaddafi* → *qadhafi*). Arabic script is transliterated first.
3. **Find candidates fast, then score them carefully.** rapidfuzz pulls the closest few hundred names. Each candidate gets a 0–100 score blended from four measures: **token-sort ratio** (same letters, any word order), **Jaro-Winkler** (typo-tolerant, rewards matching beginnings), **word alignment** (does each word have a partner?) and a **consonant skeleton** (*Laden* = *Ladin* = `ldn`).
4. **Check secondary identifiers.** DOB, nationality and type (person vs company vs vessel) confirm or rule out the name match.
5. **Suggest a disposition, with reasons.**
   * **True Match:** strong name match plus an exact DOB, or birth year plus nationality.
   * **False Positive:** the name is similar but the DOB or entity type conflicts.
   * **Potential Match – escalate:** anything the data cannot settle. A human decides.

## Key compliance concepts

| Concept | Plain English |
|---|---|
| **SDN list** | People, companies, vessels and aircraft whose property U.S. persons must **block** (freeze). U.S. persons may not deal with them. OFAC also publishes non-SDN lists (e.g. sectoral SSI) that carry narrower restrictions. |
| **Strict liability** | A firm can be penalised even if it did not know. Intent affects the size of the penalty, not whether there is a violation. |
| **True match vs false positive** | An *alert* is only a name similarity. It is a **true match** only when the customer *is* the listed party, proven by secondary identifiers. Most alerts are **false positives**: same or similar name, different person. |
| **Alias screening** | Many SDNs are listed under several names. Screening only the primary name misses them. Here *ALI, Hassan* is an alias of an SDN whose primary name is *FADHIL, Mustafa Mohamed*. |
| **50% Rule** | A company owned **50% or more**, directly or indirectly, by one or more blocked persons (combined) is itself blocked, **even if it is not on the list**. Example: two SDN brothers own 35% + 20% = 55% of an unlisted company, so the company is blocked. |
| **OFAC's "reasonable" standard** | OFAC does not prescribe software or a threshold. It expects a **risk-based** program that is reasonably designed for the firm's exposure. Its 2019 compliance framework names five components: management commitment, risk assessment, internal controls, testing/audit and training. If a violation happens, OFAC asks whether the controls were reasonable. A screening tool that misses obvious spelling variants of a listed name is hard to defend. Every threshold and rule should be documented and tested. |
| **Block vs reject** | **Block**: freeze the funds when an SDN has an interest in them. **Reject**: refuse a transaction that is prohibited but involves no blocked property. Both are reported to OFAC within **10 business days**. Blocked property is also reported annually. |

## Five likely interview questions

**1. "An alert fires on a customer named Mohammed Ali Hassan. Walk me through it."**
First, I check which list it hit (SDN or non-SDN) and whether the match is on the primary name or an alias. Next, I see how much of the name matches: all of it, or two common words out of five. Then I compare the full SDN record with our KYC data: DOB, nationality, address and ID numbers. If the DOB clearly conflicts, I clear it as a false positive and document why. If the identifiers are consistent or missing, I escalate and request documents. A suspected true match goes to the OFAC officer, and OFAC's hotline can help confirm it.

**2. "Why do Arabic names cause so many false positives, and how would you reduce them?"**
Because one Arabic name has many valid English spellings, and a few names (Muhammad, Ali, Hassan) are extremely common. A loose fuzzy threshold catches the variants but floods the queue. My approach: normalise spellings to one canonical form so I can keep a **higher** threshold without missing variants. Then let DOB and nationality clear the common-name hits. In my test, recall at threshold 85 was 100% with the Arabic module and 75% without it. About three-quarters of the hits were auto-suggested false positives because the DOB conflicted.

**3. "Explain the 50% Rule with an example."**
If one or more blocked persons together own 50% or more of a company, the company is blocked too. Ownership through other companies counts, so you trace the chain. For example, an SDN owns 30% and another SDN owns 25% of an unlisted company: 55% in aggregate, so the company is blocked. Control alone, without ownership, does not trigger the rule, but it is still a red flag to escalate.

**4. "How would you choose a matching threshold?"**
I would test it, not guess it. Run a labelled sample, including known list names spelled differently, at several thresholds. Measure recall and alert volume, and pick the lowest workload that still catches the known variants. Then document the choice and re-test it periodically or when the list or customer base changes. Lowering the threshold costs analyst hours; raising it risks a miss, and a miss is a potential violation.

**5. "You confirm a true match on an incoming wire. What happens next?"**
I do not process it. I escalate immediately to the OFAC/sanctions officer. If the SDN has an interest in the funds, we block them into an interest-bearing blocked account. If the transaction is prohibited but nothing is blockable, we reject it. We report to OFAC within 10 business days, keep records for the required period (five years, extended to ten in 2024 legislation), and consider whether a SAR is also warranted. I would also check the customer's other accounts and related parties.
