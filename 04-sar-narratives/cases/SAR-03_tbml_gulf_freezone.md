# SAR Sample 3: Trade-Based Laundering and Export-Control Evasion via a Gulf Free-Zone Front Company

> ⚠️ **FICTIONAL.** This case is invented for training. The companies (Lone Star Precision Components LLC, Al Waha Horizon Trading FZE, and the payers), the people and the transactions do not exist; any resemblance is coincidental. Real places (Jebel Ali Free Zone, Bishkek, Yerevan) and real public guidance (FinCEN/BIS alerts, the BIS Common High Priority List) are referenced only for realism. It is a standalone case, not drawn from project 03's dataset. This is not a real filing.

## 1. Case summary

| Field | Value |
|---|---|
| Case number | MHB-FIU-2026-0388 |
| Filing type | Initial report |
| Source | TM alert (R07 invoice pattern: third-party payers outside the KYC profile) on 06/03/2026, plus an enhanced due diligence refresh |
| Subject 1 | Lone Star Precision Components LLC, Houston, TX, a distributor of industrial electronic components. Customer since 2019. Business account MHB77120458 |
| Subject 2 | Victor Hale, sole owner and managing member of Subject 1 |
| Subject 3 (non-customer) | Al Waha Horizon Trading FZE, Jebel Ali Free Zone (JAFZA), Dubai, UAE |
| Activity period | 01/12/2026 to 05/27/2026 |
| Amount | **$1,400,217.50**: $1,253,000.00 received from third parties, plus $147,217.50 paid back to Al Waha |
| SAR categories | Money laundering: trade-based money laundering; suspicious use of third-party transactors. Other: suspected export-control / sanctions evasion |
| Key term | FIN-2022-RUSSIABIS |
| SAR filed | 07/21/2026 (L2 determination on 06/30/2026) |

**In one paragraph:** from January 2026 a new foreign buyer, a UAE free-zone company formed in 2025, became Subject 1's largest customer. It bought integrated circuits and telecom modules that appear on the BIS Common High Priority List, which flags items Russia seeks for its weapons programs. The buyer never paid for them itself. Four unrelated companies in Kyrgyzstan, Hong Kong, Armenia and Turkey paid $1.25 million "on its behalf". Each time, Subject 1 then sent 15% of the payment back to the buyer as a "sales commission". Freight records show that 3 of the 7 shipments were sent on from Dubai to Kazakhstan and Russia.

## 2. Red flags (FinCEN/BIS joint alerts FIN-2022-Alert003 and FIN-2023-Alert004; FATF TBML guidance)
1. **Transshipment hub buyer.** A new customer in a UAE free zone with no prior relationship and no visible business presence.
2. **Third-party payments.** Payers in Kyrgyzstan, Armenia, Hong Kong and Turkey (all named in US advisories as diversion points to Russia) settle the invoices of a UAE buyer.
3. **High-priority items.** HS 8542.31 / 8542.39 (integrated circuits) and 8517.62 (communication modules) appear on the BIS Common High Priority List.
4. **Rebates.** A fixed 15% "commission" goes back to the buyer after each third-party payment. Combined with prices well above market, this moves value back to the buyer.
5. **Over-invoicing.** Unit prices on the invoices are 18% to 25% above the subject's own prices to US customers for the same part numbers *[simulated]*.
6. **Front-company profile.** Al Waha was registered in 03/2025 at a shared "flexi-desk" address used by more than 40 entities. Its director also sits on the board of a Moscow-registered electronics distributor (not designated) *[simulated open-source finding]*.
7. **Re-export.** Freight-forwarder bookings show shipments routed onward from Jebel Ali to Almaty, Kazakhstan and to Moscow, Russia *[simulated]*.
8. **Weak explanation.** The owner described the payers as Al Waha's "payment agents" and could not provide end-user statements.

## 3. Investigation steps taken
| # | Step | Result |
|---|---|---|
| 1 | Reviewed the R07 alert and 12 months of wire activity | New payer pattern starting 01/2026 (Table 1) |
| 2 | Compared with the KYC profile | Expected exports to Mexico and Canada only; no Middle East or Central Asia activity declared |
| 3 | Sanctions screening (OFAC SDN and consolidated lists, 50% rule, BIS Entity List) *[simulated]* | No match on any party, so no blocking or rejection was required. Activity is reported by SAR |
| 4 | Request for documents through the relationship manager *[simulated]* | 7 commercial invoices, air waybills and EEI (export) filings received. No end-user certificates |
| 5 | Document review *[simulated]* | EEI filings list Al Waha as the ultimate consignee; HS codes as in Table 3; invoice prices above Subject 1's US price list |
| 6 | Open-source and corporate-registry research *[simulated]* | Shared address; no website; director linked to a Russian distributor |
| 7 | Freight-forwarder data obtained through the customer *[simulated]* | 3 of 7 shipments were sent on to Kazakhstan and Russia |
| 8 | Internal referral | Sanctions/Export Controls team notified; relationship exit under review; enhanced monitoring in place |

## 4. Supporting transactions

**Table 1: third-party payments received** (all by wire into MHB77120458)

| # | Date | Payer | Country | Invoice ref (Al Waha) | Amount |
|---|---|---|---|---|---|
| 1 | 01/12/2026 | Ala-Too Trade Group OsOO | Kyrgyzstan | LSP-INV-1041 | $184,600.00 |
| 2 | 02/03/2026 | Silverline HK Trading Ltd | Hong Kong | LSP-INV-1047 | $212,450.00 |
| 3 | 02/24/2026 | Yerevan Tech Supply LLC | Armenia | LSP-INV-1052 | $96,300.00 |
| 4 | 03/16/2026 | Anka Elektronik Dis Ticaret AS | Turkey | LSP-INV-1058 | $238,900.00 |
| 5 | 04/07/2026 | Ala-Too Trade Group OsOO | Kyrgyzstan | LSP-INV-1063 | $175,250.00 |
| 6 | 04/28/2026 | Silverline HK Trading Ltd | Hong Kong | LSP-INV-1069 | $201,800.00 |
| 7 | 05/19/2026 | Yerevan Tech Supply LLC | Armenia | LSP-INV-1074 | $143,700.00 |
| | | | | **Total** | **$1,253,000.00** |

**Table 2: "sales commission" wires to Al Waha Horizon Trading FZE** (beneficiary bank in Dubai, UAE)

| Date | Linked payment | Amount | % of payment |
|---|---|---|---|
| 01/20/2026 | #1 ($184,600.00) | $27,690.00 | 15% |
| 02/11/2026 | #2 ($212,450.00) | $31,867.50 | 15% |
| 03/24/2026 | #4 ($238,900.00) | $35,835.00 | 15% |
| 05/06/2026 | #6 ($201,800.00) | $30,270.00 | 15% |
| 05/27/2026 | #7 ($143,700.00) | $21,555.00 | 15% |
| | **Total** | **$147,217.50** | |

**Table 3: goods shipped** (from the customer's documents *[simulated]*)

| Invoice | HS code | Description | Routing after Jebel Ali |
|---|---|---|---|
| LSP-INV-1041 | 8542.31 | Processors / controllers (integrated circuits) | Almaty, Kazakhstan |
| LSP-INV-1047 | 8542.39 | Other integrated circuits (FPGA) | Not stated |
| LSP-INV-1052 | 8517.62 | Communication modules | Not stated |
| LSP-INV-1058 | 8542.31 | Processors / controllers | Moscow, Russia |
| LSP-INV-1063 | 8542.39 | Other integrated circuits | Not stated |
| LSP-INV-1069 | 8542.31 | Processors / controllers | Moscow, Russia |
| LSP-INV-1074 | 8517.62 | Communication modules | Not stated |

## 5. SAR narrative (Part V)

> Meridian Harbor Bank (MHB) is filing this SAR to report suspected trade-based money laundering and possible evasion of US export controls on Russia (FIN-2022-RUSSIABIS) involving its customer Lone Star Precision Components LLC (Subject 1), a Houston, TX distributor of electronic components, its owner Victor Hale (Subject 2), and Al Waha Horizon Trading FZE (Subject 3), a company registered in the Jebel Ali Free Zone, Dubai, United Arab Emirates. Between 01/12/2026 and 05/27/2026, Subject 1's business account MHB77120458 received $1,253,000.00 in seven wires from four third-party companies in Kyrgyzstan, Hong Kong, Armenia and Turkey as payment for Subject 3's invoices, and sent $147,217.50 back to Subject 3 as "sales commissions." The activity was identified by a transaction monitoring alert on 06/03/2026 and a subsequent enhanced due diligence review.
>
> Subject 1 has banked with MHB since 2019. At account opening and at its last review it reported sales to industrial customers in the United States, with exports limited to Mexico and Canada. Subject 3 was not previously a customer of Subject 1. Corporate records show that Subject 3 was registered in March 2025 at a shared office address used by more than 40 companies, and that it has no website. One of its directors is also a director of an electronics distributor registered in Moscow, Russia.
>
> On 01/12/2026, Subject 1 received $184,600.00 from Ala-Too Trade Group OsOO, Bishkek, Kyrgyzstan, referencing invoice LSP-INV-1041 issued to Subject 3. On 01/20/2026 Subject 1 wired $27,690.00, 15 percent of that payment, to Subject 3's account at a bank in Dubai with the memo "sales commission." The same pattern continued: Silverline HK Trading Ltd, Hong Kong, paid $212,450.00 on 02/03/2026 and $201,800.00 on 04/28/2026; Yerevan Tech Supply LLC, Armenia, paid $96,300.00 on 02/24/2026 and $143,700.00 on 05/19/2026; Anka Elektronik Dis Ticaret AS, Turkey, paid $238,900.00 on 03/16/2026; and Ala-Too Trade Group OsOO paid $175,250.00 on 04/07/2026. Subject 1 sent further 15 percent payments to Subject 3 of $31,867.50 on 02/11/2026, $35,835.00 on 03/24/2026, $30,270.00 on 05/06/2026 and $21,555.00 on 05/27/2026. None of the paying companies is a party to the invoices, and MHB identified no relationship between them and Subject 3.
>
> In response to MHB's request for documentation, Subject 1 provided commercial invoices, air waybills and Electronic Export Information filings for the seven shipments. They list Subject 3 as ultimate consignee for integrated circuits (HS 8542.31 and 8542.39) and communication modules (HS 8517.62). These items appear on the BIS Common High Priority List. The invoiced unit prices are 18 to 25 percent higher than Subject 1's prices to US customers for the same part numbers. Freight-forwarder records show that the shipments under invoices LSP-INV-1041, LSP-INV-1058 and LSP-INV-1069 were sent on from Jebel Ali to Almaty, Kazakhstan and Moscow, Russia. Subject 2 stated that the paying companies act as Subject 3's "payment agents" and did not provide end-user statements.
>
> Payments by unrelated parties in jurisdictions identified as transshipment points to Russia, the inflated invoice prices combined with fixed rebates to the buyer, the newly formed free-zone consignee with links to a Russian distributor, and the onward shipment of high-priority items to Russia are consistent with trade-based money laundering used to obtain export-controlled goods for Russia. Screening found no parties on OFAC or BIS lists. MHB has referred the matter internally to its sanctions and export controls function, placed the account under enhanced monitoring, and is reviewing the relationship. Supporting documentation is retained by MHB and is available to law enforcement on request. Contact: MHB BSA/AML Investigations, case MHB-FIU-2026-0388.

## 6. Why this narrative works
- **Two typologies, one story.** The over-invoicing plus rebate (the TBML value transfer) and the diversion of goods (export-control evasion) are each supported by specific facts.
- **It is explicit about sanctions screening.** There were no list matches, so a SAR, not an OFAC blocking report, is the right channel. That distinction is often asked in OFAC-analyst interviews.
- **It uses the advisory key term** (FIN-2022-RUSSIABIS), so FinCEN can route the report to the right analysts.
- **It reads the same in Doha.** The same facts would make a sound STR to Qatar's Financial Information Unit (QFIU); only the form and the legal references change.
