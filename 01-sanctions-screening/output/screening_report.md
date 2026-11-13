# Sanctions Screening Report

*Generated 2026-11-13 06:07 UTC - threshold 85 - 19,563 SDN + 486 non-SDN entries, 41,396 names incl. aliases*

| Disposition | Customers |
|---|---|
| True Match | 14 |
| Potential Match - escalate | 6 |
| False Positive | 6 |
| No Match | 14 |

## Summary

| ID | Customer | Disposition | Score | Best list match | Program |
|---|---|---|---|---|---|
| C001 | Moammar Abu Minyar El-Gaddafi | True Match | 100 | QADHAFI, Muammar | LIBYA2 |
| C002 | Usama bin Muhammad bin Laden | True Match | 95 | BIN LADIN, Usama bin Muhammad bin Awad | SDGT |
| C003 | Bashar Hafez al-Assad | True Match | 100 | AL-ASSAD, Bashar | PAARSSR-EO13894 |
| C004 | Sayyed Hassan Nasrullah | True Match | 100 | NASRALLAH, Hasan | SDGT |
| C005 | Qassem Suleimani | True Match | 97 | SOLEIMANI, Qasem | SDGT, NPWMD, IRGC, IFSR |
| C006 | Saif el-Islam Gadhafi | True Match | 100 | QADHAFI, Saif al-Islam | LIBYA2 |
| C007 | Rami Makhlouf | True Match | 100 | MAKHLUF, Rami | PAARSSR-EO13894 |
| C008 | Ali Abdallah Salih | True Match | 100 | SALEH, Ali Abdullah | YEMEN |
| C009 | Mousa Mohamed Abu Marzouk | True Match | 97 | ABU MARZOOK, Mousa Mohammed | SDGT |
| C010 | معمر القذافي | True Match | 100 | QADHAFI, Muammar | LIBYA2 |
| C011 | أسامة بن لادن | Potential Match - escalate | 100 | BIN LADIN, Usama bin Muhammad bin Awad | SDGT |
| C012 | Bank Melli Iran | True Match | 100 | BANK MELLI IRAN | IRAN, SDGT, IFSR |
| C013 | Al-Qard Al-Hasan Association | True Match | 100 | AL-QARD AL-HASSAN ASSOCIATION | SDGT |
| C014 | Oleg V. Deripaska | True Match | 95 | DERIPASKA, Oleg Vladimirovich | UKRAINE-EO13661, UKRAINE-EO13662 |
| C015 | Levant Horizon Trading FZE | Potential Match - escalate | - | - | - |
| C016 | Mahan Air Co | True Match | 100 | MAHAN AIR | SDGT, NPWMD, IFSR |
| C017 | Sheikh Mohamed Ali Hassan | False Positive | 96 | AL-WARDIAN, Hassan | SDGT |
| C018 | Ahmed Hussein | Potential Match - escalate | 95 | AL-KHODAIR, Ahmad Hussein | IRAQ2 |
| C019 | Ali Hassan | False Positive | 100 | FADHIL, Mustafa Mohamed | SDGT |
| C020 | Youssef Ibrahim | False Positive | 97 | EBRAHIMI, Yousef | IRAN-EO13902 |
| C021 | Fatima al-Assad | No Match | - | - | - |
| C022 | Omar Abdel Rahman | False Positive | 100 | AL RAHMAN, Shaykh Umar Abd | SDGT |
| C023 | Khalid Mahmoud | Potential Match - escalate | 100 | KHAN, Mustafa Hajji Muhammad | SDGT |
| C024 | Youssef Nasrallah | No Match | - | - | - |
| C025 | Sara Soleimani | No Match | - | - | - |
| C026 | Hassan Ali Khan | False Positive | 95 | FADHIL, Mustafa Mohamed | SDGT |
| C027 | Abdullah Yasin | No Match | - | - | - |
| C028 | Ibrahim Awad | Potential Match - escalate | 92 | AL-FAY, Ibrahim Ali 'Awad | SDGT |
| C029 | Muhammad Qasim | False Positive | 100 | QASIM, Mohammed | SDGT |
| C030 | Hannibal Gaddafi Restaurant LLC | Potential Match - escalate | 95 | GADDAFI, Hannibal | LIBYA2 |
| C031 | Emily Carter | No Match | - | - | - |
| C032 | Daniel Okafor | No Match | - | - | - |
| C033 | Priya Raman | No Match | - | - | - |
| C034 | Lucas Moreau | No Match | - | - | - |
| C035 | Layla Mansour | No Match | - | - | - |
| C036 | Tariq Benali | No Match | - | - | - |
| C037 | Hana Kobayashi | No Match | - | - | - |
| C038 | Grace Mensah | No Match | - | - | - |
| C039 | Blue Harbor Coffee Roasters LLC | No Match | - | - | - |
| C040 | Nile Valley Imports Inc | No Match | - | - | - |

## Alert details

### C001 - Moammar Abu Minyar El-Gaddafi  ->  **True Match**
Normalised as `muammar abuminyar qadhafi`; DOB 1942; nationality Libya
- **100** - QADHAFI, Muammar (individual; LIBYA2; SDN-12606) - *True Match*: Strong name match, birth year and nationality consistent - block/reject and report
    - Matched list alias (aka) 'AL-QADHAFI, Muammar Abu Minyar', not only the primary name
    - Identical after normalisation
    - Customer name: Joined kunya 'abu minyar' -> 'abuminyar'
    - Customer name: Ignored name particles: el
    - Customer name: 'moammar' treated as transliteration variant of 'muammar'
    - Customer name: 'gaddafi' treated as transliteration variant of 'qadhafi'
    - check: DOB year match only (1942; list: 1942) - obtain full DOB / ID document
    - check: Nationality/country consistent (Libya)
- **94** - QADHAFI, Ayesha (individual; LIBYA2; SDN-12610) - *False Positive*: Name similar but date of birth does not match the list entry
    - Matched list alias (aka) 'QADHAFI, Aisha Muammar Muhammed Abu Minyar', not only the primary name
    - Customer name: Joined kunya 'abu minyar' -> 'abuminyar'
    - Customer name: Ignored name particles: el
    - Customer name: 'moammar' treated as transliteration variant of 'muammar'
    - Customer name: 'gaddafi' treated as transliteration variant of 'qadhafi'
    - List name: Joined kunya 'abu minyar' -> 'abuminyar'
    - check: DOB conflict: customer 1942 vs list 1977; 1976; 01 Jan 1978
    - check: Nationality/country consistent (Libya)

### C002 - Usama bin Muhammad bin Laden  ->  **True Match**
Normalised as `usama muhammad laden`; DOB 1957-07-30; nationality Saudi Arabia
- **95** - BIN LADIN, Usama bin Muhammad bin Awad (individual; SDGT; SDN-6365) - *True Match*: Strong name match confirmed by exact date of birth - block/reject and report
    - Matched list alias (aka) 'BIN LADEN, Osama', not only the primary name
    - Customer name: Ignored name particles: bin
    - List name: 'osama' treated as transliteration variant of 'usama'
    - check: DOB exact match (1957-07-30)
    - check: Nationality/country consistent (Saudi Arabia)

### C003 - Bashar Hafez al-Assad  ->  **True Match**
Normalised as `bashar hafiz asad`; DOB 1965-09-11; nationality Syria
- **100** - AL-ASSAD, Bashar (individual; PAARSSR-EO13894; SDN-12735) - *True Match*: Strong name match confirmed by exact date of birth - block/reject and report
    - Matched list alias (aka) 'AL ASSAD, Bashar Hafez', not only the primary name
    - Identical after normalisation
    - Customer name: Ignored name particles: al
    - Customer name: 'hafez' treated as transliteration variant of 'hafiz'
    - Customer name: 'assad' treated as transliteration variant of 'asad'
    - List name: 'hafez' treated as transliteration variant of 'hafiz'
    - check: DOB exact match (1965-09-11)
    - check: Nationality/country consistent (Syria)
- **95** - AL-ASSAD, Hafez (individual; PAARSSR-EO13894; SDN-29279) - *False Positive*: Name similar but date of birth does not match the list entry
    - Customer name: Ignored name particles: al
    - Customer name: 'hafez' treated as transliteration variant of 'hafiz'
    - Customer name: 'assad' treated as transliteration variant of 'asad'
    - List name: 'hafez' treated as transliteration variant of 'hafiz'
    - List name: 'assad' treated as transliteration variant of 'asad'
    - check: DOB conflict: customer 1965 vs list 04 Dec 2001
    - check: Nationality/country consistent (Syria)
- **89** - AL-ASSAD, Bushra (individual; PAARSSR-EO13894; SDN-29072) - *False Positive*: Name similar but date of birth does not match the list entry
    - 'bushra' ~ 'bashar' sound alike (skeleton match), 88%
    - Customer name: Ignored name particles: al
    - Customer name: 'hafez' treated as transliteration variant of 'hafiz'
    - Customer name: 'assad' treated as transliteration variant of 'asad'
    - List name: 'assad' treated as transliteration variant of 'asad'
    - check: DOB conflict: customer 1965 vs list 24 Oct 1960
    - check: Nationality/country consistent (Syria)

### C004 - Sayyed Hassan Nasrullah  ->  **True Match**
Normalised as `hasan nasrallah`; DOB 1960-08-31; nationality Lebanon
- **100** - NASRALLAH, Hasan (individual; SDGT; SDN-2686) - *True Match*: Strong name match confirmed by exact date of birth - block/reject and report
    - Identical after normalisation
    - Customer name: Removed title/honorific: sayyed
    - Customer name: 'hassan' treated as transliteration variant of 'hasan'
    - Customer name: 'nasrullah' treated as transliteration variant of 'nasrallah'
    - check: DOB exact match (1960-08-31)
    - check: Nationality/country consistent (Lebanon)

### C005 - Qassem Suleimani  ->  **True Match**
Normalised as `qasim suleimani`; DOB 1957-03-11; nationality Iran
- **97** - SOLEIMANI, Qasem (individual; SDGT, NPWMD, IRGC, IFSR; SDN-10481) - *True Match*: Strong name match confirmed by exact date of birth - block/reject and report
    - Matched list alias (aka) 'SULEMANI, Qasem', not only the primary name
    - 'suleimani' ~ 'sulemani' sound alike (skeleton match), 94%
    - Customer name: 'qassem' treated as transliteration variant of 'qasim'
    - List name: 'qasem' treated as transliteration variant of 'qasim'
    - check: DOB exact match (1957-03-11)
    - check: Nationality/country consistent (Iran)

### C006 - Saif el-Islam Gadhafi  ->  **True Match**
Normalised as `saif islam qadhafi`; DOB 1972-06-25; nationality Libya
- **100** - QADHAFI, Saif al-Islam (individual; LIBYA2; SDN-12608) - *True Match*: Strong name match confirmed by exact date of birth - block/reject and report
    - Identical after normalisation
    - Customer name: Ignored name particles: el
    - Customer name: 'gadhafi' treated as transliteration variant of 'qadhafi'
    - check: DOB exact match (1972-06-25)
    - check: Nationality/country consistent (Libya)

### C007 - Rami Makhlouf  ->  **True Match**
Normalised as `rami makhluf`; DOB 1969-07-10; nationality Syria
- **100** - MAKHLUF, Rami (individual; PAARSSR-EO13894; SDN-10725) - *True Match*: Strong name match confirmed by exact date of birth - block/reject and report
    - Identical after normalisation
    - Customer name: 'makhlouf' treated as transliteration variant of 'makhluf'
    - check: DOB exact match (1969-07-10)
    - check: Nationality/country consistent (Syria)

### C008 - Ali Abdallah Salih  ->  **True Match**
Normalised as `ali abdallah salih`; DOB 1945-03-21; nationality Yemen
- **100** - SALEH, Ali Abdullah (individual; YEMEN; SDN-17387) - *True Match*: Strong name match confirmed by exact date of birth - block/reject and report
    - Identical after normalisation
    - List name: 'abdullah' treated as transliteration variant of 'abdallah'
    - List name: 'saleh' treated as transliteration variant of 'salih'
    - check: DOB exact match (1945-03-21)
    - check: Nationality/country consistent (Yemen)
- **96** - SALEH, Ahmed Ali (individual; YEMEN; SDN-17928) - *False Positive*: Name similar but date of birth does not match the list entry
    - Matched list alias (aka) 'SALEH, Ahmed Ali Abdullah', not only the primary name
    - List name: 'ahmed' treated as transliteration variant of 'ahmad'
    - List name: 'abdullah' treated as transliteration variant of 'abdallah'
    - List name: 'saleh' treated as transliteration variant of 'salih'
    - List name has additional name parts: ahmad
    - check: DOB conflict: customer 1945 vs list 25 Jul 1972; 1970
    - check: Nationality/country consistent (Yemen)

### C009 - Mousa Mohamed Abu Marzouk  ->  **True Match**
Normalised as `musa muhammad abumarzouk`; DOB 1951-02-09; nationality n/a
- **97** - ABU MARZOOK, Mousa Mohammed (individual; SDGT; SDN-3754) - *True Match*: Strong name match confirmed by exact date of birth - block/reject and report
    - 'abumarzouk' ~ 'abumarzook' sound alike (skeleton match), 90%
    - Customer name: Joined kunya 'abu marzouk' -> 'abumarzouk'
    - Customer name: 'mousa' treated as transliteration variant of 'musa'
    - Customer name: 'mohamed' treated as transliteration variant of 'muhammad'
    - List name: Joined kunya 'abu marzook' -> 'abumarzook'
    - List name: 'mousa' treated as transliteration variant of 'musa'
    - check: DOB exact match (1951-02-09)

### C010 - معمر القذافي  ->  **True Match**
Normalised as `muammar qadhafi`; DOB 1942; nationality Libya
- **100** - QADHAFI, Muammar (individual; LIBYA2; SDN-12606) - *True Match*: Strong name match, birth year and nationality consistent - block/reject and report
    - Identical after normalisation
    - Customer name: Arabic script transliterated to 'muammar qadhafi'
    - check: DOB year match only (1942; list: 1942) - obtain full DOB / ID document
    - check: Nationality/country consistent (Libya)
- **95** - GADDAFI, Hannibal (individual; LIBYA2; SDN-12627) - *False Positive*: Name similar but date of birth does not match the list entry
    - Matched list alias (aka) 'QADHAFI, Hannibal Muammar', not only the primary name
    - Customer name: Arabic script transliterated to 'muammar qadhafi'
    - List name has additional name parts: hannibal
    - check: DOB conflict: customer 1942 vs list 20 Sep 1975; 1977
    - check: Nationality/country consistent (Libya)
- **95** - GADDAFI, Muhammad (individual; LIBYA2; SDN-12628) - *False Positive*: Name similar but date of birth does not match the list entry
    - Matched list alias (aka) 'QADHAFI, Mohammed Muammar', not only the primary name
    - Customer name: Arabic script transliterated to 'muammar qadhafi'
    - List name: 'mohammed' treated as transliteration variant of 'muhammad'
    - List name has additional name parts: muhammad
    - check: DOB conflict: customer 1942 vs list 1970
    - check: Nationality/country consistent (Libya)
- **95** - GADDAFI, Saadi (individual; LIBYA2; SDN-12629) - *False Positive*: Name similar but date of birth does not match the list entry
    - Matched list alias (aka) 'AL-QADHAFI, Sa'adi Mu'ammar', not only the primary name
    - Customer name: Arabic script transliterated to 'muammar qadhafi'
    - List name has additional name parts: saadi
    - check: DOB conflict: customer 1942 vs list 27 May 1973; 25 May 1973
    - check: Nationality/country consistent (Libya)
- **91** - QADHAFI, Ayesha (individual; LIBYA2; SDN-12610) - *False Positive*: Name similar but date of birth does not match the list entry
    - Matched list alias (aka) 'QADHAFI, Aisha Muammar Muhammed Abu Minyar', not only the primary name
    - Customer name: Arabic script transliterated to 'muammar qadhafi'
    - List name: Joined kunya 'abu minyar' -> 'abuminyar'
    - List name: 'muhammed' treated as transliteration variant of 'muhammad'
    - List name has additional name parts: abuminyar, aisha, muhammad
    - check: DOB conflict: customer 1942 vs list 1977; 1976; 01 Jan 1978
    - check: Nationality/country consistent (Libya)

### C011 - أسامة بن لادن  ->  **Potential Match - escalate**
Normalised as `usama ladin`; DOB n/a; nationality n/a
- **100** - BIN LADIN, Usama bin Muhammad bin Awad (individual; SDGT; SDN-6365) - *Potential Match - escalate*: Name match not resolved by secondary identifiers - analyst review required
    - Matched list alias (aka) 'BIN LADIN, Osama', not only the primary name
    - Identical after normalisation
    - Customer name: Arabic script transliterated to 'usama bin ladin'
    - Customer name: Ignored name particles: bin
    - List name: 'osama' treated as transliteration variant of 'usama'
    - check: Customer DOB missing - request it (list DOB: 30 Jul 1957; 1958)
- **89** - AL QA'IDA (entity; FTO, SDGT; SDN-6366) - *False Positive*: Name similar but entity type differs (individual vs entity/vessel)
    - Matched list alias (aka) 'USAMA BIN LADEN ORGANIZATION', not only the primary name
    - 'ladin' ~ 'laden' sound alike (skeleton match), 88%
    - Customer name: Arabic script transliterated to 'usama bin ladin'
    - Customer name: Ignored name particles: bin
    - List name has additional name parts: laden, organization
    - check: Type mismatch: customer is an individual, list entry is an entity

### C012 - Bank Melli Iran  ->  **True Match**
Normalised as `bank melli iran`; DOB n/a; nationality Iran
- **100** - BANK MELLI IRAN (entity; IRAN, SDGT, IFSR; SDN-25578) - *True Match*: Near-exact name and matching nationality; list has no DOB to compare
    - Identical after normalisation
    - check: Nationality/country consistent (Iran)
- **100** - MB BANK (entity; SDGT, IFSR, RUSSIA-EO14024; SDN-25419) - *Potential Match - escalate*: Name match not resolved by secondary identifiers - analyst review required
    - Matched list alias (aka) 'BANK MELLI IRAN ZAO', not only the primary name
    - Identical after normalisation
    - check: Nationality differs: customer Iran vs list russia (weak - people hold several nationalities)
- **100** - TOSE-E MELLI GROUP INVESTMENT COMPANY (entity; SDGT, IFSR; SDN-25421) - *True Match*: Near-exact name and matching nationality; list has no DOB to compare
    - Matched list alias (aka) 'IRAN MELLI BANK INVESTMENT COMPANY', not only the primary name
    - Identical after normalisation (word order differs)
    - check: Nationality/country consistent (Iran)
- **95** - MELLI BANK PLC (entity; SDGT, IFSR; SDN-25420) - *Potential Match - escalate*: Name match not resolved by secondary identifiers - analyst review required
    - check: Nationality/country consistent (Iran)
- **95** - BANK SADERAT IRAN (entity; IRAN, SDGT, IFSR; SDN-10368) - *Potential Match - escalate*: Name match not resolved by secondary identifiers - analyst review required
    - Matched list alias (aka) 'IRAN EXPORT BANK', not only the primary name
    - check: Nationality/country consistent (Iran)

### C013 - Al-Qard Al-Hasan Association  ->  **True Match**
Normalised as `qard hasan association`; DOB n/a; nationality Lebanon
- **100** - AL-QARD AL-HASSAN ASSOCIATION (entity; SDGT; SDN-10416) - *True Match*: Near-exact name and matching nationality; list has no DOB to compare
    - Identical after normalisation
    - Customer name: Ignored name particles: al
    - List name: 'hassan' treated as transliteration variant of 'hasan'
    - check: Nationality/country consistent (Lebanon)

### C014 - Oleg V. Deripaska  ->  **True Match**
Normalised as `oleg v deripaska`; DOB 1968-01-02; nationality Russia
- **95** - DERIPASKA, Oleg Vladimirovich (individual; UKRAINE-EO13661, UKRAINE-EO13662; SDN-24283) - *True Match*: Strong name match confirmed by exact date of birth - block/reject and report
    - Initial 'v' consistent with 'vladimirovich'
    - check: DOB exact match (1968-01-02)
    - check: Nationality/country consistent (Russia)

### C015 - Levant Horizon Trading FZE  ->  **Potential Match - escalate**
Normalised as `levant horizon`; DOB n/a; nationality United Arab Emirates

> 50% Rule: aggregate ownership by possible SDNs is 55% - if confirmed, the entity is itself BLOCKED even though it is not named on the list. Owners flagged: Rami Makhluf (35%) ~ MAKHLUF, Rami [PAARSSR-EO13894] score 100; Iyad Makhlouf (20%) ~ MAKHLUF, Iyad [PAARSSR-EO13894] score 100


### C016 - Mahan Air Co  ->  **True Match**
Normalised as `mahan air`; DOB n/a; nationality Iran
- **100** - MAHAN AIR (entity; SDGT, NPWMD, IFSR; SDN-12927) - *True Match*: Near-exact name and matching nationality; list has no DOB to compare
    - Identical after normalisation
    - Customer name: Ignored legal-form / generic words: co
    - check: Nationality/country consistent (Iran)

### C017 - Sheikh Mohamed Ali Hassan  ->  **False Positive**
Normalised as `muhammad ali hasan`; DOB 1990-04-12; nationality Egypt
- **96** - AL-WARDIAN, Hassan (individual; SDGT; SDN-46231) - *False Positive*: Name similar but date of birth does not match the list entry
    - Matched list alias (aka) 'AL-WARDIAN, Hassan Muhammad 'Ali', not only the primary name
    - Customer name: Removed title/honorific: sheikh
    - Customer name: 'mohamed' treated as transliteration variant of 'muhammad'
    - Customer name: 'hassan' treated as transliteration variant of 'hasan'
    - List name: 'hassan' treated as transliteration variant of 'hasan'
    - List name has additional name parts: wardian
    - check: DOB conflict: customer 1990 vs list 28 Dec 1954
    - check: Nationality differs: customer Egypt vs list palestinian, region: west bank, west bank (weak - people hold several nationalities)
- **95** - FADHIL, Mustafa Mohamed (individual; SDGT; SDN-6924) - *False Positive*: Name similar but date of birth does not match the list entry
    - Matched list alias (aka) 'ALI, Hassan', not only the primary name
    - Customer name: Removed title/honorific: sheikh
    - Customer name: 'mohamed' treated as transliteration variant of 'muhammad'
    - Customer name: 'hassan' treated as transliteration variant of 'hasan'
    - List name: 'hassan' treated as transliteration variant of 'hasan'
    - check: DOB conflict: customer 1990 vs list 23 Jun 1976
    - check: Nationality/country consistent (Egypt)
- **95** - AMDOUNI, Mehrez (individual; SDGT; SDN-7828) - *False Positive*: Name similar but date of birth does not match the list entry
    - Matched list alias (aka) 'HASSAN, Mohamed', not only the primary name
    - Customer name: Removed title/honorific: sheikh
    - Customer name: 'mohamed' treated as transliteration variant of 'muhammad'
    - Customer name: 'hassan' treated as transliteration variant of 'hasan'
    - List name: 'mohamed' treated as transliteration variant of 'muhammad'
    - List name: 'hassan' treated as transliteration variant of 'hasan'
    - check: DOB conflict: customer 1990 vs list 18 Dec 1969; 25 May 1968; 18 Dec 1968; 14 Jul 1969
    - check: Nationality differs: customer Egypt vs list algeria, italy, tunisia (weak - people hold several nationalities)
- **93** - KAZAN, Ali Muhammad (individual; SDGT; SDN-10051) - *False Positive*: Name similar but date of birth does not match the list entry
    - Matched list alias (aka) 'KASSAN, Ali Mohamad', not only the primary name
    - 'hasan' ~ 'kassan' spelling similarity 77%
    - Customer name: Removed title/honorific: sheikh
    - Customer name: 'mohamed' treated as transliteration variant of 'muhammad'
    - Customer name: 'hassan' treated as transliteration variant of 'hasan'
    - List name: 'mohamad' treated as transliteration variant of 'muhammad'
    - check: DOB conflict: customer 1990 vs list 19 Dec 1967
    - check: Nationality differs: customer Egypt vs list brazil, lebanon, paraguay (weak - people hold several nationalities)
- **92** - AL ANSSARI, Ali Mohammed Ghulam Hussein (individual; SDGT, IFSR; SDN-50957) - *False Positive*: Name similar but date of birth does not match the list entry
    - Matched list alias (aka) 'HUSAYN, Ali Mohammad Ghulam', not only the primary name
    - 'hasan' ~ 'husayn' sound alike (skeleton match), 88%
    - Customer name: Removed title/honorific: sheikh
    - Customer name: 'mohamed' treated as transliteration variant of 'muhammad'
    - Customer name: 'hassan' treated as transliteration variant of 'hasan'
    - List name: 'mohammad' treated as transliteration variant of 'muhammad'
    - check: DOB conflict: customer 1990 vs list 21 Dec 1982
    - check: Nationality differs: customer Egypt vs list iraq, united kingdom (weak - people hold several nationalities)

### C018 - Ahmed Hussein  ->  **Potential Match - escalate**
Normalised as `ahmad husayn`; DOB 1985-06-01; nationality Iraq
- **95** - AL-KHODAIR, Ahmad Hussein (individual; IRAQ2; SDN-8329) - *False Positive*: Name similar but date of birth does not match the list entry
    - Customer name: 'ahmed' treated as transliteration variant of 'ahmad'
    - Customer name: 'hussein' treated as transliteration variant of 'husayn'
    - List name: 'hussein' treated as transliteration variant of 'husayn'
    - List name has additional name parts: khodair
    - check: DOB conflict: customer 1985 vs list 1941
- **95** - HUSSEIN, Ali Ahmed (individual; SDGT; SDN-42956) - *False Positive*: Name similar but date of birth does not match the list entry
    - Customer name: 'ahmed' treated as transliteration variant of 'ahmad'
    - Customer name: 'hussein' treated as transliteration variant of 'husayn'
    - List name: 'ahmed' treated as transliteration variant of 'ahmad'
    - List name: 'hussein' treated as transliteration variant of 'husayn'
    - List name has additional name parts: ali
    - check: DOB conflict: customer 1985 vs list 1980
    - check: Nationality differs: customer Iraq vs list somalia (weak - people hold several nationalities)
- **95** - AGHAMIR MOHAMMAD ALI, Seyed Mohammad Ali (individual; SDGT; SDN-57813) - *Potential Match - escalate*: Name match not resolved by secondary identifiers - analyst review required
    - Matched list alias (aka) 'AHMAD HOSSEIN, Ali', not only the primary name
    - Customer name: 'ahmed' treated as transliteration variant of 'ahmad'
    - Customer name: 'hussein' treated as transliteration variant of 'husayn'
    - List name: 'hossein' treated as transliteration variant of 'husayn'
    - List name has additional name parts: ali
    - check: DOB within 1 year (1985 vs list 23 Aug 1986) - inconclusive
    - check: Nationality differs: customer Iraq vs list iran (weak - people hold several nationalities)
- **95** - ABDALLAH, Hussein Ahmad Jalal (individual; SDGT; SDN-37430) - *False Positive*: Name similar but date of birth does not match the list entry
    - Matched list alias (aka) 'ABDALLAH, Hussein Ahmad', not only the primary name
    - Customer name: 'ahmed' treated as transliteration variant of 'ahmad'
    - Customer name: 'hussein' treated as transliteration variant of 'husayn'
    - List name: 'hussein' treated as transliteration variant of 'husayn'
    - List name has additional name parts: abdallah
    - check: DOB conflict: customer 1985 vs list 11 Feb 1996
    - check: Nationality differs: customer Iraq vs list lebanon (weak - people hold several nationalities)
- **92** - AL-HUSSEIN, Taha Osman Ahmed (individual; SUDAN-EO14098; SDN-46790) - *False Positive*: Name similar but date of birth does not match the list entry
    - Customer name: 'ahmed' treated as transliteration variant of 'ahmad'
    - Customer name: 'hussein' treated as transliteration variant of 'husayn'
    - List name: 'osman' treated as transliteration variant of 'uthman'
    - List name: 'ahmed' treated as transliteration variant of 'ahmad'
    - List name: 'hussein' treated as transliteration variant of 'husayn'
    - List name has additional name parts: taha, uthman
    - check: DOB conflict: customer 1985 vs list 20 Jun 1964; 21 Jun 1957
    - check: Nationality differs: customer Iraq vs list congo, democratic republic of the, saudi arabia, sudan, united arab emirates (weak - people hold several nationalities)

### C019 - Ali Hassan  ->  **False Positive**
Normalised as `ali hasan`; DOB 1979-11-03; nationality Jordan
- **100** - FADHIL, Mustafa Mohamed (individual; SDGT; SDN-6924) - *False Positive*: Name similar but date of birth does not match the list entry
    - Matched list alias (aka) 'ALI, Hassan', not only the primary name
    - Identical after normalisation (word order differs)
    - Customer name: 'hassan' treated as transliteration variant of 'hasan'
    - List name: 'hassan' treated as transliteration variant of 'hasan'
    - check: DOB conflict: customer 1979 vs list 23 Jun 1976
    - check: Nationality differs: customer Jordan vs list egypt, kenya (weak - people hold several nationalities)
- **95** - KHALIL, Ali Hassan (individual; SDGT; SDN-28572) - *False Positive*: Name similar but date of birth does not match the list entry
    - Customer name: 'hassan' treated as transliteration variant of 'hasan'
    - List name: 'hassan' treated as transliteration variant of 'hasan'
    - List name has additional name parts: khalil
    - check: DOB conflict: customer 1979 vs list 15 Jul 1964
    - check: Nationality differs: customer Jordan vs list lebanon (weak - people hold several nationalities)
- **95** - ZURAIK, Ali Hasan (individual; SDGT; SDN-12116) - *False Positive*: Name similar but date of birth does not match the list entry
    - Customer name: 'hassan' treated as transliteration variant of 'hasan'
    - List name has additional name parts: zuraik
    - check: DOB conflict: customer 1979 vs list 1952
    - check: Nationality differs: customer Jordan vs list lebanon (weak - people hold several nationalities)
- **95** - HASSAN, Ali Khatib Haji (individual; SDNTK; SDN-19428) - *False Positive*: Name similar but date of birth does not match the list entry
    - Customer name: 'hassan' treated as transliteration variant of 'hasan'
    - List name: 'hassan' treated as transliteration variant of 'hasan'
    - List name has additional name parts: khatib
    - check: DOB conflict: customer 1979 vs list 05 Jun 1970; 01 Jan 1963; 08 Jun 1970
    - check: Nationality differs: customer Jordan vs list tanzania (weak - people hold several nationalities)
- **95** - ALHASSAN, Ibrahim Ali (individual; SDGT; SDN-35843) - *False Positive*: Name similar but date of birth does not match the list entry
    - Customer name: 'hassan' treated as transliteration variant of 'hasan'
    - List name: 'hassan' treated as transliteration variant of 'hasan'
    - List name has additional name parts: ibrahim
    - check: DOB conflict: customer 1979 vs list 31 Jan 1981
    - check: Nationality differs: customer Jordan vs list nigeria, united arab emirates (weak - people hold several nationalities)

### C020 - Youssef Ibrahim  ->  **False Positive**
Normalised as `yusuf ibrahim`; DOB 1993-02-14; nationality Morocco
- **97** - EBRAHIMI, Yousef (individual; IRAN-EO13902; SDN-57696) - *False Positive*: Name similar but date of birth does not match the list entry
    - Matched list alias (aka) 'IBRAHIMI, Yusuf', not only the primary name
    - 'ibrahim' ~ 'ibrahimi' sound alike (skeleton match), 93%
    - Customer name: 'youssef' treated as transliteration variant of 'yusuf'
    - check: DOB conflict: customer 1993 vs list 16 Dec 1977
    - check: Nationality differs: customer Morocco vs list dominica, iran, turkey (weak - people hold several nationalities)
- **92** - IBRAHIM, Aadan Yusuf Saciid (individual; SDGT; SDN-43076) - *False Positive*: Name similar but date of birth does not match the list entry
    - Customer name: 'youssef' treated as transliteration variant of 'yusuf'
    - List name has additional name parts: aadan, saciid
    - check: DOB conflict: customer 1993 vs list 1987; 1988; 1989
    - check: Nationality differs: customer Morocco vs list somalia (weak - people hold several nationalities)
- **92** - YOUSEF IBRAHIM MANSOUR AND PARTNER FOR EXCHANGE (entity; SDGT; SDN-58555) - *False Positive*: Name similar but entity type differs (individual vs entity/vessel)
    - Matched list alias (aka) 'YOUSSEF IBRAHIM MANSOUR AND CO. FOR EXCHANGE', not only the primary name
    - Customer name: 'youssef' treated as transliteration variant of 'yusuf'
    - List name: 'youssef' treated as transliteration variant of 'yusuf'
    - List name: 'mansour' treated as transliteration variant of 'mansur'
    - List name has additional name parts: exchange, mansur
    - check: Type mismatch: customer is an individual, list entry is an entity
    - check: Nationality differs: customer Morocco vs list lebanon (weak - people hold several nationalities)

### C022 - Omar Abdel Rahman  ->  **False Positive**
Normalised as `umar abdrahman`; DOB 1988-05-09; nationality United States
- **100** - AL RAHMAN, Shaykh Umar Abd (individual; SDGT; SDN-2675) - *False Positive*: Name similar but date of birth does not match the list entry
    - Identical after normalisation
    - Customer name: Joined compound name 'abdel rahman' -> 'abdrahman'
    - Customer name: 'omar' treated as transliteration variant of 'umar'
    - List name: Joined compound name 'abd al rahman' -> 'abdrahman'
    - check: DOB conflict: customer 1988 vs list 03 May 1938
    - check: Nationality differs: customer United States vs list egypt (weak - people hold several nationalities)
- **92** - OMAR, Abdirahman Mohamed (individual; SDGT; SDN-39636) - *False Positive*: Name similar but date of birth does not match the list entry
    - 'abdrahman' ~ 'abdirahman' sound alike (skeleton match), 95%
    - Customer name: Joined compound name 'abdel rahman' -> 'abdrahman'
    - Customer name: 'omar' treated as transliteration variant of 'umar'
    - List name: 'mohamed' treated as transliteration variant of 'muhammad'
    - List name: 'omar' treated as transliteration variant of 'umar'
    - List name has additional name parts: abdirahman, muhammad
    - check: DOB conflict: customer 1988 vs list 1962
    - check: Nationality differs: customer United States vs list somalia (weak - people hold several nationalities)
- **90** - AL-NU'AYMI, 'Abd al-Rahman bin 'Umayr (individual; SDGT; SDN-16449) - *False Positive*: Name similar but date of birth does not match the list entry
    - 'umar' ~ 'umayr' sound alike (skeleton match), 89%
    - Customer name: Joined compound name 'abdel rahman' -> 'abdrahman'
    - Customer name: 'omar' treated as transliteration variant of 'umar'
    - List name: Joined compound name 'abd al rahman' -> 'abdrahman'
    - List name has additional name parts: nuaymi, umayr
    - check: DOB conflict: customer 1988 vs list 1954
    - check: Nationality differs: customer United States vs list qatar (weak - people hold several nationalities)
- **86** - EL TILEMSI, Ahmed (individual; SDGT; SDN-15611) - *False Positive*: Name similar but date of birth does not match the list entry
    - Matched list alias (aka) 'EL AMAR, Abderrahmane Ould', not only the primary name
    - 'umar' ~ 'amar' spelling similarity 78%
    - 'abdrahman' ~ 'abderrahmane' spelling similarity 89%
    - Customer name: Joined compound name 'abdel rahman' -> 'abdrahman'
    - Customer name: 'omar' treated as transliteration variant of 'umar'
    - check: DOB conflict: customer 1988 vs list 1977
    - check: Nationality differs: customer United States vs list mali (weak - people hold several nationalities)

### C023 - Khalid Mahmoud  ->  **Potential Match - escalate**
Normalised as `khalid mahmud`; DOB 1975-12-30; nationality Egypt
- **100** - KHAN, Mustafa Hajji Muhammad (individual; SDGT; SDN-12890) - *Potential Match - escalate*: Name match not resolved by secondary identifiers - analyst review required
    - Matched list alias (aka) 'MAHMUD, Khalid', not only the primary name
    - Identical after normalisation
    - Customer name: 'mahmoud' treated as transliteration variant of 'mahmud'
    - check: DOB within 1 year (1975 vs list Aug 1977; Sep 1977; 1976) - inconclusive
    - check: Nationality differs: customer Egypt vs list pakistan, saudi arabia (weak - people hold several nationalities)
- **95** - ZAHHAR, Mahmoud Khaled (individual; SDGT, NS-PLC; SDN-9647) - *False Positive*: Name similar but date of birth does not match the list entry
    - Customer name: 'mahmoud' treated as transliteration variant of 'mahmud'
    - List name: 'mahmoud' treated as transliteration variant of 'mahmud'
    - List name: 'khaled' treated as transliteration variant of 'khalid'
    - List name has additional name parts: zahhar
    - check: DOB conflict: customer 1975 vs list 1945
    - check: Nationality differs: customer Egypt vs list gaza strip, palestinian, region: gaza (weak - people hold several nationalities)
- **95** - ZAHHAR, Mahmoud Khaled (individual; SDGT, NS-PLC; CONS-9647) - *False Positive*: Name similar but date of birth does not match the list entry
    - Customer name: 'mahmoud' treated as transliteration variant of 'mahmud'
    - List name: 'mahmoud' treated as transliteration variant of 'mahmud'
    - List name: 'khaled' treated as transliteration variant of 'khalid'
    - List name has additional name parts: zahhar
    - check: DOB conflict: customer 1975 vs list 1945
    - check: Nationality differs: customer Egypt vs list gaza strip, palestinian, region: gaza (weak - people hold several nationalities)
- **90** - MOHAMMED, Khalid Shaikh (individual; SDGT; SDN-6928) - *False Positive*: Name similar but date of birth does not match the list entry
    - 'mahmud' ~ 'muhammad' spelling similarity 82%
    - Customer name: 'mahmoud' treated as transliteration variant of 'mahmud'
    - List name: 'mohammed' treated as transliteration variant of 'muhammad'
    - check: DOB conflict: customer 1975 vs list 14 Apr 1965; 01 Mar 1964
    - check: Nationality differs: customer Egypt vs list cuba, kuwait (weak - people hold several nationalities)
- **87** - AL-KHATIB, Mahmoud (individual; NS-PLC; CONS-9687) - *False Positive*: Name similar but date of birth does not match the list entry
    - 'khalid' ~ 'khatib' spelling similarity 79%
    - Customer name: 'mahmoud' treated as transliteration variant of 'mahmud'
    - List name: 'mahmoud' treated as transliteration variant of 'mahmud'
    - check: DOB conflict: customer 1975 vs list 1972

### C026 - Hassan Ali Khan  ->  **False Positive**
Normalised as `hasan ali khan`; DOB 1982-07-22; nationality Pakistan
- **95** - FADHIL, Mustafa Mohamed (individual; SDGT; SDN-6924) - *False Positive*: Name similar but date of birth does not match the list entry
    - Matched list alias (aka) 'ALI, Hassan', not only the primary name
    - Customer name: 'hassan' treated as transliteration variant of 'hasan'
    - List name: 'hassan' treated as transliteration variant of 'hasan'
    - check: DOB conflict: customer 1982 vs list 23 Jun 1976
    - check: Nationality differs: customer Pakistan vs list egypt, kenya (weak - people hold several nationalities)
- **90** - KHALIL, Ali Hassan (individual; SDGT; SDN-28572) - *False Positive*: Name similar but date of birth does not match the list entry
    - 'khan' ~ 'khalil' spelling similarity 78%
    - Customer name: 'hassan' treated as transliteration variant of 'hasan'
    - List name: 'hassan' treated as transliteration variant of 'hasan'
    - check: DOB conflict: customer 1982 vs list 15 Jul 1964
    - check: Nationality differs: customer Pakistan vs list lebanon (weak - people hold several nationalities)
- **90** - HASSAN, Ali Khatib Haji (individual; SDNTK; SDN-19428) - *False Positive*: Name similar but date of birth does not match the list entry
    - 'khan' ~ 'khatib' spelling similarity 78%
    - Customer name: 'hassan' treated as transliteration variant of 'hasan'
    - List name: 'hassan' treated as transliteration variant of 'hasan'
    - check: DOB conflict: customer 1982 vs list 05 Jun 1970; 01 Jan 1963; 08 Jun 1970
    - check: Nationality differs: customer Pakistan vs list tanzania (weak - people hold several nationalities)

### C028 - Ibrahim Awad  ->  **Potential Match - escalate**
Normalised as `ibrahim awad`; DOB 1980-09-09; nationality Iraq
- **92** - AL-FAY, Ibrahim Ali 'Awad (individual; SDGT; SDN-31953) - *False Positive*: Name similar but date of birth does not match the list entry
    - List name has additional name parts: ali, fay
    - check: DOB conflict: customer 1980 vs list 1968
    - check: Nationality differs: customer Iraq vs list turkey (weak - people hold several nationalities)
- **91** - AL-BADRI, Dr. Ibrahim 'Awwad Ibrahim 'Ali (individual; SDGT; SDN-12926) - *False Positive*: Name similar but date of birth does not match the list entry
    - Matched list alias (aka) 'AL-SAMARRA'I, Ibrahim 'Awad Ibrahim al-Badri', not only the primary name
    - List name has additional name parts: badri, samarrai
    - check: DOB conflict: customer 1980 vs list 1971
    - check: Nationality/country consistent (Iraq)
- **89** - BRAHIMI, Ahmed (individual; SDGT; SDN-53913) - *False Positive*: Name similar but date of birth does not match the list entry
    - Matched list alias (aka) 'IBRAHIM, Ahmed', not only the primary name
    - 'awad' ~ 'ahmad' spelling similarity 76%
    - List name: 'ahmed' treated as transliteration variant of 'ahmad'
    - check: DOB conflict: customer 1980 vs list 24 Jun 1970
    - check: Nationality differs: customer Iraq vs list algeria (weak - people hold several nationalities)
- **89** - JADHRAN, Ibrahim (individual; LIBYA3; SDN-24957) - *Potential Match - escalate*: Name match not resolved by secondary identifiers - analyst review required
    - Matched list alias (aka) 'AL JADHRAN, Ibrahim Saeed Salem Awad Aissa Hamed Dawoud', not only the primary name
    - List name: 'saeed' treated as transliteration variant of 'said'
    - List name: 'aissa' treated as transliteration variant of 'issa'
    - List name: 'hamed' treated as transliteration variant of 'hamid'
    - List name has additional name parts: dawoud, hamid, issa, jadhran, said, salem
    - check: DOB year match only (1980; list: 29 Oct 1982; 1979 to 1982) - obtain full DOB / ID document
    - check: Nationality differs: customer Iraq vs list libya (weak - people hold several nationalities)

### C029 - Muhammad Qasim  ->  **False Positive**
Normalised as `muhammad qasim`; DOB 2001-04-04; nationality Pakistan
- **100** - QASIM, Mohammed (individual; SDGT; SDN-15581) - *False Positive*: Name similar but date of birth does not match the list entry
    - Identical after normalisation
    - List name: 'mohammed' treated as transliteration variant of 'muhammad'
    - check: DOB conflict: customer 2001 vs list 1976; 1965
    - check: Nationality/country consistent (Pakistan)
- **95** - HIJAZI, Kassem Mohamad (individual; GLOMAG; SDN-28445) - *False Positive*: Name similar but date of birth does not match the list entry
    - List name: 'kassem' treated as transliteration variant of 'qasim'
    - List name: 'mohamad' treated as transliteration variant of 'muhammad'
    - List name has additional name parts: hijazi
    - check: DOB conflict: customer 2001 vs list 15 Sep 1972
    - check: Nationality differs: customer Pakistan vs list brazil, paraguay (weak - people hold several nationalities)
- **95** - SALEH, Kassem Mohamad (individual; SDNTK; SDN-12892) - *False Positive*: Name similar but date of birth does not match the list entry
    - List name: 'kassem' treated as transliteration variant of 'qasim'
    - List name: 'mohamad' treated as transliteration variant of 'muhammad'
    - List name: 'saleh' treated as transliteration variant of 'salih'
    - List name has additional name parts: salih
    - check: DOB conflict: customer 2001 vs list 10 Feb 1980
    - check: Nationality differs: customer Pakistan vs list colombia, lebanon, venezuela (weak - people hold several nationalities)
- **95** - AL-BAZZAL, Muhammad Qasim (individual; SDGT; SDN-26122) - *False Positive*: Name similar but date of birth does not match the list entry
    - List name has additional name parts: bazzal
    - check: DOB conflict: customer 2001 vs list 26 Aug 1984
    - check: Nationality differs: customer Pakistan vs list lebanon (weak - people hold several nationalities)
- **95** - CHAMS, Kassem (individual; SDNTK; SDN-23023) - *False Positive*: Name similar but date of birth does not match the list entry
    - Matched list alias (aka) 'SHAMS, Kassem Mohammed', not only the primary name
    - List name: 'kassem' treated as transliteration variant of 'qasim'
    - List name: 'mohammed' treated as transliteration variant of 'muhammad'
    - List name has additional name parts: shams
    - check: DOB conflict: customer 2001 vs list 20 Mar 1962
    - check: Nationality differs: customer Pakistan vs list lebanon (weak - people hold several nationalities)

### C030 - Hannibal Gaddafi Restaurant LLC  ->  **Potential Match - escalate**
Normalised as `hannibal qadhafi restaurant`; DOB n/a; nationality Malta
- **95** - GADDAFI, Hannibal (individual; LIBYA2; SDN-12627) - *Potential Match - escalate*: Name match not resolved by secondary identifiers - analyst review required
    - Customer name: Ignored legal-form / generic words: llc
    - Customer name: 'gaddafi' treated as transliteration variant of 'qadhafi'
    - List name: 'gaddafi' treated as transliteration variant of 'qadhafi'
    - check: Customer is an entity but the list entry is an individual: name overlap may indicate ownership/control - check beneficial owners (50% Rule)
    - check: Customer DOB missing - request it (list DOB: 20 Sep 1975; 1977)
    - check: Nationality differs: customer Malta vs list libya (weak - people hold several nationalities)
