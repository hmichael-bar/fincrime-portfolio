---
title: "Findings Memo: The Cyprus Corridor in the ICIJ Offshore Leaks"
subtitle: "Network analysis of Cyprus-linked offshore structures, with a Malta and sanctions-exposure focus"
date: "12 November 2026"
---

**To:** EDD / Financial Intelligence Unit (portfolio exercise)
**From:** Analyst
**Re:** Network review of Cyprus-linked offshore structures, Malta overlap, and sanctions exposure
**Classification:** Public-source analysis. No customer data.

> **ICIJ caveat.** There are legitimate uses for offshore companies and trusts. ICIJ does not intend to suggest or imply that any people, companies or other entities included in the ICIJ Offshore Leaks Database have broken the law or otherwise behaved improperly. In this memo, a name match to a sanctions or PEP list is a **lead for review, not an identification**.

## 1. Bottom line up front

1. **The Cyprus corridor runs on a small number of professional intermediaries.** In the Cyprus-linked slice of the leaks (18,297 companies, 43,065 nodes), five service providers account for **8,673 entity-intermediary links**. The largest, Consulco International Ltd, is recorded with Cyprus and UAE addresses and administered **3,168** companies. The third largest is a UAE free-zone vehicle (*Omni Management Consultancy FZE*, recorded in Cyprus). For a bank, an intermediary is a concentration risk: one weak provider can seed thousands of customers.
2. **Mass registration and nominee patterns are pervasive.** We found **51 addresses** each used by 20 or more companies. The largest are law-firm and corporate-services offices in Nicosia and Limassol, plus one Valletta address used by 201 Malta companies. We also found **109 officers** holding board or shareholder roles at 25 or more companies each. Of these, 67 are corporate nominee vehicles and 42 are individuals. One individual holds roles at 180 companies.
3. **One cluster ties Cyprus, Malta and later sanctions together.** Exact-name screening against OpenSanctions found the **Christodoulos G. Vassiliades law-firm network**. On **12 April 2023** the US designated it, in a State Department action alongside OFAC's Usmanov-related designations, and the UK designated it the same day. The network appears as **156 node records attached to 278 companies**, across the Pandora Papers, Panama Papers, Paradise Papers (including the **Malta company registry**) and the 2013 Offshore Leaks. In **136** of those links the firm or its principal is recorded as *Beneficial Owner* or *Ultimate Beneficial Owner*. That is a strong sign that the real owner sits behind a nominee or trust layer.
4. **Russia and Gulf exposure is material.** **1,730** companies in scope have at least one officer with a Russia, Ukraine, Belarus or Kazakhstan address, and **991** have an officer in a GCC state. Screening produced **1,291 raw alerts**. After analyst review, **28 distinct names (25 distinct watchlist records) were dispositioned as probable or possible matches** to US/EU/UK sanctions lists, and **23 records were cleared as false positives**.
5. **Circular ownership is rare in this data.** We found only **4 mutual-shareholding loops** (A owns B, B owns A). All four are two-company pairs. Two are in the Malta registry and two in the Panama Papers. Each needs a registry check before any conclusion is drawn.

## 2. Scope, data and method

| Item | Detail |
|---|---|
| Data | ICIJ Offshore Leaks Database bulk CSV (build of 9 Sep 2026): Panama, Paradise, Pandora, Bahamas Leaks and 2013 Offshore Leaks. OpenSanctions "default" collection (downloaded 12 Nov 2026). |
| Scope rule | Every node ICIJ tags with Cyprus, plus every company one hop from such a node, plus that company's other officers, intermediaries and addresses. |
| Graph | 43,065 nodes (18,297 entities, 23,355 officers, 523 intermediaries, 835 addresses) and 73,116 documented relationships. ICIJ's fuzzy "similar name" links are excluded on purpose. |
| Analytics | Degree, betweenness (2,000-node sample) and PageRank centrality; intermediary and address concentration; officer role counts (threshold 25); cycle search on ownership edges after merging duplicate company records. |
| Screening | Name normalisation, exact plus fuzzy matching (RapidFuzz ≥93), name-ambiguity and country corroboration grading, then manual disposition (`data/analyst_review.csv`). |

The data runs **only to 2015–2018**, depending on the leak. Every finding is historical. Each one is a reason to refresh due diligence today, not a finding about current ownership.

## 3. Findings

### 3.1 Hub intermediaries (who builds the structures)

| Rank | Intermediary (recorded country) | Companies in scope | Main jurisdictions used |
|---|---|---|---|
| 1 | Consulco International Ltd (Cyprus, UAE) | 3,168 | BVI 1,497 · Seychelles 817 · Bahamas 493 |
| 2 | G.S.L. Law & Consulting (Cyprus) | 2,096 | Not stated (2013 Offshore Leaks) |
| 3 | Omni Management Consultancy FZE (Cyprus) | 1,315 | BVI 916 · Anguilla 117 · Seychelles 95 |
| 4 | Chesterfield Group Ltd (Cyprus) | 1,140 | BVI 739 · Bahamas 175 · Niue 170 |
| 5 | Christabel Corporate Services Ltd (Cyprus) | 954 | Not stated (2013 Offshore Leaks) |

Consulco and Omni also have the **highest betweenness** in the graph (0.73 and 0.63). In plain terms, a large share of the shortest paths between otherwise unrelated companies pass through them. The pattern is the classic Cyprus "wrapper": a Cyprus law or corporate-services firm sets up companies in zero-tax registries (BVI, Seychelles) for clients who are often in Russia or the CIS. The firm then supplies directors, shareholders and a registered office. *Omni Management Consultancy* carries an "FZE" (UAE free-zone establishment) suffix, which points to the **Cyprus–UAE pairing** that later shows up in post-2022 sanctions-evasion cases (see Report 2 in `05-typology-reports`).

### 3.2 Mass-registration addresses and nominee officers

- The **top shared address**, a Nicosia law-firm billing address, is the registered or contact address for **2,096** companies. A Limassol corporate-services building hosts **954**.
- **Malta:** *171 Old Bakery Street, Valletta* is the registered address of **201** Malta companies in scope. All **1,681** Malta-registry companies in scope have at least one Cyprus-based officer. That is true by construction, because a Cyprus link is how they entered scope, but it shows how tightly the two corporate-service markets interlock.
- **Nominee signatures:** Corporate officers such as *Dorchester International Inc* (St Kitts & Nevis) are shareholders of **263** companies, and Seychelles vehicles such as *Intercon Ltd* hold **187**. Several officers are named outright as nominees, e.g. *Eurotrade Nominees Ltd* and *Integrity Directors Ltd*. Individuals with 100 or more directorships appear in this data, mostly with UAE or UK addresses. Their names are withheld because they are private persons.
- **Single-ship companies:** One Cyprus ship manager, *Volgo-Baltic Shipmanagement Ltd*, is director and legal representative of **36 Malta companies** with names like *Volga-Baltic Ship 1–10*, *Rusich-2…13* and *Valday-1…4*, incorporated 2001–2007. One company per vessel is standard and lawful in shipping. It is also the structure behind the dark-fleet ownership chains described in the Malta case study and in Report 1. A bank financing or insuring such vessels should look through to the group.

### 3.3 Case study: the Vassiliades / Ledra cluster

| Attribute | Finding |
|---|---|
| Anchors | Christodoulos G. Vassiliades; Christodoulos G. Vassiliades & Co. LLC; Ledra Nominees Ltd; Ledra Trustees Ltd; Ledra Trustee Services Ltd; Vassiliades & Co. (Malta) Ltd. All are exact-name matches to entries OpenSanctions sources to the OFAC SDN list. |
| Designation context | On 12 Apr 2023 the US State Department designated the Vassiliades network as an enabler of Russian oligarchs. This was part of a coordinated US action that OFAC announced as targeting Usmanov's network and other facilitators [1][2]. The UK sanctioned Vassiliades the same day as a "financial fixer" for Usmanov [3]. |
| Footprint in leaks | 278 companies: 148 in Pandora Papers (Alcogal, Panama), 98 in Offshore Leaks, 20 in the Malta registry, 9 in Panama Papers, 3 in Paradise Papers (Appleby, Bermuda) |
| Roles | 136 (Ultimate) Beneficial Owner records; 132 intermediary records; 30 shareholder records; 12 directorships; 12 judicial or legal representative roles (Malta) |
| Timeline | Incorporations from 1992 to 2018, peaking in 1997 (57 companies) |
| Russia exposure | 11 companies also list at least one Russia-based officer. In Bermuda (Appleby), Vassiliades is recorded as director and president of an aircraft-holding company whose shareholders include a Russian trading group. |

**Analyst assessment.** The designation came years *after* these records were created. Being administered by a later-designated professional does **not** make a company sanctioned, and the OFAC 50 Percent Rule turns on *ownership by a blocked person*, not on administration. What it does do is put **all 278 companies on a priority re-screening list**. Three things raise their risk. First, for 136 of them the leak records name the law firm, not a natural person, as beneficial owner. Second, the same firm had a Malta subsidiary that was also designated. Third, the State Department publicly described the network as an enabler of Russian oligarchs. A bank with exposure to any of these companies should request current UBO evidence, trust deeds and settlor/beneficiary details, and should assess any nominee or trustee layer controlled by the Vassiliades network for 50%-rule exposure to its clients.

**What we excluded and why.** Ten name-similar records (e.g. *Ledra Shipping Company Ltd*, *Duval Vassiliades Solicitors*) were **not** attributed to the network. "Ledra" is a common Cypriot name, and a different UK firm uses "Vassiliades". These records are listed in `outputs/case_vassiliades_excluded_for_review.csv`.

### 3.4 Sanctions and PEP screening results

- **Funnel:** 1,291 raw alerts → 854 grade A/B (exact, or near-exact with country corroboration) → 28 names dispositioned probable/possible.
- **Probable matches** (after review) include the Vassiliades and Ledra entities, Gazprombank-group holding company *GPB-DI Holdings Ltd* (Cyprus), *IPP Oil Products (Cyprus) Ltd*, Bermuda's *Altitude X3 Ltd* (OFAC-designated on 3 Mar 2022 [4]), FESCO, and a set of prominent Russian and Ukrainian business figures whose names appear in Panama, Pandora and 2013 Offshore Leaks records. These are public figures on one or more US/EU/UK lists.
- **False positives cleared (23):** very common Russian and Greek-Cypriot names with several different people on the watchlists, cleared because nothing in the leak record corroborated identity. One leak record shares its name with Russia's foreign minister, a textbook false positive. Names of cleared private individuals are not reproduced here.
- **Ambiguous (1):** *Boris Rotenberg*. Two sanctioned people share the name (father and son), and the leak record carries no date of birth.
- **Not yet reviewed:** 518 alerts (mostly PEP and non-Western lists), left as a work queue in `outputs/screening_results_reviewed.csv` with private-person names withheld.

### 3.5 Circular ownership

After merging 1,345 officer records into their matching company records (ICIJ often stores the same company twice), cycle search over 25,544 ownership edges found **four 2-company mutual-shareholding loops**. Mutual shareholding is unusual and can hide who sits at the top. It can also be a data-entry artefact, so each loop goes to registry verification rather than escalation.

## 4. Red flags and recommendations

**Red flags for onboarding and periodic review:** (1) the beneficial owner is recorded as a **law firm, trust company or nominee**; (2) the company was formed by a **high-volume intermediary** (more than 1,000 companies) or sits at a **mass-registration address**; (3) officers hold **25 or more concurrent appointments**; (4) a **Cyprus or Malta administrator** is paired with a BVI, Seychelles or St Kitts & Nevis vehicle and officers in Russia, the CIS or a UAE free zone; (5) a **single-ship company** whose owner is not visible past the ship manager; (6) any link to a **later-designated professional enabler**.

**Recommendations**

1. **Re-screen** all 278 Vassiliades/Ledra-linked companies and any customer using them, and document a 50%-rule analysis for each.
2. **Screen intermediaries, not just owners.** Keep a watchlist of designated enablers (law firms, trust and nominee providers), and alert when one appears as formation agent, nominee or trustee anywhere in a customer's chain.
3. **Score concentration.** Treat structures built on a top-decile intermediary or address as higher-risk until UBO evidence is obtained.
4. **Tune name screening** with a name-frequency penalty (as built here), so common names need a DOB or ID number before escalation.

**Limitations.** The leaks are a partial, dated, non-random sample of a few providers' files. There is no customer or transaction data, and nearly all matches are on names only, without DOB or ID corroboration.

## Sources

[1] U.S. Department of the Treasury, "Treasury Targets Russian Financial Facilitators and Sanctions Evaders Around the World," press release JY1402, 12 Apr 2023. https://home.treasury.gov/news/press-releases/jy1402
[2] OFAC, Recent Actions, "Russia-related Designations," 12 Apr 2023 (SDN entries incl. VASSILIADES, Christodoulos Georgiou; VASSILIADES & CO. MALTA LIMITED; LEDRA NOMINEES LIMITED; LEDRA TRUSTEES LIMITED; LEDRA TRUSTEE SERVICES LIMITED). https://ofac.treasury.gov/recent-actions/20230412
[3] UK Government, "UK sanctions Abramovich and Usmanov's financial fixers in crackdown on oligarch enablers," 12 Apr 2023. https://www.gov.uk/government/news/uk-sanctions-abramovich-and-usmanovs-financial-fixers-in-crackdown-on-oligarch-enablers
[4] OpenSanctions entity record for ALTITUDE X3 LTD (source: OFAC SDN, designated 3 Mar 2022). https://www.opensanctions.org/entities/ofac-35326/
[5] ICIJ, Offshore Leaks Database (data and caveat). https://offshoreleaks.icij.org/
[6] OpenSanctions, "Default" dataset. https://www.opensanctions.org/datasets/default/
[7] OCCRP, "The Secret Caretaker" (Panama Papers reporting on Cyprus-routed loans to Roldugin-linked entities). https://www.occrp.org/en/panamapapers/the-secret-caretaker
