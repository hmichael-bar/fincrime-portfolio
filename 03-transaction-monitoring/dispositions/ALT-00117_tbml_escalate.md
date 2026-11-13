# ALT-00117 | R07 Trade-Based ML: Invoice Pattern | ESCALATE to L2 + Sanctions/Export Control Referral

> **Synthetic case.** All names, accounts and transactions are fictional. *[simulated]* = a check this project does not model.

| Field | Value |
|---|---|
| Alert ID | ALT-00117 (related: R02/R04/R07 alerts, Jan to Jun) |
| Rule | R07: invoice-referenced wires meeting at least 2 TBML conditions |
| Alert date | 2026-01-30 |
| Customer | C0206, Chen Imports LLC, used-clothing importer, FL (branch BR15, Miami) |
| KYC | Expected goods: **used clothing**. Expected countries: **Pakistan** (supplier Pacific Rag Exporters). Risk rating: High |
| Analyst / date | L1-ANALYST-01 / 2026-07-09 |
| **Decision** | **Escalate. Possible TBML / third-party settlement with a sanctions-evasion nexus** |

## 1. Why the alert fired
Three of the four R07 conditions were met in January:

| Txn | Date | Type | Amount | Counterparty | Country | Memo |
|---|---|---|---|---|---|---|
| T001430 | Jan 4 | Wire in | $84,735.88 | Ala-Too Logistics OSOO | **Kyrgyzstan** | INV-2026-0226 PAYMENT ON BEHALF OF BUYER |
| T001629 | Jan 4 | Wire out | $97,043.75 | Hamriyah Polar Star **FZC** | UAE | INV-2026-0222 **marine engines** |
| T002389 | Jan 7 | Wire out | $70,920.00 | Al Rasheed Industrial Supplies **FZCO** | UAE | INV-2026-0226 **marine engines** |
| T008840 | Jan 30 | Wire out | $70,920.00 | Hamriyah Polar Star **FZC** | UAE | INV-2026-0223 **marine engines** |

## 2. Look-back (6 months): all invoice-referenced trade wires
| Date | Dir. | Amount | Counterparty | Country | Invoice |
|---|---|---|---|---|---|
| Jan 4 | IN | $84,735.88 | Ala-Too Logistics OSOO | Kyrgyzstan | 0226 "on behalf of buyer" |
| Jan 4 | OUT | $97,043.75 | Hamriyah Polar Star FZC | UAE | 0222 |
| Jan 7 | OUT | $70,920.00 | Al Rasheed Industrial Supplies FZCO | UAE | 0226 |
| Jan 30 | OUT | $70,920.00 | Hamriyah Polar Star FZC | UAE | 0223 |
| Mar 31 | IN | $74,602.46 | Ararat Machinery LLC | Armenia | 0220 "on behalf of buyer" |
| Apr 3 | OUT | $70,920.00 | Victoria Harbour Components Ltd | Hong Kong | 0220 |
| Apr 5 | IN | $92,659.30 | Ala-Too Logistics OSOO | Kyrgyzstan | 0224 "on behalf of buyer" |
| Apr 9 | OUT | $80,354.60 | Hamriyah Polar Star FZC | UAE | 0224 |
| Jun 9 | OUT | $63,760.87 | Hamriyah Polar Star FZC | UAE | 0219 |
| Jun 11 | OUT | $103,742.23 | Hamriyah Polar Star FZC | UAE | 0225 |
| Jun 14 | IN | $123,711.25 | Ararat Machinery LLC | Armenia | 0221 "on behalf of buyer" |
| Jun 17 | OUT | $109,107.19 | Al Rasheed Industrial Supplies FZCO | UAE | 0221 |
| **Totals** | | **IN $375,708.89 (4) / OUT $666,768.64 (8)** | | | |

At the same time, the customer's normal business continues: 14 wires to its declared Pakistani clothing supplier ($743,770) and about 49 domestic ACH receipts from US buyers.

## 3. Red flags (FATF / FinCEN TBML indicators)
1. **Goods inconsistent with the business.** A used-clothing importer is paying for "marine engines", which is industrial machinery outside its line of business and potentially an export-controlled or dual-use item.
2. **Free-zone counterparties.** Two UAE free-zone entities (FZC / FZCO) and a Hong Kong trading company. Free zones offer light ownership transparency, which makes them a common way to route goods and payments.
3. **Third-party payments.** Buyers in **Kyrgyzstan and Armenia** pay "on behalf of" an unnamed buyer, and these payments match invoice numbers on outgoing wires. The bank cannot see who the real buyer is.
4. **Sanctions-evasion corridor.** Kyrgyzstan, Armenia, UAE and Hong Kong appear repeatedly in US advisories on diversion of goods to Russia (for example the joint FinCEN/BIS alerts on export-control evasion).
5. **Repeated identical amount.** $70,920.00 appears three times across three different counterparties and countries.
6. **Invoice sequence out of order.** Invoice 0219 is paid in June after 0226 was paid in January, and invoice 0226 shows up both on a January inbound payment and a January outbound wire. These are signs of invoices made up to justify payments rather than issued for real shipments.
7. **Value mismatch.** Outflows for the "marine engines" ($667K) far exceed the third-party inflows ($376K). The difference is funded from the customer's clothing revenues, which suggests commingling.

## 4. Decision and rationale
**Escalated.** The customer is settling trades in goods unrelated to its business, through free-zone intermediaries, partly paid for by unrelated third parties in jurisdictions linked to sanctions evasion. This fits trade-based money laundering and possibly export-control or sanctions evasion. L1 cannot clear it without trade documents.

## 5. Recommendations to L2
- **Referral to the Sanctions / Export Controls team.** Screen all counterparties, vessels and ports. Check whether "marine engines" fall under BIS Common High Priority List items *[simulated]*.
- Request invoices, bills of lading, packing lists and end-user information for the 8 outbound "marine engine" wires (this is due diligence on the activity, done through the relationship manager so the customer is not tipped off about a SAR).
- Check pricing: compare invoice values against typical unit prices for marine engines.
- Consider a SAR covering Jan 4 to Jun 17. If the documents do not support genuine trade, consider exiting the relationship.
