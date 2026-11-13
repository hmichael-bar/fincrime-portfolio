#!/usr/bin/env python3
"""
Command-line interface for the OFAC sanctions screening engine.

  python screen.py name "Moammar Gaddafi" --dob 1942 --nationality Libya
  python screen.py name "معمر القذافي"
  python screen.py batch sample_data/customers.csv --out output
  python screen.py tune  sample_data/customers.csv --out output
  python screen.py update-lists
"""
from __future__ import annotations

import argparse
import json
import sys
import textwrap
from pathlib import Path

from sanctions_screener import Screener
from sanctions_screener.batch import (read_customers, screen_customers, tune_thresholds,
                                      write_detail_json, write_markdown_report, write_summary_csv)
from sanctions_screener.matcher import DEFAULT_THRESHOLD

COLORS = {"True Match": "\033[91m", "Potential Match - escalate": "\033[93m",
          "False Positive": "\033[96m", "No Match": "\033[92m"}
RESET = "\033[0m"


def _c(text: str, disp: str, enable: bool) -> str:
    return f"{COLORS.get(disp, '')}{text}{RESET}" if enable else text


def cmd_name(args) -> int:
    s = Screener(include_consolidated=not args.sdn_only, threshold=args.threshold)
    r = s.screen(args.name, args.type, args.dob or "", args.nationality or "", max_hits=args.max_hits,
                 owners=args.owners or "")
    if args.json:
        print(json.dumps({"query": args.name, "normalized": r.normalized.text,
                          "disposition": r.disposition, "ownership_note": r.ownership_note,
                          "hits": [h.to_dict() for h in r.hits]}, indent=2, ensure_ascii=False))
        return 0
    color = sys.stdout.isatty() and not args.no_color
    print(f"\nQuery       : {args.name}")
    print(f"Normalised  : {r.normalized.text}")
    for n in r.normalized.notes:
        print(f"              - {n}")
    print(f"Threshold   : {args.threshold:g}")
    print("Result      : " + _c(r.disposition, r.disposition, color))
    if r.ownership_note:
        print("Ownership   : " + textwrap.fill(r.ownership_note, 90, subsequent_indent=" " * 14))
    for i, h in enumerate(r.hits, 1):
        d = h.to_dict()
        print(f"\n[{i}] score {d['score']:>5}  " + _c(d["disposition"], d["disposition"], color))
        print(f"    List entry : {d['primary_name']}  ({d['list']} {d['uid']}, {d['type']})")
        print(f"    Matched on : {d['matched_on']} -> {d['matched_name']}")
        print(f"    Programs   : {', '.join(d['programs'])}")
        if d["dob"]:
            print(f"    DOB        : {'; '.join(d['dob'])}")
        if d["nationality"] or d["pob"]:
            print(f"    Nat./POB   : {', '.join(d['nationality']) or '-'} / {'; '.join(d['pob']) or '-'}")
        print(f"    Why        : {d['disposition_reason']}")
        for x in d["reasons"]:
            print(f"      - {x}")
        for x in d["secondary_checks"]:
            print(f"      * {x}")
        comps = ", ".join(f"{k}={v}" for k, v in d["score_components"].items())
        print(f"    Components : {comps}")
    print()
    return 0


def cmd_batch(args) -> int:
    s = Screener(include_consolidated=not args.sdn_only, threshold=args.threshold)
    customers = read_customers(args.csv)
    results = screen_customers(s, customers, args.threshold, args.max_hits)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    write_summary_csv(results, out / "screening_results.csv")
    write_detail_json(results, out / "screening_results.json", args.threshold, s.stats)
    write_markdown_report(results, out / "screening_report.md", args.threshold, s.stats)
    print(f"Screened {len(customers)} customers against {s.stats['names_incl_aliases']:,} names "
          f"(threshold {args.threshold:g})\n")
    print(f"{'ID':6} {'Customer':34} {'Disposition':28} {'Score':>5}  Best match")
    for c, r in results:
        t = r.top
        print(f"{c.get('customer_id',''):6} {c.get('name','')[:34]:34} {r.disposition:28} "
              f"{(f'{t.score:.0f}' if t else '-'):>5}  {(t.entry.name[:45] if t else '')}")
    print(f"\nWrote {out/'screening_results.csv'}, {out/'screening_results.json'}, {out/'screening_report.md'}")
    return 0


def cmd_tune(args) -> int:
    s = Screener(include_consolidated=not args.sdn_only)
    customers = read_customers(args.csv)
    rows = tune_thresholds(s, customers)
    base_rows = tune_thresholds(Screener(include_consolidated=not args.sdn_only, arabic_rules=False),
                                customers)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    hdr = ["threshold", "recall", "customers_alerted", "false_alert_customers", "total_hits",
           "auto_cleared_hits", "hits_for_analyst", "precision"]
    with open(out / "threshold_tuning.csv", "w", encoding="utf-8") as fh:
        fh.write(",".join(hdr) + "\n")
        for r in rows:
            fh.write(",".join(f"{r[h]:.3f}" if isinstance(r[h], float) else str(r[h]) for h in hdr) + "\n")
    print(f"{'Thr':>4} {'Recall':>7} {'Cust.alerted':>13} {'Non-SDN alerted':>16} {'Hits':>5} "
          f"{'Auto-cleared':>13} {'For analyst':>12} {'Precision':>10}")
    for r in rows:
        print(f"{r['threshold']:>4} {r['recall']:>7.0%} {r['customers_alerted']:>13} "
              f"{r['false_alert_customers']:>16} {r['total_hits']:>5} {r['auto_cleared_hits']:>13} "
              f"{r['hits_for_analyst']:>12} {r['precision']:>10.0%}")
    print("\nBaseline WITHOUT the Arabic-name module (same fuzzy scorer):")
    print(f"{'Thr':>4} {'Recall':>7} {'Cust.alerted':>13} {'Hits':>5}")
    for r in base_rows:
        print(f"{r['threshold']:>4} {r['recall']:>7.0%} {r['customers_alerted']:>13} {r['total_hits']:>5}")
    with open(out / "threshold_tuning_no_arabic.csv", "w", encoding="utf-8") as fh:
        fh.write(",".join(hdr) + "\n")
        for r in base_rows:
            fh.write(",".join(f"{r[h]:.3f}" if isinstance(r[h], float) else str(r[h]) for h in hdr) + "\n")
    try:
        from sanctions_screener.plot import plot_tuning
        plot_tuning(rows, out / "threshold_tuning.png", base_rows)
        print(f"\nChart: {out/'threshold_tuning.png'}")
    except ImportError:
        print("\n(matplotlib not installed - skipping chart)")
    print(f"Table: {out/'threshold_tuning.csv'}")
    return 0


def cmd_update(_args) -> int:
    from sanctions_screener.download import main
    return main()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="OFAC SDN sanctions screening with Arabic-name support")
    p.add_argument("--sdn-only", action="store_true", help="skip the Consolidated non-SDN list")
    sub = p.add_subparsers(dest="cmd", required=True)

    n = sub.add_parser("name", help="screen a single name")
    n.add_argument("name")
    n.add_argument("--type", default="individual", choices=["individual", "entity"])
    n.add_argument("--dob", help="YYYY-MM-DD or YYYY")
    n.add_argument("--nationality")
    n.add_argument("--owners", help="for entities: 'Name|pct;Name|pct' (50%% Rule check)")
    n.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    n.add_argument("--max-hits", type=int, default=5)
    n.add_argument("--json", action="store_true")
    n.add_argument("--no-color", action="store_true")
    n.set_defaults(func=cmd_name)

    b = sub.add_parser("batch", help="screen a CSV of customers")
    b.add_argument("csv")
    b.add_argument("--out", default="output")
    b.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    b.add_argument("--max-hits", type=int, default=5)
    b.set_defaults(func=cmd_batch)

    t = sub.add_parser("tune", help="threshold vs recall / alert-volume analysis (needs 'expected' column)")
    t.add_argument("csv")
    t.add_argument("--out", default="output")
    t.set_defaults(func=cmd_tune)

    u = sub.add_parser("update-lists", help="download the latest OFAC files")
    u.set_defaults(func=cmd_update)
    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    raise SystemExit(args.func(args))
