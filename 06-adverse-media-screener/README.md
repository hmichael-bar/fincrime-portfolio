# Adverse Media Screener (English + Arabic)

Give it a person or company name. It searches recent news in **English and Arabic** using two free sources with no API keys: the **GDELT DOC API** and **Google News RSS**. It flags financial-crime risk keywords in six categories, scores each story's severity, merges duplicate stories, and writes an adverse-media report in Markdown, HTML and JSON with links to every source.

This is the *negative news* check that KYC/EDD analysts run at onboarding and periodic review. Being able to read and search the Arabic press directly is a real gap in most Western compliance teams.

> Tested only on public, well-known sanctioned or prosecuted subjects. Do not use it to profile private individuals.

---

## Why adverse media matters

* **KYC / CDD:** The FinCEN CDD Rule and FATF Recommendation 10 expect banks to understand customer risk. Negative news is often the first sign that a customer is involved in a predicate offence (fraud, corruption, trafficking) before any list designation.
* **EDD and PEPs:** For high-risk customers and politically exposed persons, adverse-media review is a standard enhanced-due-diligence step, repeated at periodic review.
* **Sanctions risk ahead of the list:** Designations often follow months of press reporting. Media screening shows a risk before the name reaches the SDN list.
* **Language blind spots:** Much reporting on Gulf, Levant and North Africa subjects appears first, or only, in Arabic. An English-only search misses it.

## What it does

| Step | Detail |
|---|---|
| Search | Google News RSS, US-English and Arabic editions: the name alone, and the name AND an OR-list of risk terms. GDELT DOC 2.0: English sources, plus Arabic sources via GDELT's built-in translation. Each step respects GDELT's limit of one request per 5 seconds, with retry and backoff. |
| Classify | Regular expressions for English and normalised Arabic phrases (hamza, ta marbuta and diacritics folded) across six categories: **money laundering, sanctions/asset freeze, fraud, bribery/corruption, terrorism financing, organised crime/trafficking**. |
| Legal stage | Each story is tagged as an *allegation/investigation*, *charged/arrested/sued*, or *conviction/penalty/designation*. Exculpatory wording (acquitted, delisted, sanctions lifted) lowers severity, unless it is negated: *"court refuses to lift sanctions"* stays adverse. |
| Relevance | Is the subject named in the headline, in the snippet, only by surname ("Makhlouf family"), or not at all? Fuzzy matching handles transliteration differences (Makhlouf/Makhluf). |
| Severity | 0–100 = category weight × stage multiplier × relevance multiplier, with a bonus when several categories appear. |
| De-duplicate | Same URL, or near-identical headlines (rapidfuzz token-set ≥ 90). Syndicated copies collapse into one story with an "also reported by" list. |
| Rate | Overall **HIGH / MEDIUM / LOW / NONE**, with a written reason. |
| Report | Markdown + self-contained HTML (Arabic headlines render right-to-left) + JSON for downstream tools. Every search query and its status is logged for the audit trail. |

## Quick start

```bash
cd 06-adverse-media-screener
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python screen_media.py "Rami Makhlouf" --alias "Rami Makhluf" --arabic "رامي مخلوف"
python screen_media.py "Bank Melli Iran" --kind entity --arabic "بنك ملي إيران"
python screen_media.py --batch sample_subjects.csv --out output
python screen_media.py "Binance" --kind entity --days 90 --no-gdelt   # skip GDELT if it rate-limits you
```

## Example results (run 13 Nov 2026, 365-day look-back)

| Subject | Why chosen | Articles → unique → adverse | Adverse EN / AR | Main categories | Rating |
|---|---|---|---|---|---|
| **Bank Melli Iran** | OFAC-designated Iranian state bank | 201 → 113 → 30 | 22 / 8 | Sanctions (28), terrorism financing (3) | HIGH |
| **Binance** | Pleaded guilty to BSA/sanctions violations (2023) | 354 → 309 → 53 | 49 / 4 | Money laundering (34), sanctions (12), fraud (5) | HIGH |
| **Rami Makhlouf** | SDN; Assad-era Syrian tycoon | 80 → 64 → 3 | 1 / 2 | Sanctions / asset freeze (3) | HIGH |

Full reports: [`output/bank_melli_iran.html`](output/bank_melli_iran.html) · [`output/binance.html`](output/binance.html) · [`output/rami_makhlouf.html`](output/rami_makhlouf.html). Each has a `.md` and `.json` twin. Console log: [`output/console_output.txt`](output/console_output.txt).

```
=== Bank Melli Iran (entity) ===
Overall risk: HIGH - Credible, serious adverse media naming the subject (conviction/penalty/designation-level or repeated).
201 articles -> 113 unique stories -> 30 adverse
  [ 90] 2026-09-23 Khaleej Times          CBUAE imposes sanctions on Bank Melli Iran, bans financial transactions with Iran
         Sanctions / asset freeze | Conviction / penalty / designation | named in title
  [ 68] 2026-09-23 معلومات مباشر          الإمارات تحظر معاملات فروع «بنك ملي إيران» مع طهران
         Sanctions / asset freeze | Not stated | named in title
```

**What the examples teach**

* **The Arabic search adds real coverage.** For Rami Makhlouf, the top finding (*"Did the UAE begin seizing Rami Makhlouf's funds in response to the criminal court?"*) came only from the Arabic edition. Two of his three adverse stories are Arabic, and the Arabic query returned twice as many articles as the English one (41 vs 21).
* **De-duplication matters.** The UAE central bank's action against Bank Melli produced dozens of near-identical headlines. 201 raw articles became 113 stories. Without merging, an analyst would read the same story twenty times.
* **Keyword screening produces false positives that need a human.** Binance's top hit, *"Binance Blocks MEXC Transfers After FinCEN Money Laundering Designation"*, names Binance and money laundering, but the designated party is MEXC. Binance is the one complying. Likewise, *"Makhlouf family members"* stories are scored as *partial* relevance because they may concern relatives rather than the subject. This is why every finding is a lead for review, not a conclusion.
* **Headlines alone undercount.** Most coverage of Makhlouf discusses his business empire without risk words in the headline, so only 3 of 64 stories score as adverse. A human reader would see more context. See Limitations.

## Project layout

```
06-adverse-media-screener/
├── screen_media.py            CLI (single subject or --batch CSV)
├── sample_subjects.csv        the three public test subjects
├── adverse_media/
│   ├── keywords.py            EN + AR risk taxonomy, legal-stage words, mitigating/negation words
│   ├── sources.py             GDELT DOC API + Google News RSS clients (rate-limit aware)
│   ├── analyze.py             relevance, classification, severity, de-duplication, overall rating
│   ├── screener.py            builds the search strings and runs one subject end to end
│   └── report.py              Markdown / HTML / JSON writers
├── output/                    example reports for the three subjects
├── HOW_IT_WORKS.md            one-page interview prep sheet
└── requirements.txt
```

## Limitations

* **Headline-level analysis.** Google News RSS and GDELT return headlines, not article bodies. The tool does not scrape publisher sites, which avoids paywall and terms-of-use problems but misses risk terms that appear only in the body text.
* **GDELT** covers roughly the last 3 months and rate-limits heavily. A rate-limited call is logged in the report, not hidden. Use `--no-gdelt` if needed.
* **Keyword logic cannot tell who did what.** Subject-as-victim, subject-as-reporter and subject-as-compliant-party stories (the Binance/MEXC example) need human review. A production tool would add named-entity recognition and relation extraction.
* **Namesakes.** A common name returns stories about other people. Add DOB, nationality, company or city context to the search, and confirm identity before recording a finding.
* **Arabic names must be supplied in Arabic script** (`--arabic`). Latin-to-Arabic transliteration is ambiguous, so the tool does not guess.
* **Source credibility is not scored.** A wire-service report and an anonymous blog get the same weight. The analyst applies that judgment.

## Data sources

[GDELT Project DOC 2.0 API](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/) (free, open) and Google News RSS search feeds (public, for personal/non-commercial use). No API keys, no paid data.
