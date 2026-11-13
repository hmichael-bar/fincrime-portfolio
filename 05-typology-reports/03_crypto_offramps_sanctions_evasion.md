---
title: "Typology Report 3: Crypto Off-Ramps for Sanctions Evasion"
subtitle: "OTC desks, nested exchanges, mixers and ruble stablecoins, with lessons from Hydra and Garantex"
date: "November 2026"
---

## Executive summary

Sanctioned actors use crypto less to *store* value than to **move it across the line between blocked and unblocked economies**, then turn it back into usable money. The weak point is the **off-ramp**: the place where crypto becomes fiat, or a widely accepted stablecoin, in a bank account. US enforcement since 2021 has therefore targeted **exchanges and off-ramps** (SUEX, Chatex, Garantex, Bitzlato, Cryptex/PM2BTC, Grinex) and **obfuscation services** (Blender, Tornado Cash, Sinbad) more than individual wallets [1]–[9].

The **Garantex** story is the template. A Moscow-operated exchange, sanctioned in April 2022, kept operating and allegedly processed at least **$96 billion** from 2019 to 2025 [2][3]. After a March 2025 takedown its operators allegedly moved customers to a successor, **Grinex**, and a ruble-backed stablecoin, **A7A5**. OFAC designated both networks in August 2025 [4]. Elliptic reports A7A5 passed **$100 billion** in on-chain transactions within a year of launch [10].

**Bottom line for banks:** Banks rarely touch a sanctioned wallet directly. They touch the **fiat leg**: wires to and from OTC desks, payment agents, VASPs with weak KYC, and individuals cashing out. Effective controls combine **blockchain analytics on VASP counterparties**, **behavioural monitoring of fiat accounts**, and **sanctions screening of wallet addresses** where OFAC lists them.

## 1. How the schemes work

### 1.1 The off-ramp chain

```
Sanctioned / illicit source           Obfuscation                     Off-ramp                        Fiat
(ransomware, darknet, Russian    →   mixers, chain-hopping,     →   OTC desk / nested exchange /  →  bank account of
 importer, DPRK hack proceeds)        bridges, privacy coins          P2P / payment agent              trader, mule or
                                                                       / stablecoin swap               front company
```

### 1.2 The main off-ramp types

| Type | What it is | Why it's abused | Example enforcement |
|---|---|---|---|
| **OTC brokers / desks** | Desks that match large crypto-to-fiat or crypto-to-crypto trades privately | Large tickets and cash settlement with little KYC. Often "nested" inside a big exchange | **SUEX OTC** was the first exchange designated by OFAC (21 Sept 2021). Treasury said over 40% of its known transaction history involved illicit actors [1] |
| **Nested exchanges** | A service that operates through accounts at a larger exchange, so the larger exchange sees one customer, not thousands | Borrows the host's liquidity while hiding end customers | **Bitzlato** was the first FinCEN §9714 "primary money laundering concern" order (18 Jan 2023) [6] |
| **Sanctions-tolerant exchanges** | Exchanges in permissive jurisdictions that keep serving sanctioned users | Direct ruble↔USDT conversion | **Garantex** (OFAC 5 Apr 2022; DOJ takedown 6–7 Mar 2025; redesignated with successor **Grinex** 14 Aug 2025) [2][3][4] |
| **Mixers** | Pool and re-distribute funds to break the transaction trail | Hide source before cash-out | **Blender.io** (first mixer designated, May 2022), **Tornado Cash** (Aug 2022), **Sinbad** (Nov 2023) [7][8] |
| **Stablecoins and "rails"** | Fiat-pegged tokens (USDT, and the ruble-pegged **A7A5**) | Fast, cross-border, dollar-like value. A7A5 bridges rubles into USDT | OFAC Aug 2025 designations of the A7A5 issuer network [4]. FATF reports most on-chain illicit activity now involves stablecoins [11] |
| **P2P markets and payment agents** | Individuals or agents who swap crypto for cash or bank transfers | Spread off-ramping across many bank accounts (mules) | FinCEN's March 2022 alert lists P2P and high-risk-jurisdiction exchangers as red flags [12] |

### 1.3 Mixers: law in motion

Mixers show why analysts must track **current legal status**. OFAC designated **Tornado Cash** on 8 Aug 2022 [8]. In *Van Loon v. Treasury* (Nov 2024), the Fifth Circuit held that its immutable smart contracts are not "property" that can be blocked. Treasury **delisted** Tornado Cash on **21 Mar 2025** [13]. Separately, a New York jury in **August 2025** convicted co-founder **Roman Storm** of conspiracy to operate an unlicensed money-transmitting business and deadlocked on the laundering and sanctions counts [14]. *For banks:* delisting removes the sanctions *prohibition*, but mixer exposure remains a **money-laundering risk factor**. FATF and FinCEN guidance still treats obfuscation as a red flag [11][12].

## 2. Red flags for banks

**Fiat-side (what a bank actually sees)**

- Incoming wires from **VASPs or OTC desks** in high-risk jurisdictions, or from VASPs with known exposure to sanctioned exchanges (Garantex/Grinex), followed by **rapid outflows** [12].
- **Many retail customers** receiving round-amount transfers from the same crypto counterparty: P2P cash-out mules.
- A trading or "IT services" company with sudden **crypto-sourced inflows** that pays importers of dual-use goods (crypto settling a TBML scheme; see Report 2).
- A customer's stated business is unrelated, yet the account shows **regular exchange of stablecoins** for USD or EUR at volumes inconsistent with income.
- **IP or device data** from Russia, Iran or DPRK on accounts claiming residence elsewhere [12].

**Chain-side (for banks with VASP clients or analytics tools)**

- **Direct or one-hop exposure** to OFAC-listed wallet addresses, sanctioned exchanges, mixers or darknet markets.
- **Chain-hopping** through bridges or swaps shortly after receiving funds from a high-risk source.
- Use of **A7A5** or swaps between ruble-linked tokens and USDT.
- The client VASP **cannot explain nested customers**, or refuses to share Travel Rule information [11].

## 3. Case examples

**Case 1: Hydra and Garantex (April 2022).** Germany's BKA shut down **Hydra**, then the world's largest darknet market, and seized 543 BTC (about €23 million). The US charged a Russian national, Dmitry Pavlov, alleged to have administered Hydra's servers [15]. The same day OFAC designated Hydra and **Garantex**, stating that Garantex had facilitated transactions for ransomware actors and darknet markets [2]. *Lesson:* darknet markets need exchange off-ramps, so the two were hit together.

**Case 2: Garantex keeps going, then falls (2022–2025).** Despite sanctions, Garantex kept operating. On 6–7 March 2025 US, German and Finnish authorities seized its domains and froze over $26 million. DOJ unsealed charges against its alleged technical administrator and former commercial director. Prosecutors allege the exchange processed **at least $96 billion** from 2019 to 2025, and that its operators **redesigned operations in 2023 to evade sanctions** [3]. These are allegations; the defendants are presumed innocent. *Lesson:* sanctioning an exchange does not stop it. Monitoring for **flows to its successors and wallet clusters** is what matters.

**Case 3: Grinex and the A7A5 ruble stablecoin (August 2025).** OFAC re-designated Garantex and designated **Grinex**, which Treasury said Garantex staff created to continue operations. It also designated executives and Russian and Kyrgyz companies tied to **A7A5**, a ruble-backed token issued in Kyrgyzstan [4]. Elliptic found A7A5 exceeded **$100 billion** in on-chain transactions in under a year, mainly bridging rubles and USDT, and later reported a steep fall in volumes as sanctions pressure grew [10]. *Lesson:* sanctioned states can **build their own rails**. Screening must cover token contracts and issuers, not just exchanges.

**Case 4: Bitzlato and PM2BTC: FinCEN's §9714 tool.** FinCEN's first order under §9714 of the Combating Russian Money Laundering Act named **Bitzlato** (Jan 2023) a primary money laundering concern tied to Russian illicit finance and barred covered institutions from transmitting funds to or from it [6]. In **September 2024** FinCEN did the same for **PM2BTC**, while OFAC designated the exchange **Cryptex** and its operator [5]. *Lesson:* these are **funds-transfer prohibitions** for US banks, not just sanctions, so payment filters must include them.

**Case 5: DPRK and the Bybit theft (February 2025).** The FBI attributed the theft of about **$1.5 billion** from the Bybit exchange to North Korea ("TraderTraitor"). It said the actors were converting the assets across thousands of addresses and asked VASPs and other private firms to block related addresses [16]. *Lesson:* the off-ramp problem is the same for proliferation finance. Large thefts are laundered through bridges, OTC brokers and, ultimately, fiat accounts.

**Case 6: Huione Group (2025).** FinCEN finalised a **§311** rule (Oct 2025) cutting Cambodia-based **Huione Group** off from the US financial system. It found Huione's businesses, including crypto services, laundered proceeds of cyber-scams and other crime [9]. *Lesson:* "payment platforms" that sit between crypto and fiat in permissive jurisdictions are a growing off-ramp category.

## 4. Detection and screening recommendations

1. **Screen wallet addresses.** Where OFAC lists digital-currency addresses on SDN entries, load them into payment and onboarding screening for customers that disclose wallets. OFAC's virtual-currency guidance sets the expectation [17].
2. **VASP counterparty due diligence.** Treat VASPs as financial-institution customers. Review licensing, Travel Rule compliance, nested-customer controls and **blockchain-analytics exposure reports** to sanctioned clusters (Garantex/Grinex, Cryptex, mixers) [11].
3. **§9714 and §311 filters.** Encode FinCEN special-measure targets (Bitzlato, PM2BTC, Huione) as **hard stops** in payment screening, separate from OFAC lists [5][6][9].
4. **Behavioural monitoring on the fiat leg.** Use rules for crypto-sourced funds followed by rapid wires abroad, fan-in/fan-out patterns typical of P2P mules, and mismatches between stated business and stablecoin flows [12].
5. **Track successors, not just names.** When an exchange is sanctioned, ask analytics vendors for **successor clustering** (e.g. Garantex → Grinex) and update monitoring.
6. **Know the legal status.** Maintain a dated register of mixer and service designations and delistings (e.g. Tornado Cash delisted Mar 2025). Keep risk-scoring obfuscation even when a sanction is lifted [13][14].
7. **SAR practice.** Include wallet addresses, transaction hashes, the VASP names, and the key term from the relevant FinCEN alert (e.g. "FIN-2022-RUSSIASANCTIONS" for the March 2022 alert) [12].

## Sources

[1] US Treasury, "Treasury Takes Robust Actions to Counter Ransomware," JY0364, 21 Sep 2021 (SUEX designation). https://home.treasury.gov/news/press-releases/jy0364
[2] US Treasury, "Treasury Sanctions Russia-Based Hydra, World's Largest Darknet Market, and Ransomware-Enabling Virtual Currency Exchange Garantex," JY0701, 5 Apr 2022. https://home.treasury.gov/news/press-releases/jy0701
[3] US Attorney's Office, E.D. Virginia, "Garantex Cryptocurrency Exchange Disrupted in International Operation," 7 Mar 2025. https://www.justice.gov/usao-edva/pr/garantex-cryptocurrency-exchange-disrupted-international-operation
[4] US Treasury, "Treasury Sanctions Cryptocurrency Exchange and Network Enabling Sanctions Evasion and Cyber Criminals," SB0225, 14 Aug 2025 (Garantex, Grinex, A7A5 network). https://home.treasury.gov/news/press-releases/sb0225
[5] US Treasury, "Treasury Takes Coordinated Actions Against Illicit Russian Virtual Currency Exchanges and Cybercrime Facilitator," JY2616, 26 Sep 2024 (Cryptex, Sergey Ivanov), and FinCEN, "Treasury Takes Coordinated Actions Against Illicit Russian Virtual Currency Exchanges and Cybercriminal Money Laundering Networks" (PM2BTC §9714 order). https://home.treasury.gov/news/press-releases/jy2616 ; https://www.fincen.gov/news/news-releases/treasury-takes-coordinated-actions-against-illicit-russian-virtual-currency
[6] FinCEN, "FinCEN Identifies Virtual Currency Exchange Bitzlato as a 'Primary Money Laundering Concern' in Connection with Russian Illicit Finance," 18 Jan 2023. https://www.fincen.gov/news/news-releases/fincen-identifies-virtual-currency-exchange-bitzlato-primary-money-laundering
[7] US Treasury, "Treasury Sanctions Mixer Used by the DPRK to Launder Stolen Virtual Currency," JY1933, 29 Nov 2023 (Sinbad; notes Blender.io as first mixer designated). https://home.treasury.gov/news/press-releases/jy1933
[8] US Treasury, "U.S. Treasury Sanctions Notorious Virtual Currency Mixer Tornado Cash," JY0916, 8 Aug 2022. https://home.treasury.gov/news/press-releases/jy0916
[9] FinCEN, "FinCEN Issues Final Rule Severing Huione Group from U.S. Financial System," Oct 2025. https://www.fincen.gov/news/news-releases/fincen-issues-final-rule-severing-huione-group-us-financial-system
[10] Elliptic, "A7A5: The ruble-backed stablecoin crosses $100 billion in transactions" (Jan 2026) and "The fall of A7A5: how sanctions strangled the ruble stablecoin" (2026). https://www.elliptic.co/insights/a7a5-the-ruble-backed-stablecoin-100-billion-in-transactions/ ; https://www.elliptic.co/insights/the-fall-of-a7a5-how-sanctions-strangled-the-ruble-stablecoin/
[11] FATF, *Targeted Update on Implementation of the FATF Standards on Virtual Assets and VASPs*, 26 Jun 2025. https://www.fatf-gafi.org/en/publications/Fatfrecommendations/targeted-update-virtual-assets-vasps-2025.html
[12] FinCEN, "FinCEN Advises Increased Vigilance for Potential Russian Sanctions Evasion Attempts," FIN-2022-Alert001, 7 Mar 2022. https://www.fincen.gov/sites/default/files/2022-03/FinCEN%20Alert%20Russian%20Sanctions%20Evasion%20FINAL%20508.pdf
[13] OFAC, Recent Actions, 21 Mar 2025 (Tornado Cash delisting); Steptoe, "Treasury Department Delists Tornado Cash Following the Fifth Circuit's Decision." https://ofac.treasury.gov/recent-actions/20250321 ; https://www.steptoe.com/en/news-publications/international-compliance-blog/treasury-department-delists-tornado-cash-following-the-fifth-circuits-decision.html
[14] Mayer Brown, "The Tornado Cash Trial's Mixed Verdict: Implications for Developer Liability," Aug 2025. https://www.mayerbrown.com/en/insights/publications/2025/08/the-tornado-cash-trials-mixed-verdict-implications-for-developer-liability
[15] US Department of Justice, "Justice Department Investigation Leads to Shutdown of Largest Online Darknet Marketplace," 5 Apr 2022. https://www.justice.gov/opa/pr/justice-department-investigation-leads-shutdown-largest-online-darknet-marketplace
[16] FBI / IC3, Public Service Announcement I-022625-PSA, "North Korea Responsible for $1.5 Billion Bybit Hack," 26 Feb 2025. https://ic3.gov/psa/2025/psa250226
[17] OFAC, *Sanctions Compliance Guidance for the Virtual Currency Industry*, Oct 2021. https://ofac.treasury.gov/media/913571/download
