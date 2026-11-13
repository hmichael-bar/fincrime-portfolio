#!/usr/bin/env python3
"""
Adverse media screener - CLI.

  python screen_media.py "Rami Makhlouf" --arabic "رامي مخلوف" --alias "Rami Makhluf"
  python screen_media.py "Bank Melli Iran" --kind entity --arabic "بنك ملي إيران"
  python screen_media.py --batch subjects.csv
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from adverse_media.analyze import Subject
from adverse_media.report import write_all
from adverse_media.screener import screen_subject
from adverse_media.keywords import CATEGORIES
from adverse_media.report import STAGE_LABEL


def run_one(subject: Subject, args) -> None:
    print(f"\n=== {subject.name} ({subject.kind}) ===")
    run = screen_subject(subject, days=args.days, use_gdelt=not args.no_gdelt)
    paths = write_all(run, Path(args.out))
    print(f"\nOverall risk: {run.rating} - {run.rating_reason}")
    print(f"{run.raw_count} articles -> {len(run.findings)} unique stories -> {len(run.adverse)} adverse")
    for f in run.adverse[:8]:
        a = f.article
        cats = ", ".join(CATEGORIES[c]["label"] for c in f.categories)
        print(f"  [{f.severity:>3.0f}] {a.published:%Y-%m-%d} {a.source[:22]:22s} {a.title[:85]}" if a.published
              else f"  [{f.severity:>3.0f}] {'n/a':10s} {a.source[:22]:22s} {a.title[:85]}")
        print(f"         {cats} | {STAGE_LABEL[f.stage]} | named in {f.relevance}")
    print("Reports: " + ", ".join(str(p) for p in paths.values()))


def main() -> int:
    p = argparse.ArgumentParser(description="Adverse media screening (GDELT + Google News RSS, EN + AR)")
    p.add_argument("name", nargs="?", help="person or company name")
    p.add_argument("--alias", action="append", default=[], help="additional Latin-script name (repeatable)")
    p.add_argument("--arabic", action="append", default=[], help="Arabic-script name (repeatable)")
    p.add_argument("--kind", default="person", choices=["person", "entity"])
    p.add_argument("--days", type=int, default=365, help="look-back window (GDELT covers ~3 months max)")
    p.add_argument("--no-gdelt", action="store_true", help="skip GDELT (e.g. if rate-limited)")
    p.add_argument("--batch", help="CSV with columns name,kind,aliases,arabic_names (';'-separated)")
    p.add_argument("--out", default="output")
    args = p.parse_args()

    if args.batch:
        with open(args.batch, encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                run_one(Subject(name=row["name"].strip(), kind=(row.get("kind") or "person").strip(),
                                aliases=[x.strip() for x in (row.get("aliases") or "").split(";") if x.strip()],
                                arabic_names=[x.strip() for x in (row.get("arabic_names") or "").split(";") if x.strip()]),
                        args)
        return 0
    if not args.name:
        p.error("give a name or --batch file")
    run_one(Subject(args.name, args.alias, args.arabic, args.kind), args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
