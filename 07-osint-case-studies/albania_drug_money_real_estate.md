---
title: "Albania: Cocaine Profits in Concrete"
subtitle: "How Albanian trafficking networks launder drug proceeds through construction, real estate and tourism"
date: "OSINT desk study · H. Michael Bar Bourenane · November 2026 · public sources only"
---

## Key judgments

- **Albanian-speaking networks have moved from street-level and cannabis trafficking to wholesale cocaine brokerage.** They buy directly in Ecuador and Colombia and move product through Europe's main ports. The profits return home, and a large share is invested in construction, real estate and coastal tourism [1][2].
- **The real-estate sector is the main laundering channel.** The Global Initiative Against Transnational Organized Crime (GI-TOC) estimates that around €700 million is laundered in Albania each year [3]. Expert estimates cited in the Albanian press put real-estate laundering at about €500 million in 2019 alone, and up to €1.6 billion over 2016–2019 [2].
- **The Tirana high-rise boom is the most visible red flag.** Towers above 10 floors are being built faster than local incomes or mortgage lending would explain. Albania's special anti-corruption prosecutor, SPAK, has opened cases directly linking construction businessmen and towers to cocaine trafficking, including the "Aruba Corporation" case [4][5].
- **Regulatory pressure has eased but not removed the risk.** FATF grey-listed Albania in February 2020 and delisted it in October 2023, after the government dropped a proposed fiscal amnesty that the IMF and EU had warned could launder criminal wealth [6][7]. Real-estate-agent supervision is new and still incomplete [6].

*Confidence:* moderate. The volume estimates are rough and come from secondary reporting of GI-TOC and expert work. Links between specific towers and drug money are mostly allegations under investigation, and are labelled as such.

## 1. From cannabis to cocaine

| Phase | What changed |
|---|---|
| 1990s–2000s | After the collapse of communism and the 1997 pyramid-scheme crisis, smuggling of people, weapons and heroin went through Albania toward Italy. |
| 2000s–2014 | Large-scale cannabis cultivation peaked. The 2014 police operation in Lazarat, a village producing an estimated hundreds of tonnes a year, marked the end of that era. |
| 2015–present | Albanian brokers built direct supply relationships in Latin America, especially Ecuador, and placed members in Rotterdam, Antwerp, Hamburg, Valencia and Gioia Tauro. Europol operations since 2020 have dismantled large Albanian-led cocaine networks, including the group known as "Kompania Bello". |
| 2025 | Europe-wide raids targeted an Albanian-run syndicate accused of moving about 28 tonnes of cocaine from Latin America to European ports and laundering profits through luxury resorts and property in Albania [8]. |

**Analytic note:** Wholesale cocaine generates far more cash than cannabis ever did, and in euros, often in bulk. That cash needs a destination that absorbs large sums, holds value and is socially respectable. In a fast-growing, cash-tolerant economy, property development is that destination.

## 2. How the money gets into concrete

| Stage | Method | Detail |
|---|---|---|
| Placement | Bulk cash smuggling and cash deposits | Euros carried back by couriers or by road through the Balkans, then deposited through businesses with high cash turnover. |
| Placement | Remittance cover | Funds disguised as diaspora remittances from Italy, the UK, Greece and Germany. |
| Layering | Shell construction companies | Newly formed developers with little capital and no track record win permits and start large projects [3]. |
| Layering | Loan-back and guarantees | Criminal associates guarantee bank loans for construction firms, or "lend" cash to developers [9]. |
| Layering | Pre-sale apartments | Units are sold off-plan for cash to nominees, which converts cash into property contracts. |
| Integration | Tourism and hospitality | Hotels, beach resorts and restaurants on the Durrës, Vlorë and Sarandë coast, which are cash-intensive and seasonal, provide ongoing laundering capacity [8]. |
| Integration | Under-declared sale prices | Property sold at a declared price below market, with the difference paid in cash, hides both the source of funds and its value. |

## 3. The Tirana tower boom: indicators

- Dozens of high-rise permits were issued in Tirana within a few years. Reporting says a significant share of projects over 10 floors are believed to be backed by criminal syndicates. This is an allegation, not a judicial finding [4].
- Prices in central Tirana rose sharply despite modest local wages, and many units remain empty, which is consistent with property bought as a store of value rather than to live in.
- SPAK's "Aruba Corporation" case concerns alleged links between drug trafficking and tower construction in Tirana. SPAK has also imposed precautionary measures on several construction and real-estate businessmen over suspected trafficking links [5][2].

**How an analyst would check this (OSINT method):**
1. **Permit records:** list high-rise permits from Tirana municipality and the National Territorial Council by developer and date.
2. **Company records:** pull each developer from the Albanian National Business Center (QKB). Check incorporation date, share capital, shareholders and directors, and flag new firms with minimal capital running €10m+ projects.
3. **Satellite and street-level imagery:** use Sentinel-2, Google Earth history and Street View to confirm build speed and occupancy, such as lit windows and parked cars, against declared sales.
4. **Network links:** cross-reference shareholders and directors against SPAK indictments, Europol press releases, sanctions lists and local-language investigative reporting (BIRN, Exit News, Faktoje).

## 4. Regulatory context

- **FATF:** grey-listed in February 2020 and removed in October 2023. Analysts link the delisting closely to the government withdrawing its proposed fiscal amnesty [6][7].
- **Real-estate supervision:** risk-based supervision of notaries and real-estate agents has been introduced, but MONEYVAL still flagged gaps in 2023 [6].
- **Enforcement:** SPAK has become the main tool, using decrypted Sky ECC and EncroChat messages shared by European partners to build cases against traffickers and their business associates.
- **US sanctions:** OFAC has designated Albanian-linked trafficking groups, including the Kosovar-Albanian Kelmendi organisation under the Kingpin Act and the Hysa family's casino businesses in Mexico [10].

## 5. Red flags for KYC and EDD teams

- Albanian or diaspora construction companies under three years old that run large projects with little share capital or bank financing.
- Payments for Albanian property funded by cash deposits or by many small remittances from different senders in Western Europe.
- Third-party loan guarantees from individuals with no clear source of wealth.
- Off-plan apartments bought in bulk by nominees or by companies with no other activity.
- Hospitality businesses on the coast whose revenues stay flat across tourist and off seasons.
- Customers or counterparties named in SPAK proceedings, Europol releases or OFAC narcotics designations, including their relatives and close associates.
- Links to Ecuador-based import/export companies, especially in bananas and seafood, the classic cocaine cover cargo.

## 6. Intelligence gaps

- No authoritative estimate exists of the share of Tirana high-rise stock financed by criminal proceeds. Current figures are expert extrapolations.
- The outcomes of the 2025 cross-border case and the "Aruba Corporation" case will show whether prosecutions reach developers as well as couriers.
- Displacement risk: as Tirana comes under scrutiny, funds may shift to coastal resorts, Montenegro or Dubai.

## Sources

[1] GI-TOC, Illicit financial flows in Albania (Hotspots series). https://see.globalinitiative.net/hotspots/iffs/reports/albania.pdf
[2] Albanian Daily News, "Drug money in Albania laundered in construction, tourism: GI report." https://albaniandailynews.com/news/drug-money-in-albania-laundered-in-construction-tourism-gi-report
[3] Euronews Albania, "Money laundering in Albania estimated at around €700 million per year, GI-TOC report." https://euronews.al/en/?p=13904
[4] Tirana Times, "Dirty money in the skyline: Albania's tower boom and the laundering of criminal wealth." https://www.tiranatimes.com/dirty-money-in-the-skyline-albanias-tower-boom-and-the-laundering-of-criminal-wealth/
[5] Alfa Press, "'Aruba Corporation': SPAK strikes billion-dollar drug and tower scheme in Tirana." https://alfapress.al/english/aktualitet/korporata-aruba-spak-godet-skemen-e-miliardave-te-s-dhe-kullave--i196073
[6] Basel Institute on Governance, Basel AML Index, Albania country profile. https://baselgovernance.org/countries/albania
[7] Faktoje, fact-check on Albania's FATF grey-list exit. https://en.faktoje.al/?p=5344
[8] Tirana Times, "European raids hit Albanian cartel, millions laundered in resorts." https://www.tiranatimes.com/european-raids-hit-albanian-cartel-millions-laundered-in-resorts
[9] Osservatorio Balcani Caucaso, "Albania: a development model based on money laundering?" https://www.balcanicaucaso.org/en/cp_article/albania-a-development-model-based-on-money-laundering/
[10] US Treasury, OFAC Counter Narcotics sanctions program; OCCRP, "US blacklists Balkan businessman Naser Kelmendi." https://ofac.treasury.gov/sanctions-programs-and-country-information/counter-narcotics-trafficking-sanctions

<div class="footer-note">Open-source desk study compiled from public reporting, NGO research, regulatory reports and sanctions records. No private individual is named except where an official sanctions action names them. References to investigations are allegations unless a conviction is stated. Portfolio and teaching material, not legal advice.</div>
