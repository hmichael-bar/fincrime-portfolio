---
title: "Typology Report 1: Shadow Fleet Oil Shipping"
subtitle: "STS transfers, AIS spoofing, flag-hopping, the Russian oil price cap and Iranian crude"
date: "November 2026"
---

## Executive summary

A "shadow" or "dark" fleet is a pool of mostly older tankers whose ownership, insurance and movements are deliberately obscured. They carry oil for sanctioned states, mainly Russia, Iran and Venezuela. The IMO Assembly formally recognised the problem in December 2023 (Resolution A.1192(33)). That resolution describes the dark fleet as ships engaged in illegal operations to circumvent sanctions, including by switching off AIS [1]. C4ADS estimates the global dark fleet at **500 to 1,000 vessels** [2].

For a bank, the exposure is rarely the tanker itself. It is the **payments around it**: freight, charter hire, bunkers, port fees, insurance premiums, ship sale-and-purchase proceeds, trade finance on the cargo, and the corporate accounts of single-ship owning companies and their managers. The core analytical task is to connect a payment to a **vessel (IMO number)**, the vessel to its **behaviour** (AIS gaps, ship-to-ship transfers, flag changes), and the behaviour to a **sanctions nexus** (designated vessel, owner, manager, cargo origin or price-cap breach).

**Bottom line:** Treat any oil-related payment as higher-risk when the vessel is over 15 years old, recently re-flagged, insured outside the International Group of P&I Clubs, managed by a recently formed company in a high-risk hub, or engaged in STS transfers in known hotspots. These factors reflect the deceptive-practice and due-diligence indicators in US and Price Cap Coalition advisories [3][4].

## 1. How the scheme works

### 1.1 The legal targets

| Regime | What it prohibits | Key dates |
|---|---|---|
| **Russian oil price cap** (G7 + EU + Australia "Price Cap Coalition") | Coalition-based services (insurance, finance, shipping, brokering) for seaborne Russian crude or products sold **above** the cap. The oil itself is not banned. | Crude cap of **$60/bbl** from 5 Dec 2022. The EU lowered its cap to **$47.60** (Sept 2025), then **$44.10** from 1 Feb 2026 under a dynamic mechanism set at 15% below average Urals prices. The UK aligned, while the US stayed at $60 [5][6]. |
| **US Russia sanctions (EO 14024)** | All dealings with designated vessels, owners and oil majors | On **10 Jan 2025** OFAC designated **Gazprom Neft, Surgutneftegas and 183 vessels**, its largest shadow-fleet action at the time [7] |
| **US Iran sanctions** | Almost any dealing in Iranian petroleum, including by foreign buyers | Since NSPM-2 (Feb 2025) OFAC has repeatedly designated tankers, ship managers and Chinese "teapot" refineries. Example: Luqing Petrochemical and 8 vessels on **20 Mar 2025** [8] |

The price cap creates a **paperwork incentive**. A Coalition service provider is protected if it holds an **attestation** that the oil was bought at or below the cap. The October 2024 updated Coalition advisory recommends further due diligence: itemised ancillary costs, appropriately capitalised P&I insurance, and continuous AIS [4]. Shadow-fleet operators avoid the issue entirely by **leaving the Coalition's service ecosystem**. They use non-Western insurers, non-Coalition ship managers and opaque single-ship companies. KSE Institute reports that Russian-flagged tankers rose from **3% to 21%** of the shadow fleet between May 2025 and February 2026 [9].

### 1.2 The toolbox (deceptive shipping practices)

The May 2020 US Global Maritime Sanctions Advisory (OFAC, State Department and US Coast Guard) remains the standard list [3]:

1. **AIS disabling or manipulation ("going dark" and "spoofing").** A ship stops broadcasting its position, or broadcasts a false one, to hide a port call or meeting. Spoofing can be sophisticated. C4ADS documents a China-linked network of 50+ supertankers (the "Protean Fleet") that used GNSS manipulation and frequent dark voyages [2].
2. **Ship-to-ship (STS) transfers.** Cargo is moved between tankers at sea to blend or disguise origin. STS is often legitimate, so location and counterpart matter. Hotspots include the Gulf of Oman, off Malaysia, the Laconian Gulf and offshore Malta.
3. **Falsified cargo and vessel documents.** These include bills of lading, certificates of origin and invoices. Iranian crude is frequently relabelled as Malaysian or Iraqi.
4. **Flag-hopping and fraudulent registries.** Ships re-flag repeatedly to registries with weak oversight, or to "false flags" (registries the purported flag state does not recognise).
5. **Complex ownership and management.** Each tanker sits in its own single-ship company, often in the Marshall Islands, Liberia, Hong Kong or the UAE. Ship managers are frequently newly formed and change often (see Project 02: one Cyprus manager directed 36 single-ship Malta companies).
6. **Voyage irregularities.** These include unexplained loitering, indirect routing and port calls that do not fit the cargo.
7. **Name and IMO-number games.** Vessels are renamed. In extreme cases a ship takes another vessel's identity ("zombie" ships).

### 1.3 The money trail

```
 Buyer/trader (often UAE, HK, India)  ── cargo payment ──►  Seller (Russian/Iranian exporter or front)
        │                                                      ▲
        │ charter hire / freight                               │ price-cap attestation (if Coalition services used)
        ▼                                                      │
 Single-ship owner (Marshall Is., HK, UAE) ◄── ship manager (new, high-risk hub) ── crew, bunkers, port fees
        │
        └── P&I insurance (non-IG insurer)   +   ship sale proceeds when tankers are bought from Western owners
```

Banks are most likely to see: (a) **USD or EUR payments to trading houses** that broker Russian or Iranian oil; (b) **ship sale-and-purchase** proceeds when old Western tankers are sold to newly formed buyers; (c) **operating accounts** of ship managers and owners; and (d) **trade finance** (letters of credit) on cargoes with doubtful origin.

## 2. Red flags for banks

**Vessel and voyage**

- The vessel is **15 years or older**, had a **recent change of flag, name, owner or manager**, or flies a flag with a weak registry record or a false flag.
- There are **AIS gaps** near high-risk loading areas (Russian Baltic or Black Sea ports, Kharg Island, Venezuelan terminals) or near known STS zones [3].
- There is an **STS transfer** with a designated or "dark" vessel, or in a hotspot, without a documented commercial reason.
- Insurance is **outside the International Group of P&I Clubs**, or the insurer cannot be verified [4].

**Counterparty and corporate**

- The owner or manager was **formed in the past 12–24 months**, sits at a **mass-registration address**, or shares officers with designated companies.
- The buyer is a **newly formed tanker purchaser** paying cash for a 15–20-year-old tanker at or above market price (a common way Western tonnage moved into the shadow fleet).
- A trading company with **no oil-trading history** suddenly handles large crude cargoes, often in the UAE or Hong Kong.

**Documentation and pricing**

- **Price-cap attestations** are missing, generic or inconsistent. Ancillary costs (freight, insurance) are not itemised, or are implausibly high, which can disguise an above-cap price [4].
- The **certificate of origin conflicts** with the voyage history (e.g. "Malaysian blend" loaded after an STS off Malaysia from an Iran-linked tanker).
- **Round-number payments** or payments routed through unrelated third countries.

## 3. Case examples

**Case 1: *Suez Rajan* and Iranian crude (US, 2023).** US authorities seized about 1 million barrels of Iranian crude from the tanker *Suez Rajan*. Its Greek operator, **Empire Navigation**, pleaded guilty to an Iran sanctions violation and agreed to a fine of about **$2.4 million** and three years' probation. Court papers said the ship tried to disguise the cargo's origin by claiming it came from another tanker, a classic STS cover story [10]. *Lesson:* the documentary claim of origin is often exactly what the STS was designed to fake.

**Case 2: OFAC's 10 January 2025 action.** OFAC designated **Gazprom Neft and Surgutneftegas**, insurers including Ingosstrakh, and **183 vessels**, most of them tankers [7]. *Lesson:* screening must run on **IMO numbers**, not vessel names, and must be re-run on the entire book after each mass designation, including ship-sale and charter payments.

**Case 3: Teapot refineries and the Iran network (2025).** On 20 March 2025 OFAC designated a Chinese independent refinery that had bought about half a billion dollars of Iranian oil. It also designated ship managers in Hong Kong and elsewhere and 8 tankers, citing AIS manipulation [8]. *Lesson:* the buyer end of the chain is now a sanctions target, so trade-finance exposure to refiners matters.

**Case 4: *Eagle S* and the Baltic cable (Finland, Dec 2024).** Finnish authorities detained the Cook Islands-flagged tanker *Eagle S*, owned by a UAE-registered company, on suspicion of damaging the Estlink 2 power cable with its anchor. The European Commission described the ship as part of Russia's shadow fleet of aged, poorly insured vessels [11]. *Lesson:* shadow-fleet exposure is also **physical, environmental and reputational** risk, not just sanctions risk.

**Case 5: The policy is still moving (2026).** In January 2026 the EU and UK cut their crude cap to $44.10 [5][6]. Meanwhile, during the 2026 oil-price shock linked to the Iran conflict, OFAC issued temporary general licenses (the GL 134 series, March–June 2026). These authorised transactions in Russian-origin oil **already loaded at sea** [12]. *Lesson:* the rules differ by jurisdiction and change month to month. Controls must reference the **current** cap and licence for each regime, and record which one applied.

## 4. Detection and screening recommendations

1. **Screen the vessel, not just the parties.** Capture the **IMO number** for every oil- or shipping-related payment, LC and loan. Screen it against OFAC, EU and UK vessel listings and re-screen on every list update.
2. **Buy or build maritime-intelligence enrichment.** Feed AIS-gap, STS, flag-history and ownership-change scores from a commercial provider into the transaction-monitoring rules. Alert when a payment's vessel has a "dark activity" event within ±30 days of the payment.
3. **Price-cap evidence file.** For Coalition-nexus oil, require the attestation tier the Coalition advisory recommends: itemised costs and documented insurance [4]. Store the evidence with the transaction.
4. **Ship sale-and-purchase EDD.** Treat the sale of a tanker over 15 years old to a buyer formed in the last 24 months as high-risk by default. Obtain UBO, source of funds and intended trade.
5. **Network screening.** Run graph analysis across owners, managers, addresses and officers, as in Project 02. A single shared address or director often links a clean-looking company to a designated fleet.
6. **Contract clauses.** Encourage clients to adopt clauses making AIS disabling or unexplained STS a termination event, as recommended by the 2020 advisory [3].
7. **SAR narrative quality.** Name the vessel (IMO), the behaviour (date and place of AIS gap or STS), and the sanctions nexus. Note that the UN DPRK Panel of Experts, a key public source on STS evasion, lost its mandate after Russia's March 2024 veto, so public reporting now relies more on national authorities and NGOs [13].

## Sources

[1] IMO, "IMO Assembly, 33rd session, 27 Nov–6 Dec 2023" (Resolution A.1192(33) on dark fleet operations). https://www.imo.org/en/mediacentre/meetingsummaries/pages/imo-assembly%2C-33rd-session%2C-27-november---6-december-2023-.aspx
[2] C4ADS, *Oil and Water* (June 2025). https://c4ads.org/reports/oil-and-water/
[3] OFAC, US Department of State and US Coast Guard, "Sanctions Advisory for the Maritime Industry, Energy and Metals Sectors, and Related Communities," 14 May 2020. https://ofac.treasury.gov/system/files/126/05142020_global_advisory_v1.pdf
[4] Price Cap Coalition, "Updated Advisory for the Maritime Oil Industry and Related Sectors," 21 Oct 2024 (builds on the Oct 2023 advisory and the Feb 2024 Compliance and Enforcement Alert). https://ofac.treasury.gov/media/933506/download ; https://ofac.treasury.gov/recent-actions/20241021
[5] European Commission, "New dynamic mechanism to lower price cap for Russian crude oil to USD 44.10 per barrel," 15 Jan 2026. https://finance.ec.europa.eu/news/new-dynamic-mechanism-lower-price-cap-russian-crude-oil-4410-barrel-2026-01-15_en
[6] Baker McKenzie Sanctions Blog, "EU and UK announce aligned reduction of the Russian Oil Price Cap." https://sanctionsnews.bakermckenzie.com/eu-and-uk-announce-aligned-reduction-of-the-russian-oil-price-cap/
[7] US Treasury, press release JY2777, 10 Jan 2025 (Gazprom Neft, Surgutneftegas, 183 vessels). https://home.treasury.gov/news/press-releases/jy2777
[8] US Treasury, "Treasury Sanctions Network Supporting Iran's Oil Exports," SB0056, 20 Mar 2025. https://home.treasury.gov/news/press-releases/sb0056
[9] KSE Institute, "Russian Shadow Fleet Tracker, March 2026." https://kse.ua/about-the-school/news/russian-shadow-fleet-tracker-march-2026-share-of-russian-flagged-shadow-tankers-jumps-from-3-to-21-in-nine-months/
[10] Associated Press (via KVIA), "Greek shipper pleads guilty to smuggling Iranian crude oil and will pay $2.4 million fine," 6 Sep 2023. https://kvia.com/news/ap-national/2023/09/06/greek-shipper-pleads-guilty-to-smuggling-iranian-crude-oil-and-will-pay-2-4-million-fine/
[11] NPR, "What to know about Finland, Russia's 'shadow fleet' and a severed undersea cable," 31 Dec 2024. https://www.npr.org/2024/12/31/nx-s1-5243302/finland-russia-severed-undersea-cable-shadow-fleet
[12] Maritime Executive, "U.S. Issues 30-Day License for Delivery and Sale of Russian Oil at Sea" (Mar 2026); World Oil, "U.S. extends waiver for certain Russian oil cargo transactions," 18 May 2026. https://maritime-executive.com/article/u-s-issues-30-day-license-for-delivery-and-sale-of-russian-oil-at-sea ; https://worldoil.com/news/2026/5/18/u-s-extends-waiver-for-certain-russian-oil-cargo-transactions/
[13] UN Security Council, 9591st meeting, SC/15648, 28 Mar 2024 (draft renewing DPRK Panel of Experts fails owing to Russian veto). https://press.un.org/en/2024/sc15648.doc.htm
