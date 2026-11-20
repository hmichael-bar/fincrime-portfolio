---
title: "Malta: Dark-Fleet Activity at the EU's Biggest Flag"
subtitle: "Ship-to-ship transfers at Hurd's Bank, shadow-fleet bunkering, the Libyan fuel-smuggling precedent and what it means for KYC"
date: "OSINT desk study · H. Michael Bar Bourenane · November 2026 · public sources only"
---

## Key judgments

- **The waters around Malta are one of the Mediterranean's established ship-to-ship (STS) transfer zones for sanctions-sensitive oil.** Hurd's Bank, a shallow bank east of Malta, sits outside Maltese territorial waters and outside Malta's direct jurisdiction [1][2]. Researchers and trackers have named it alongside the Laconian Gulf, Ceuta and the Romanian coast as a transshipment area for Russian oil [3][4].
- **Malta is exposed from two sides: as a location and as a flag.** It is the EU's largest ship registry [5]. Malta-flagged tankers have been sold out of the register and into the Russian shadow fleet, reflagging to registries that do not apply EU sanctions [5].
- **Activity shifts quickly when pressure rises.** A maritime-AI firm reported that illicit STS transfers of Russian oil off Malta rose 220% in one quarter in 2023 [6]. By contrast, Kpler-based tracking by the KSE Institute counted only 18 STS operations with Russian oil products at the "Malta Light" area from Q1 2025 to Q2 2026, about 1% of the total, with little or no activity in 2026 [7]. Volume appears to have moved toward Cyprus and the Suez zone rather than disappeared [7].
- **Malta has a documented precedent of fuel smuggling laundered at sea.** In 2018 OFAC designated six people, 24 companies and seven vessels in a Libya–Malta–Italy fuel-smuggling network that reportedly earned more than €30 million [8][9]. The method included falsified fuel certificates and fishing boats used to move fuel at sea [9][10].
- **Malta's government has repeatedly pushed back on tougher EU maritime sanctions,** citing the competitiveness of the EU-flagged fleet [6][11]. For compliance teams, that means EU rules alone will not close the gap. Bank-level screening of vessels, owners and counterparties carries much of the load.

*Confidence:* moderate. The location, the OFAC action and the EU measures are well documented. Activity levels vary by data provider and period, and are presented as reported.

## 1. Why the waters off Malta attract shadow-fleet activity

| Factor | Why it matters |
|---|---|
| Geography | Malta sits on the main east–west Mediterranean shipping lane, between Suez, the Black Sea and Gibraltar. Tankers can pause there without a large detour. |
| Hurd's Bank | A shallow bank east of Malta (about 35°53′N, 14°45′E) where tankers can anchor in calm water outside territorial limits [1][2]. |
| Jurisdiction gap | Transfers just outside territorial waters fall outside Malta's direct enforcement reach [2][6]. |
| The flag | As the EU's largest registry, Malta flags many tankers that can be sold on into opaque ownership [5]. |
| Bunkering market | Shadow-fleet tankers have refuelled in international waters off Malta and Greece, which together made up 45% of observed shadow-fleet bunkering in early 2024 [12]. |

## 2. Documented activity

### STS transfers of Russian oil
- **2023:** Windward reported a 220% quarterly rise in illicit STS transfers of Russian oil off Malta, at the moment Malta was opposing new EU measures aimed at the practice [6].
- **2023:** The US sanctioned the Liberia-flagged tanker HS Atlantica for breaching the oil price cap. It was described as the first dark-fleet ship targeted by regulators, and it was then loitering in international waters off Malta [13].
- **2024:** Academic researchers writing in *Proceedings* identified Hurd's Bank as one of four Mediterranean and Black Sea STS hubs used to mask the origin of Russian oil [3][4].
- **2025–2026:** KSE Institute counted 18 Russian oil-product STS operations at "Malta Light" (3, 4, 6 and 5 per quarter through 2025), against 222 off Cyprus and 359 in the Suez zone, with almost none at Malta in 2026 [7].

**Analytic note:** The drop in Malta's share does not mean the risk is gone. It shows how quickly operators move to the next hub when attention rises. Screening that depends on a fixed list of "risky anchorages" goes stale fast.

### Other sanctioned trades through Hurd's Bank
- Maltese outlets reported Russian fuel transferred at Hurd's Bank and carried on to Venezuela while it was under US sanctions [2].
- In 2024 a Maltese outlet reported that large oil exports recorded as Maltese sales to Nigeria in fact took place by STS transfer at Hurd's Bank [14]. Official trade figures can therefore reflect transfers at sea, not Maltese supply.

### The flag: tankers leaving the Malta register
A 2025 Follow the Money investigation found that at least 230 ageing tankers owned in sanctioning countries were sold into the shadow fleet [15]. Among them, a Greek owner sold two Malta-flagged tankers, the *Fos Picasso* and the *Fos DaVinci*, to a Hanoi-based buyer in November 2024. Both moved to the Panama register [5].

## 3. The precedent: Libyan fuel smuggling (2016–2018)

| Element | What the public record shows |
|---|---|
| The network | OFAC designated Maltese nationals Darren Debono and Gordon Debono, Libyan national Fahmi Ben Khalifa and three others in 2018 [8][9]. |
| The scheme | A consortium formed in 2016 smuggled fuel from Zuwarah, Libya, to Malta and Italy, reportedly earning more than €30 million [9]. |
| The method | Fuel moved by sea, partly on fishing vessels, and was sold in European ports with falsified fuel certificates [8][10]. |
| Front businesses | OFAC also designated Malta-based companies, including a Valletta restaurant and trading and fishing firms owned or controlled by Darren Debono [9][16]. |
| Status | Two of the Maltese individuals, Rodrick Grech and Terence Micallef, were later removed from the SDN list [10][17]. Criminal cases were brought in Italy and Malta [10][17]. |

**Compliance relevance:** This case is a full laundering cycle on one page. Product is moved at sea, documents are falsified, and proceeds pass through ordinary local businesses. The same red flags apply to oil cargoes today.

## 4. How this investigation is done (OSINT method)

1. **Start from the area, not the ship.** Draw a box around Hurd's Bank and the approaches to Malta. Pull AIS history for tankers that loitered there (Global Fishing Watch, MarineTraffic or VesselFinder).
2. **Look for gaps.** Flag tankers whose AIS signal stops near the bank, or whose reported position jumps. DFRLab researchers note AIS alone is unreliable because ships spoof or go dark [4].
3. **Confirm with imagery.** Check satellite imagery (Copernicus Browser: Sentinel-1 radar works through cloud, Sentinel-2 optical shows pairs of hulls side by side) for vessels that were there with no AIS [4].
4. **Identify the ships.** Use IMO numbers, not names, which change. Check flag, owner and manager history in Equasis and IMO GISIS.
5. **Map the companies.** Look up registered owners and managers in OpenCorporates and OCCRP Aleph. Note single-ship companies, mass-registration addresses and recent ownership changes.
6. **Screen everything.** Run vessels, owners, managers and insurers against OFAC, EU, UK and OpenSanctions lists. The EU list alone reached more than 670 shadow-fleet vessels after its 21st package in July 2026 [18][19].
7. **Write it up carefully.** Report observed behaviour ("AIS gap of 31 hours at Hurd's Bank, consistent with an STS transfer"), not conclusions about intent.

## 5. KYC/EDD red flags

- Tankers, managers or charterers with recent activity at Hurd's Bank or other Mediterranean STS hubs, especially with AIS gaps during the stop.
- Vessels recently sold off the Malta, Greek or Cypriot register to newly formed buyers in third countries, followed by a flag change [5].
- Cargo documents showing Malta as origin for oil that Malta does not produce or refine at scale [14].
- Bunkering or ship-supply companies that service already-designated tankers. The EU began listing such suppliers in July 2026 [19].
- Price-cap attestations that are missing, late or signed by unknown intermediaries for Russian-origin products.
- Fuel trading or fishing businesses with cash-heavy accounts, links to Libyan ports, or ties to people named in the 2018 OFAC action.

## 6. Intelligence gaps

- How much activity left Malta for Cyprus and the Suez zone in 2026, and how much moved to transfers with no AIS record at all [7].
- Whether vessels recently reflagged into Malta have fully left shadow-fleet trading.
- The current scale of Libyan fuel smuggling by sea after the 2018 designations.

## Sources

[1] Finextra, "Heard about Hurd's Bank?" https://finextra.com/blogposting/20539/heard-about-hurds-bank
[2] MaltaToday, "Hurd's Bank, off Malta, acting as transfer point for Russian fuel destined for sanction-hit Venezuela." https://www.maltatoday.com.mt/news/national/96809/hurds_bank_off_maltas_coast_acting_as_transfer_point_for_russian_fuel_destined_for_venezuela
[3] The Maritime Executive, "Russia's Shadow Fleet Tactics Exposed," Jun 2024. https://maritime-executive.com/article/russia-s-shadow-fleet-tactics-exposed
[4] DFRLab, "Oil laundering at sea: defeating Russia's shadow fleet in the Mediterranean," Dec 2024. https://dfrlab.org/2024/12/20/oil-laundering-russia-osint/
[5] The Shift, "Tankers abandon Malta register to join Russian fleet busting oil sanctions," Feb 2025. https://theshiftnews.com/2025/02/07/tankers-abandon-malta-register-to-join-russian-fleet-busting-oil-sanctions/
[6] The Shift, "Illicit ship-to-ship Russian oil transfers off Malta up 220% – report." https://theshiftnews.com/?p=84205
[7] KSE Institute, "Ship-to-Ship Operations with Russian Oil: Geography, Logistics, and Sanctions," 2026. https://sanctions.kse.ua/wp-content/uploads/2026/09/Russia_STS_Opetations_AUG26.pdf
[8] US Treasury, "Treasury Sanctions International Network Smuggling Oil from Libya to Europe," 2018. https://home.treasury.gov/news/press-releases/sm0298
[9] FreightWaves, "Treasury sanctions Libyan oil smugglers," 2018. https://www.freightwaves.com/?p=155148
[10] MaltaToday, "Operation Dirty Oil: American sanctions delisting of Maltese port worker." https://www.maltatoday.com.mt/news/court_and_police/119523/operation_dirty_oil_american_sanctions_delisting_of_maltese_port_worker
[11] Greek City Times, "Greece & Malta Block EU's 20th Russia Oil Sanctions Package," Feb 2026. https://greekcitytimes.com/2026/02/11/greece-malta-block-eus-20th-russia-oil-sanctions-package/
[12] S&P Global Commodity Insights, "Russia's stealth tanker fleet refueling in European waters as EU mulls new curbs," May 2024. https://www.spglobal.com/energy/en/news-research/latest-news/crude-oil/050824-russias-stealth-tanker-fleet-refueling-in-european-waters-as-eu-mulls-new-curbs
[13] Lloyd's List, "Malta's loitering sanctioned tanker is first from dark fleet to be targeted by regulators," Dec 2023. https://www.lloydslist.com/LL1147521/Maltas-loitering-sanctioned-tanker-is-first-from-dark-fleet-to-be-targeted-by-regulators
[14] The Maltese Herald, "Large oil exports from Malta to Nigeria took place ship-to-ship in Hurd's Bank," Nov 2024. https://themalteseherald.com/2024/11/03/large-oil-exports-from-malta-to-nigeria-took-place-ship-to-ship-in-in-hurds-bank/
[15] The Guardian via inkl, "Shipowners have made £4.8bn selling tankers to Russian 'shadow fleet'." https://www.inkl.com/news/us-and-european-shipowners-sold-230-ageing-tankers-to-russian-shadow-fleet
[16] MaltaToday, "Maltese restaurant Scoglitti among list of companies hit by US fuel smuggling sanctions," 2018. https://www.maltatoday.com.mt/news/national/84847/maltese_restaurant_scoglitti_among_list_of_companies_hit_by_us_fuel_smuggling_sanctions
[17] MaltaToday, "Maltese national implicated in fuel smuggling ring removed from US sanctions list." https://www.maltatoday.com.mt/news/world/113977/maltese_national_implicated_in_fuel_smuggling_ring_removed_from_us_sanctions_list
[18] European Commission Representation in Malta, "EU adopts 20th package of sanctions against Russia," Apr 2026. https://malta.representation.ec.europa.eu/news/eu-adopts-20th-package-sanctions-against-russia-2026-04-23_en
[19] Hellenic Shipping News, "EU sanctions: 21st sanctions package against Russia," Jul 2026. https://www.hellenicshippingnews.com/eu-sanctions-21st-sanctions-package-against-russia/

<div class="footer-note">Open-source desk study compiled from public reporting, government statements and sanctions records. Inclusion of a person, company or vessel reflects public reporting or official action, not a finding of guilt; allegations are labelled as such, and later delistings are noted. Portfolio and teaching material, not legal advice.</div>
