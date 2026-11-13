# How It Works: Interview Prep (Project 05)

## The 30-second pitch

> "I wrote three typology reports in the format an FIU or a sanctions-intelligence firm uses: how the scheme works, red flags for banks, real enforcement cases, and the controls I'd build. They cover shadow-fleet oil shipping, trade-based laundering through Gulf free zones, and crypto off-ramps. Each one ties back to primary sources: OFAC, FinCEN, DOJ, FATF. The common thread is that evasion always breaks a consistency somewhere: the vessel's track doesn't match the paperwork, the invoice price doesn't match the market, or the crypto-sourced money doesn't match the customer's business. Detection means looking for those mismatches."

## Key terms (say these comfortably)

| Term | Plain meaning |
|---|---|
| **Typology** | A repeatable pattern of how a financial crime is done, used to write detection rules |
| **STS transfer** | Ship-to-ship transfer: moving cargo between tankers at sea, sometimes to hide origin |
| **AIS** | The radio transponder that broadcasts a ship's identity and position. "Going dark" means switching it off; "spoofing" means faking it. |
| **Price cap** | The G7/EU rule that Western services (insurance, shipping, finance) may handle Russian oil only if it's sold at or below a set price. US: $60. EU/UK: $44.10 from Feb 2026. |
| **TBML** | Trade-based money laundering: moving value by lying about trade (price, quantity, quality, existence) |
| **Transshipment** | Goods routed through a third country to hide the real destination |
| **CHPL / HS codes** | Common High Priority List: dual-use items found in Russian weapons, identified by Harmonized System customs codes |
| **Off-ramp** | Where crypto turns into usable fiat money |
| **Nested exchange** | A service operating through accounts at a bigger exchange, hiding its own customers |
| **§311 / §9714** | FinCEN powers to cut a foreign institution or exchange off from the US system. §9714 is Russia-specific (used on Bitzlato and PM2BTC). |
| **50 Percent Rule** | Entities ≥50% owned, in aggregate, by blocked persons are blocked too |

---

## Q1. "Explain how a shadow-fleet tanker evades sanctions, and where a bank would actually see it."

**Answer:** The tanker hides three things: **where it loaded**, **who owns it** and **what the oil sold for**. For the first, it switches off or spoofs AIS and then does a ship-to-ship transfer, so the cargo appears on a different ship with a "Malaysian" or "Iraqi" origin. For the second, each ship sits in a single-ship company in the Marshall Islands or Hong Kong, run by a newly formed manager. For the third, it avoids Western insurers and shippers altogether, so it never needs a price-cap attestation.

A bank rarely touches the oil. It sees the **payments around it**: freight and charter hire, ship sale proceeds when an old Western tanker is sold to a brand-new buyer, operating accounts of ship managers, and letters of credit on the cargo. So my first control is to **capture the IMO number on every shipping-related payment** and screen it. OFAC designated 183 vessels in one day in January 2025, and names change but IMO numbers don't. Then I'd enrich with AIS-gap and STS data.

## Q2. "What's the difference between the price cap and a sanctions ban? Why does it matter for compliance?"

**Answer:** A ban prohibits the trade outright. Iranian oil is close to that for US persons. The **price cap doesn't ban Russian oil**. It bans **Western services** for Russian oil sold *above* the cap. Compliance therefore turns on **evidence**: the attestation tiers, and itemised freight and insurance costs so a high price can't hide in "shipping fees". The Coalition's October 2024 advisory sets that out.

It matters because the rules **diverge and move**. The EU and UK cut the crude cap to $47.60 and then to $44.10 in February 2026, while the US stayed at $60. In 2026 the US also issued temporary general licences for Russian oil already at sea during the Iran-related price shock. A bank operating in New York and London can face two different caps on the same cargo, so the control has to record **which regime applied, on what date**.

## Q3. "How would you detect trade-based money laundering through a Dubai free-zone company?"

**Answer:** I test **four consistencies**.

1. **Price**: is the unit price far off market for that HS code? That's over- or under-invoicing.
2. **Product**: does the product fit the business? A textile trader buying microcontrollers is a mismatch.
3. **Route**: does the route make sense? US to Dubai to Kyrgyzstan for chips on the high-priority list is a classic transshipment route.
4. **Payer**: is the payer the buyer? Third-party and exchange-house payments are the shadow-banking signature.

FinCEN and BIS added very concrete flags in May 2023. Examples: a company incorporated after 24 February 2022 trading priority HS codes, or a freight forwarder listed as the ultimate consignee. The Zarringhalam case in June 2025 shows the Iranian version, where UAE front companies with falsified invoices netted payments for Iran.

**Nuance to add:** the UAE left the FATF grey list in 2024, and FinCEN explicitly warns against wholesale de-risking. So this is **company-level** due diligence, not a country ban.

## Q4. "Walk me through Garantex. Why didn't sanctions stop it?"

**Answer:** OFAC sanctioned Garantex in April 2022, the same day Germany took down Hydra, because it served ransomware gangs and darknet markets. Sanctions block US persons, but a Moscow-run exchange serving Russian customers didn't need US persons. It kept going, and DOJ alleges it processed at least **$96 billion** between 2019 and 2025. In March 2025, US, German and Finnish authorities seized its domains and DOJ charged two operators. Those are allegations.

The lesson is what came next. Treasury says Garantex staff set up a successor exchange, **Grinex**, and customers moved into **A7A5**, a ruble-backed stablecoin issued in Kyrgyzstan. OFAC designated that whole network in August 2025, and Elliptic counted over **$100 billion** in A7A5 transactions within a year. So screening on a name isn't enough. You need **blockchain analytics that cluster successors**, and controls on the **fiat leg**, where a bank actually sees the money.

## Q5. "Tornado Cash was delisted. Does that mean mixer exposure is fine now?"

**Answer:** No. It means one legal tool changed. In *Van Loon* (November 2024) the Fifth Circuit held that Tornado Cash's immutable smart contracts weren't "property" OFAC could block, and Treasury **delisted it in March 2025**. That removes the sanctions prohibition. But in August 2025 a jury convicted co-founder Roman Storm of conspiracy to run an unlicensed money-transmitting business, and FATF and FinCEN still treat obfuscation as a **money-laundering red flag**.

At a bank I'd keep mixer exposure as a **risk-scoring factor** and keep a **dated register** of designations and delistings. Then a reviewer can see what the rule was on the day of the transaction. It's the same point as the price cap: in sanctions, **the date is part of the fact**.

---

### Numbers worth memorising
Price cap: US $60 · EU/UK $44.10 (Feb 2026) · 183 vessels designated 10 Jan 2025 · dark fleet ≈ 500–1,000 ships (C4ADS) · UAE grey list Mar 2022 → Feb 2024 · FinCEN/BIS supplemental alert 19 May 2023 · Garantex ≥ $96bn alleged; sanctioned Apr 2022; takedown Mar 2025; Grinex/A7A5 designated 14 Aug 2025; A7A5 > $100bn on-chain · Bybit $1.5bn (DPRK, Feb 2025) · Tornado Cash: designated Aug 2022, delisted Mar 2025.
