# SAR Sample 1: Structuring Cash Deposits Below the CTR Threshold

> ⚠️ **FICTIONAL / SYNTHETIC.** The subject, the bank (Meridian Harbor Bank) and all transactions come from the synthetic dataset in `../03-transaction-monitoring` (customer C0298, alert ALT-00153). Investigative facts marked *[simulated]* are invented to show the process. This is not a real filing.

## 1. Case summary

| Field | Value |
|---|---|
| Case number | MHB-FIU-2026-0412 |
| Filing type | Initial report |
| Source | TM alert ALT-00153 (R01 structuring), escalated by L1 on 07/07/2026 |
| Subject | Olivia Ali, individual, age 51, administrative assistant (employer: Riverside Medical Group). Address: [synthetic], Hoboken, NJ |
| Account | Personal checking MHB91746874, opened 06/23/2010 |
| Activity period | 02/03/2026 to 06/16/2026 |
| Amount | **$126,340.00** in cash deposits (and $65,570.67 transferred out) |
| SAR categories | Structuring: multiple transactions below the CTR threshold; suspicious inquiry about BSA reporting. Other: suspicious use of multiple locations |
| SAR filed | 07/24/2026 (L2 determination on 07/16/2026, so within 30 days) |

**In one paragraph:** over three short bursts (Feb 3 to 5, Apr 24 to 26, Jun 11 to 14), the subject deposited $126,340 in cash as 14 deposits of $8,170 to $9,920 at 8 branches in New Jersey and New York, often at two or three branches on the same day. No deposit reached $10,000, so no CTR was filed. Within 2 to 3 days of each burst she sent most of the funds by ACH to her own account at another bank. Her only documented income is payroll of about $2,814 every two weeks.

## 2. Red flags
1. Repeated cash deposits just under $10,000 (14 of 14 between $8,170 and $9,920).
2. Several branches on the same day (for example 02/05: three deposits at BR07 Manhattan and BR06 Queens).
3. Cash volume of about 3.5 times her payroll for the period, from an occupation that does not involve cash. KYC expected cash activity: Low.
4. Quick transfer of the cash to an outside institution after each burst.
5. The same three-step pattern repeated about every two months.
6. Teller note *[simulated]*: on 04/25/2026 the subject asked the teller at BR07 whether deposits "over ten thousand get reported".

## 3. Investigation steps taken
| # | Step | Result |
|---|---|---|
| 1 | Reviewed the alert and the full 6-month history | Three structuring episodes found (Table 1) |
| 2 | Checked CTR filings for the subject | None filed. No deposit reached $10,000 |
| 3 | Reviewed the KYC profile and income | Payroll only: 13 credits, $36,587.71. No business or cash source declared |
| 4 | Reviewed deposit tickets and teller video *[simulated]* | The subject made all 14 deposits herself. No third-party depositors |
| 5 | Searched prior SARs, 314(a) lists and negative news *[simulated]* | No matches |
| 6 | Sent a 314(b) request to Pinnacle Bank, the receiving bank *[simulated]* | Response pending at filing |
| 7 | Considered an RFI | Not sent. Asking the customer about the cash would risk tipping her off |

## 4. Supporting transactions
**Table 1: cash deposits and outbound transfers** (full CSV: `../supporting_data/SAR-01_structuring_transactions.csv`)

| Txn | Date | Time | Description | Amount | Location |
|---|---|---|---|---|---|
| T010336 | 02/03/2026 | 10:53 | Cash deposit | $9,920.00 | BR07 Manhattan, NY |
| T010490 | 02/03/2026 | 14:55 | Cash deposit | $9,900.00 | BR04 Hoboken, NJ |
| T011021 | 02/05/2026 | 09:04 | Cash deposit | $9,690.00 | BR07 Manhattan, NY |
| T011081 | 02/05/2026 | 11:26 | Cash deposit | $9,420.00 | BR06 Queens, NY |
| T011147 | 02/05/2026 | 13:57 | Cash deposit | $9,000.00 | BR06 Queens, NY |
| T012037 | 02/08/2026 | 13:59 | ACH debit to own account, Pinnacle Bank | $17,729.83 | Online |
| T036411 | 04/24/2026 | 17:09 | Cash deposit | $8,400.00 | BR04 Hoboken, NJ |
| T036564 | 04/25/2026 | 11:54 | Cash deposit | $8,170.00 | BR07 Manhattan, NY |
| T036603 | 04/25/2026 | 13:38 | Cash deposit | $8,300.00 | BR03 Paterson, NJ |
| T036801 | 04/26/2026 | 09:45 | Cash deposit | $8,200.00 | BR05 Brooklyn, NY |
| T036900 | 04/26/2026 | 14:32 | Cash deposit | $8,600.00 | BR02 Newark, NJ |
| T037823 | 04/29/2026 | 17:25 | ACH debit to own account, Pinnacle Bank | $29,568.32 | Online |
| T052283 | 06/11/2026 | 19:41 | Cash deposit | $9,400.00 | BR05 Brooklyn, NY |
| T052309 | 06/12/2026 | 08:14 | Cash deposit | $9,800.00 | BR02 Newark, NJ |
| T052532 | 06/12/2026 | 17:12 | Cash deposit | $9,100.00 | BR08 Yonkers, NY |
| T053027 | 06/14/2026 | 10:34 | Cash deposit | $8,440.00 | BR01 Jersey City, NJ |
| T053942 | 06/16/2026 | 19:20 | ACH debit to own account, Pinnacle Bank | $18,272.52 | Online |

**Table 2: episode summary**

| Episode | Dates | Deposits | Cash total | Branches | Transferred out |
|---|---|---|---|---|---|
| 1 | 02/03 to 02/05 | 5 | $47,930.00 | 3 | $17,729.83 (02/08) |
| 2 | 04/24 to 04/26 | 5 | $41,670.00 | 5 | $29,568.32 (04/29) |
| 3 | 06/11 to 06/14 | 4 | $36,740.00 | 4 | $18,272.52 (06/16) |
| **Total** | | **14** | **$126,340.00** | **8** | **$65,570.67** |

## 5. SAR narrative (Part V)

> Meridian Harbor Bank (MHB) is filing this SAR to report suspected structuring of cash deposits by Olivia Ali (subject), an administrative assistant, in personal checking account MHB91746874. Between 02/03/2026 and 06/14/2026 the subject made 14 cash deposits totalling $126,340.00, each between $8,170.00 and $9,920.00, at eight MHB branches in New Jersey and New York. The deposits appear designed to avoid Currency Transaction Report filing. The activity was identified through transaction monitoring alert ALT-00153 and a review of the account from 01/01/2026 to 06/30/2026.
>
> The subject has held the account since 06/23/2010. At account opening she reported employment as an administrative assistant with Riverside Medical Group and low expected cash activity. Her only regular credits are payroll deposits averaging $2,814.44 every two weeks ($36,587.71 in total for the review period).
>
> The cash deposits occurred in three groups. From 02/03/2026 to 02/05/2026 the subject deposited $47,930.00 in five deposits at three branches, including $9,920.00 at the Manhattan, NY branch and $9,900.00 at the Hoboken, NJ branch on 02/03/2026, and three deposits totalling $28,110.00 at the Manhattan and Queens, NY branches on 02/05/2026. On 02/08/2026 she sent $17,729.83 by ACH to an account in her name at Pinnacle Bank. From 04/24/2026 to 04/26/2026 she deposited $41,670.00 in five deposits of $8,170.00 to $8,600.00 at five different branches, and on 04/29/2026 sent $29,568.32 to the same Pinnacle Bank account. On 04/25/2026 the subject asked a teller at the Manhattan branch whether deposits over $10,000 are reported. From 06/11/2026 to 06/14/2026 she deposited $36,740.00 in four deposits at four branches, and on 06/16/2026 sent $18,272.52 to the Pinnacle Bank account.
>
> None of the deposits exceeded $10,000, and no CTR was filed on the subject during the period. Bank records and teller video show that the subject made each deposit in person. The cash deposits are about 3.5 times her payroll income for the same period, and MHB has no information on a source of cash consistent with her stated occupation. The repeated use of different branches on the same day, amounts just below the reporting threshold, the subject's question about reporting, and the transfer of funds to another institution shortly after each group of deposits are consistent with structuring to evade reporting requirements (31 U.S.C. 5324). The source of the cash is unknown.
>
> MHB has placed the account under enhanced monitoring and sent a 314(b) request to Pinnacle Bank. Supporting documentation, including deposit tickets, teller notes and video, is retained by MHB and is available to law enforcement on request. Contact: MHB BSA/AML Investigations, case MHB-FIU-2026-0412.

## 6. Why this narrative works
- **Who:** the subject, her occupation, account number, and the other institution involved.
- **What:** 14 cash deposits and 3 outbound ACH transfers, with exact amounts.
- **When:** exact dates, in chronological order.
- **Where:** branches by city and state; the receiving bank.
- **Why it is suspicious:** amounts just under the threshold, several branches, the reporting question, and cash inconsistent with income. Stated as facts, with no guess at what crime produced the cash.
- **How:** branch-hopping over consecutive days, then consolidation at another bank.
