# How It Works: Interview Prep (Project 02)

## The 30-second pitch

> "I took the ICIJ Offshore Leaks database, about two million nodes, and cut out everything connected to Cyprus. That's roughly 18,000 companies. I built a graph in Python with networkx to find the service providers, addresses and nominee directors that hold the network together. Then I screened every name against OpenSanctions. The standout was a Cypriot law-firm network, Vassiliades and Ledra, that the US and UK designated in April 2023. It's attached to 278 companies across four leak sets and the Malta company registry, and for 136 of them the firm itself is recorded as beneficial owner. My memo turns that into a re-screening list and a set of red flags for onboarding."

## Key terms (say these comfortably)

| Term | Plain meaning |
|---|---|
| **Node / edge** | A node is a thing (company, person, agent, address). An edge is a documented relationship ("director of", "registered address"). |
| **Intermediary** | The law firm or corporate-services provider that formed or administers the company. Think of it as the "factory". |
| **Degree centrality** | How many direct connections a node has. High degree means a hub. |
| **Betweenness centrality** | How often a node sits on the shortest path between two other nodes. High betweenness means a bridge or chokepoint. |
| **Nominee director/shareholder** | A person or company that holds a role on paper for someone else. It is legal in many places, but it hides the real owner. |
| **Circular ownership** | A owns B and B owns A (or a longer loop). It can make "who is at the top?" unanswerable. |
| **OFAC 50 Percent Rule** | An entity owned 50% or more, directly or indirectly, individually or in aggregate, by blocked persons is itself blocked, even if it isn't on the list. |
| **False positive** | A screening alert where the name matches but it's a different person. |

---

## Q1. "Walk me through how you built the network and why you scoped it that way."

**Answer:** The full ICIJ dataset is about 2 million nodes. Most of it is irrelevant to a Cyprus question, and a graph that big is unreadable. So I used a **seed-and-expand** rule. The seeds are every node ICIJ tags with Cyprus: companies, officers, intermediaries and addresses. Then I added every company one hop from a seed, plus that company's other officers and agents. That gives about 43,000 nodes and 73,000 edges. It's big enough to show the real infrastructure and small enough to compute centrality on a laptop.

I deliberately **dropped ICIJ's "similar name" and "same name as" links**, because those are ICIJ's own fuzzy suggestions, not documented relationships. In an investigation you don't want guesses baked into the evidence graph.

**Follow-up you might get: "What does that miss?"** Anything two or more hops from Cyprus. For example, a Russian owner who uses a BVI company administered from Switzerland, with no Cyprus node at all. And anything after 2018, because the leaks are dated.

## Q2. "How did you decide a sanctions match was real?"

**Answer:** In three layers, the same way a bank alert queue works.

1. **Automated matching.** I normalise names: upper-case, strip accents, drop titles like "Mr" and suffixes like "Ltd", and sort the words, so "Petrov Alexander" equals "Alexander Petrov". Then I match exactly, or fuzzily at 93% similarity or higher.
2. **Grading.** Grade A needs an exact match, a name that is *unique* on the watchlist, and a country that agrees (or a three-part name). This is how I handled the "John Smith problem": common names get downgraded automatically.
3. **Human disposition.** I reviewed the important alerts and wrote the decision and reason into `analyst_review.csv`. For example, one Panama Papers officer shares a name with Russia's foreign minister. That's a **false positive**: nothing else corroborates it, so I cleared it and kept the private person's name out of the outputs. "Boris Rotenberg" is **ambiguous**, because two sanctioned people share that name (father and son) and the leak has no date of birth.

The end result: 1,291 raw alerts → 854 strong → 28 probable or possible names. And I never put an unreviewed alert on the map.

## Q3. "What's the most important finding and what would you do with it at a bank?"

**Answer:** The **Vassiliades / Ledra cluster**. The US State Department designated Christodoulos Vassiliades's network on 12 April 2023, as part of the Usmanov-related action. That included his firm, Ledra nominee and trustee companies, and a Malta subsidiary. The UK sanctioned him the same day as a "financial fixer". In the leaks, those entities are attached to 278 companies. Most telling: in **136 records the law firm is listed as beneficial owner**, which means the real owner sits behind a nominee or trust layer.

At a bank I would:

1. Re-screen every customer and counterparty connected to those 278 companies.
2. For each one, get current UBO evidence and trust documents, and do a **50 Percent Rule** analysis.
3. Add designated *enablers* (law firms, trust companies) to intermediary-level screening, so they're caught when they appear as agent or trustee, not only as owner.

**The nuance you must say out loud:** being *administered* by a designated firm doesn't make a company blocked. The 50% rule is about **ownership**. So this is a priority review list, not a list of sanctioned companies.

## Q4. "Explain centrality to me like I'm not technical. Why does it matter for AML?"

**Answer:** Picture an airport map. **Degree** is how many routes leave an airport. **Betweenness** is how many trips between *other* cities have to change planes there. Here, the top two by betweenness are Consulco International and Omni Management Consultancy FZE, both corporate-service providers. A huge share of paths between otherwise unrelated companies run through them.

For AML that matters in two ways. First, **concentration risk**: if one provider is weak or complicit, thousands of companies inherit that weakness. Second, **efficient investigation**: if you have one bad company, the high-betweenness node is the fastest route to its siblings. I'd use these hubs as a risk factor in customer scoring, not as evidence against them. These are often perfectly legitimate firms.

## Q5. "What are the limitations? Would you stand behind this in front of a regulator?"

**Answer:** I'd stand behind the **method** and say clearly what the **data** can't prove.

- **Dated and partial:** the leaks are a few providers' files, and they run to 2015–2018. Ownership has almost certainly changed.
- **Name-only matching:** most leak records lack a date of birth or ID number, so even "probable" matches need corroboration from corporate registries, court records or the customer.
- **Not a random sample:** finding more Russian links in Cyprus partly reflects *whose* files leaked.
- **No transactions:** network position is a risk *indicator*, not evidence of laundering.
- **Leaks ≠ wrongdoing:** I quote ICIJ's caveat on every output, and I never name private individuals.

So the memo's language is "priority for review" and "red flags", not "this company is laundering money". That's the line between an analyst and an accuser.

---

### Numbers worth memorising
43,065 nodes · 18,297 companies · 1,688 Malta companies · top intermediary 3,168 companies · 51 addresses with 20+ companies · 109 high-volume officers · 4 mutual-ownership loops · 1,291 → 854 → 28 screening funnel · Vassiliades: 278 companies, 136 "beneficial owner" records, designated 12 Apr 2023.
