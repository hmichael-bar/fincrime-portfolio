"""Orchestrates the searches, scoring and de-duplication for one subject."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

from .analyze import Finding, Subject, deduplicate, overall_rating, score_article
from .keywords import SEARCH_TERMS_AR, SEARCH_TERMS_EN
from .sources import SourceLog, gdelt_search, google_news_search


@dataclass
class ScreeningRun:
    subject: Subject
    run_at: datetime
    days: int
    findings: list[Finding]
    logs: list[SourceLog]
    rating: str
    rating_reason: str
    raw_count: int
    non_adverse_count: int = 0
    queries: list[str] = field(default_factory=list)

    @property
    def adverse(self) -> list[Finding]:
        return [f for f in self.findings if f.is_adverse]


def _or(terms: list[str]) -> str:
    return "(" + " OR ".join(terms) + ")"


def build_queries(subject: Subject, days: int, use_gdelt: bool = True):
    """Return list of (source, lang, query). Mirrors the 'name + risk terms' search strings
    an analyst types into a search engine."""
    q = []
    latin = [subject.name] + subject.aliases[:2]
    for n in latin:
        q.append(("gnews", "en", f'"{n}" when:{days}d'))
        q.append(("gnews", "en", f'"{n}" {_or(SEARCH_TERMS_EN)} when:{days}d'))
    for n in subject.arabic_names[:2]:
        q.append(("gnews", "ar", f'"{n}" when:{days}d'))
        q.append(("gnews", "ar", f'"{n}" {_or(SEARCH_TERMS_AR)} when:{days}d'))
    if use_gdelt:
        span = "3m" if days >= 90 else f"{days}d"   # GDELT DOC API covers a rolling ~3 months
        q.append(("gdelt", span, f'"{subject.name}" {_or(SEARCH_TERMS_EN[:7])} sourcelang:english'))
        # GDELT machine-translates foreign-language coverage, so an English query + sourcelang
        # finds Arabic-language press.
        q.append(("gdelt", span, f'"{subject.name}" sourcelang:arabic'))
    return q


def screen_subject(subject: Subject, days: int = 365, use_gdelt: bool = True,
                   progress=print) -> ScreeningRun:
    articles, logs = [], []
    queries = build_queries(subject, days, use_gdelt)
    for src, opt, query in queries:
        if src == "gnews":
            arts, log = google_news_search(query, opt)
        else:
            arts, log = gdelt_search(query, timespan=opt)
        progress(f"  {log.source:18s} {log.status:12s} {log.n_results:>4} results  | {query}")
        articles += arts
        logs.append(log)

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    articles = [a for a in articles if a.published is None or a.published >= cutoff]
    scored = [score_article(subject, a) for a in articles]
    findings = deduplicate(scored)
    findings.sort(key=lambda f: (-f.severity, -(f.article.published.timestamp() if f.article.published else 0)))
    rating, reason = overall_rating(findings)
    return ScreeningRun(subject=subject, run_at=datetime.now(timezone.utc), days=days,
                        findings=findings, logs=logs, rating=rating, rating_reason=reason,
                        raw_count=len(articles),
                        non_adverse_count=sum(1 for f in findings if not f.is_adverse),
                        queries=[q for _, _, q in queries])
