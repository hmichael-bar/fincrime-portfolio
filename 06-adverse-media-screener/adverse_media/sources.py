"""
Free news sources - no API keys.

* GDELT DOC 2.0 API  (https://api.gdeltproject.org/api/v2/doc/doc)
  Global news index, updated every 15 minutes, 65+ languages. Non-English articles are
  machine-translated by GDELT, so an English query with `sourcelang:arabic` finds Arabic
  press coverage. Limit: one request every 5 seconds - we wait and retry politely.
* Google News RSS   (https://news.google.com/rss/search?q=...)
  Returns ~50-100 recent articles per query, per language/edition (hl/gl/ceid).
"""
from __future__ import annotations

import html
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import feedparser
import requests

USER_AGENT = "adverse-media-screener/1.0 (educational portfolio project; public news only)"
GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"
GNEWS_URL = "https://news.google.com/rss/search"
GNEWS_EDITIONS = {"en": {"hl": "en-US", "gl": "US", "ceid": "US:en"},
                  "ar": {"hl": "ar", "gl": "EG", "ceid": "EG:ar"}}

_last_gdelt_call = 0.0


@dataclass
class Article:
    title: str
    url: str
    source: str
    published: datetime | None
    language: str
    snippet: str = ""
    found_via: list[str] = field(default_factory=list)   # e.g. ["Google News (ar)"]
    query: str = ""

    def to_dict(self) -> dict:
        return {"title": self.title, "url": self.url, "source": self.source,
                "published": self.published.isoformat() if self.published else None,
                "language": self.language, "snippet": self.snippet, "found_via": self.found_via,
                "query": self.query}


@dataclass
class SourceLog:
    source: str
    query: str
    status: str          # "ok", "error: ...", "rate-limited"
    n_results: int = 0


def _clean_html(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


# --------------------------------------------------------------------------
def gdelt_search(query: str, timespan: str = "12m", max_records: int = 75,
                 retries: int = 3, base_wait: float = 6.0) -> tuple[list[Article], SourceLog]:
    global _last_gdelt_call
    params = {"query": query, "mode": "artlist", "format": "json", "maxrecords": max_records,
              "timespan": timespan, "sort": "datedesc"}
    status = "error"
    for attempt in range(retries):
        wait = base_wait - (time.time() - _last_gdelt_call)
        if wait > 0:
            time.sleep(wait)
        try:
            _last_gdelt_call = time.time()
            r = requests.get(GDELT_URL, params=params, headers={"User-Agent": USER_AGENT}, timeout=45)
        except requests.RequestException as exc:
            status = f"error: {exc.__class__.__name__}"
            time.sleep(base_wait * (attempt + 1))
            continue
        if r.status_code == 429 or "limit requests" in r.text[:200]:
            status = "rate-limited"
            time.sleep(base_wait * 2 * (attempt + 1))
            continue
        if r.status_code != 200:
            status = f"error: HTTP {r.status_code}"
            break
        try:
            data = r.json() if r.text.strip() else {}
        except ValueError:
            # GDELT answers invalid queries with a plain-text message
            return [], SourceLog("GDELT", query, f"error: {r.text[:80]}")
        out = []
        for a in data.get("articles", []):
            try:
                dt = datetime.strptime(a.get("seendate", ""), "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
            except ValueError:
                dt = None
            lang = (a.get("language") or "").lower()
            out.append(Article(title=a.get("title", "").strip(), url=a.get("url", ""),
                               source=a.get("domain", ""), published=dt,
                               language="ar" if lang.startswith("arab") else "en" if lang.startswith("engl") else lang,
                               found_via=["GDELT"], query=query))
        return out, SourceLog("GDELT", query, "ok", len(out))
    return [], SourceLog("GDELT", query, status)


def google_news_search(query: str, lang: str = "en") -> tuple[list[Article], SourceLog]:
    ed = GNEWS_EDITIONS[lang]
    try:
        r = requests.get(GNEWS_URL, params={"q": query, **ed}, headers={"User-Agent": USER_AGENT}, timeout=30)
        r.raise_for_status()
    except requests.RequestException as exc:
        return [], SourceLog(f"Google News ({lang})", query, f"error: {exc.__class__.__name__}")
    feed = feedparser.parse(r.content)
    out = []
    for e in feed.entries:
        src = (e.get("source") or {}).get("title", "")
        title = e.get("title", "")
        if src and title.endswith(" - " + src):           # Google appends " - Publisher"
            title = title[: -len(src) - 3]
        try:
            dt = parsedate_to_datetime(e.get("published", "")) if e.get("published") else None
        except (TypeError, ValueError):
            dt = None
        snippet = _clean_html(e.get("summary", ""))
        if snippet.startswith(title):
            snippet = snippet[len(title):].strip(" -")
        if src and snippet.strip() == src:
            snippet = ""
        out.append(Article(title=title.strip(), url=e.get("link", ""), source=src, published=dt,
                           language=lang, snippet=snippet, found_via=[f"Google News ({lang})"], query=query))
    return out, SourceLog(f"Google News ({lang})", query, "ok", len(out))
