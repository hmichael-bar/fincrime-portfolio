"""Batch screening of a customer file, report writers and threshold tuning."""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from .matcher import FALSE_POSITIVE, NO_MATCH, POTENTIAL, TRUE_MATCH, Screener, ScreenResult


def read_customers(path: str | Path) -> list[dict]:
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return [{k.strip().lower(): (v or "").strip() for k, v in row.items()} for row in csv.DictReader(fh)]


def screen_customers(screener: Screener, customers: list[dict], threshold: float,
                     max_hits: int = 5) -> list[tuple[dict, ScreenResult]]:
    out = []
    for c in customers:
        res = screener.screen(c.get("name", ""), c.get("type", "individual"), c.get("dob", ""),
                              c.get("nationality", ""), threshold=threshold, max_hits=max_hits,
                              owners=c.get("owners", ""))
        out.append((c, res))
    return out


def write_summary_csv(results, path: Path) -> None:
    fields = ["customer_id", "name", "type", "alert", "disposition", "top_score", "matched_name",
              "list_entry", "list", "programs", "list_type", "n_hits", "disposition_reason",
              "ownership_note", "top_reasons"]
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for c, r in results:
            t = r.top
            alert = bool(r.hits) or ("50% Rule" in r.ownership_note)
            w.writerow({
                "customer_id": c.get("customer_id", ""), "name": c.get("name", ""),
                "type": c.get("type", ""), "alert": "Y" if alert else "N",
                "disposition": r.disposition, "top_score": f"{t.score:.1f}" if t else "",
                "matched_name": t.matched_name if t else "", "list_entry": t.entry.name if t else "",
                "list": t.entry.source if t else "", "programs": ", ".join(t.entry.programs) if t else "",
                "list_type": t.entry.sdn_type if t else "", "n_hits": len(r.hits),
                "disposition_reason": t.disposition_reason if t else "",
                "ownership_note": r.ownership_note,
                "top_reasons": " | ".join(t.reasons[:4]) if t else "",
            })


def write_detail_json(results, path: Path, threshold: float, stats: dict) -> None:
    payload = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "threshold": threshold, "list_stats": stats,
        "results": [{
            "customer": c, "normalized_name": r.normalized.text, "disposition": r.disposition,
            "ownership_note": r.ownership_note, "hits": [h.to_dict() for h in r.hits]}
            for c, r in results],
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_markdown_report(results, path: Path, threshold: float, stats: dict) -> None:
    counts = {}
    for _, r in results:
        counts[r.disposition] = counts.get(r.disposition, 0) + 1
    lines = [
        "# Sanctions Screening Report",
        "",
        f"*Generated {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC - threshold {threshold:g} - "
        f"{stats['sdn_entries']:,} SDN + {stats['consolidated_entries']:,} non-SDN entries, "
        f"{stats['names_incl_aliases']:,} names incl. aliases*",
        "",
        "| Disposition | Customers |", "|---|---|",
    ]
    for d in (TRUE_MATCH, POTENTIAL, FALSE_POSITIVE, NO_MATCH):
        lines.append(f"| {d} | {counts.get(d, 0)} |")
    lines += ["", "## Summary", "",
              "| ID | Customer | Disposition | Score | Best list match | Program |",
              "|---|---|---|---|---|---|"]
    for c, r in results:
        t = r.top
        lines.append(f"| {c.get('customer_id','')} | {c.get('name','')} | {r.disposition} | "
                     f"{t.score:.0f} | {t.entry.name if t else ''} | "
                     f"{', '.join(t.entry.programs) if t else ''} |" if t else
                     f"| {c.get('customer_id','')} | {c.get('name','')} | {r.disposition} | - | - | - |")
    lines += ["", "## Alert details", ""]
    for c, r in results:
        if not r.hits and not r.ownership_note.startswith("50%"):
            continue
        lines.append(f"### {c.get('customer_id','')} - {c.get('name','')}  ->  **{r.disposition}**")
        lines.append(f"Normalised as `{r.normalized.text}`; DOB {c.get('dob') or 'n/a'}; "
                     f"nationality {c.get('nationality') or 'n/a'}")
        if r.ownership_note:
            lines.append(f"\n> {r.ownership_note}\n")
        for h in r.hits:
            e = h.entry
            lines.append(f"- **{h.score:.0f}** - {e.name} ({e.sdn_type}; {', '.join(e.programs)}; "
                         f"{e.uid}) - *{h.disposition}*: {h.disposition_reason}")
            for x in h.reasons[:6]:
                lines.append(f"    - {x}")
            for x in h.secondary:
                lines.append(f"    - check: {x}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


# --------------------------------------------------------------------------
def tune_thresholds(screener: Screener, customers: list[dict], thresholds=None) -> list[dict]:
    """Recall vs alert volume across thresholds on a labelled file (column 'expected')."""
    thresholds = thresholds or list(range(70, 101, 5))
    # Screen once at the lowest threshold, then re-filter - much faster.
    low = min(thresholds)
    base = screen_customers(screener, customers, threshold=low, max_hits=50)
    rows = []
    n_sdn = sum(1 for c in customers if c.get("expected") == "sdn")
    for t in thresholds:
        alerted_sdn = alerted_other = total_hits = 0
        cleared_by_rules = 0
        for c, r in base:
            hits = [h for h in r.hits if h.score >= t]
            own = "50% Rule" in r.ownership_note
            if c.get("expected") == "sdn":
                alerted_sdn += 1 if (hits or own) else 0
            elif hits:
                alerted_other += 1
            total_hits += len(hits)
            cleared_by_rules += sum(1 for h in hits if h.disposition == FALSE_POSITIVE)
        alerted = alerted_sdn + alerted_other
        rows.append({
            "threshold": t, "recall": alerted_sdn / n_sdn if n_sdn else 0.0,
            "customers_alerted": alerted, "false_alert_customers": alerted_other,
            "total_hits": total_hits, "auto_cleared_hits": cleared_by_rules,
            "hits_for_analyst": total_hits - cleared_by_rules,
            "precision": alerted_sdn / alerted if alerted else 0.0,
        })
    return rows
