"""End-to-end run: generate data -> rules -> anomaly model -> risk scores -> evaluation.

Usage:
    python src/run_pipeline.py            # regenerate data and run everything
    python src/run_pipeline.py --no-regen # keep existing data, rerun detection (e.g. after editing thresholds)
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_data  # noqa: E402
from anomaly import combined_scores, score_customers  # noqa: E402
from evaluate import evaluate  # noqa: E402
from rules import load_data, load_params, run_rules  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-regen", action="store_true", help="reuse data/ instead of regenerating it")
    args = ap.parse_args()
    t0 = time.time()
    OUT.mkdir(exist_ok=True)
    if not args.no_regen or not (ROOT / "data" / "transactions.csv").exists():
        print("[1/5] generating synthetic data ...")
        generate_data.build()
    cust, tx = load_data()
    params = load_params()

    print("[2/5] running rules engine ...")
    alerts = run_rules(cust, tx, params)
    alerts.to_csv(OUT / "alerts.csv", index=False)
    print(f"      {len(alerts)} alerts")

    print("[3/5] scoring customers with Isolation Forest ...")
    anomaly = score_customers(cust, tx, params)
    anomaly.to_csv(OUT / "customer_features_and_anomaly.csv", index=False)

    print("[4/5] building combined risk score ...")
    scores = combined_scores(cust, alerts, anomaly, params)
    scores.to_csv(OUT / "customer_risk_scores.csv", index=False)

    print("[5/5] evaluating against ground truth + threshold sweeps ...")
    m = evaluate(cust, tx, params, alerts, anomaly, scores)
    o = m["overall"]
    print(f"      alerts={o['alerts']}  alert_precision={o['alert_precision']:.0%}  customer_recall={o['customer_recall']:.0%}")
    print(f"      isolation forest AUC={m['isolation_forest']['roc_auc']}")
    print(f"done in {time.time() - t0:.1f}s -> outputs/evaluation_report.md")


if __name__ == "__main__":
    main()
