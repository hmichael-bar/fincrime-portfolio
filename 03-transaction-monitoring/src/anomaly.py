"""Second line of detection: customer-level features + an Isolation Forest.

Rules look for patterns we already know. The anomaly model asks a different question:
"which customers look least like everyone else?" It is unsupervised: it never sees the
ground-truth labels. Its output is used two ways:
  1. as a lead list of customers no rule alerted on, and
  2. as one input to a combined risk score that ranks the alert queue.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reference import country_risk  # noqa: E402

FEATURES = {
    "log_total_in": "Total credits (log $)",
    "log_total_out": "Total debits (log $)",
    "cash_in_share": "Share of credits that are cash",
    "n_cash_8k_10k": "# cash deposits $8,000-$9,999",
    "n_cash_states": "# states where cash was deposited",
    "intl_wire_share": "Share of volume in international wires",
    "log_high_risk_wire": "High-risk-jurisdiction wire $ (log)",
    "n_round_wires": "# round-dollar wires >= $10K",
    "fast_out_ratio": "Share of credits leaving within 3 days",
    "n_unique_senders": "# distinct inbound counterparties",
    "max_gap_days": "Longest gap between transactions (days)",
    "max_vol_vs_expected": "Peak month volume / KYC expected volume",
    "crypto_out_share": "Share of debits sent to crypto",
    "device_sharing": "# customers on same device",
    "account_age_days": "Account age (days)",
}


def customer_features(cust: pd.DataFrame, tx: pd.DataFrame) -> pd.DataFrame:
    c = cust.set_index("customer_id")
    g = tx.groupby("customer_id")
    f = pd.DataFrame(index=c.index)
    tin = tx[tx.direction == "IN"].groupby("customer_id").amount.sum()
    tout = tx[tx.direction == "OUT"].groupby("customer_id").amount.sum()
    f["log_total_in"] = np.log1p(tin.reindex(f.index, fill_value=0))
    f["log_total_out"] = np.log1p(tout.reindex(f.index, fill_value=0))
    cash = tx[tx.txn_type == "CASH_DEPOSIT"]
    f["cash_in_share"] = (cash.groupby("customer_id").amount.sum() / tin).reindex(f.index).fillna(0)
    f["n_cash_8k_10k"] = cash[(cash.amount >= 8000) & (cash.amount < 10000)].groupby("customer_id").size().reindex(f.index, fill_value=0)
    f["n_cash_states"] = cash[cash.branch_state != ""].groupby("customer_id").branch_state.nunique().reindex(f.index, fill_value=0)
    wires = tx[tx.txn_type.isin(["WIRE_IN", "WIRE_OUT"])]
    intl = wires[wires.counterparty_country != "United States"]
    vol = g.amount.sum()
    f["intl_wire_share"] = (intl.groupby("customer_id").amount.sum() / vol).reindex(f.index).fillna(0)
    hr = wires[wires.counterparty_country.map(country_risk) != "standard"]
    f["log_high_risk_wire"] = np.log1p(hr.groupby("customer_id").amount.sum().reindex(f.index, fill_value=0))
    f["n_round_wires"] = wires[(wires.amount >= 10000) & (wires.amount % 1000 == 0)].groupby("customer_id").size().reindex(f.index, fill_value=0)

    # fast-out ratio: for each day with credits, how much left in the next 3 days (capped at the credit)
    daily = tx.assign(day=tx.timestamp.dt.floor("D"), inn=np.where(tx.direction == "IN", tx.amount, 0),
                      out=np.where((tx.direction == "OUT") & (tx.txn_type != "CARD_PURCHASE"), tx.amount, 0))
    daily = daily.groupby(["customer_id", "day"])[["inn", "out"]].sum().reset_index()
    fast = {}
    for cid, d in daily.groupby("customer_id"):
        d = d.set_index("day")[["inn", "out"]].asfreq("D", fill_value=0)
        fwd = d.out[::-1].rolling(4, min_periods=1).sum()[::-1]  # today + next 3 days
        fast[cid] = np.minimum(d.inn, fwd).sum() / d.inn.sum() if d.inn.sum() else 0
    f["fast_out_ratio"] = pd.Series(fast).reindex(f.index).fillna(0)

    inbound = tx[tx.txn_type.isin(["P2P_IN", "ACH_IN"])]
    f["n_unique_senders"] = inbound.groupby("customer_id").counterparty_account.nunique().reindex(f.index, fill_value=0)

    def max_gap(s):
        t = s.sort_values()
        return t.diff().dt.days.max() if len(t) > 1 else 181
    gaps = g.timestamp.apply(max_gap).reindex(f.index).fillna(181)
    prior_gap = (g.timestamp.min() - pd.to_datetime(c.last_txn_before_2026)).dt.days.reindex(f.index).fillna(0)
    f["max_gap_days"] = np.maximum(gaps, prior_gap)

    mvol = tx.groupby(["customer_id", "month"]).amount.sum().groupby("customer_id").max()
    f["max_vol_vs_expected"] = np.log1p((mvol / c.expected_monthly_volume_usd).reindex(f.index).fillna(0))
    cb = tx[tx.txn_type == "CRYPTO_BUY"].groupby("customer_id").amount.sum()
    f["crypto_out_share"] = (cb / tout).reindex(f.index).fillna(0)
    dev = pd.concat([cust[["device_id", "customer_id"]], tx.loc[tx.device_id != "", ["device_id", "customer_id"]]]).drop_duplicates()
    per_dev = dev.groupby("device_id").customer_id.nunique()
    f["device_sharing"] = c.device_id.map(per_dev).fillna(1)
    f["account_age_days"] = (tx.timestamp.max() - c.account_open_date).dt.days
    return f[list(FEATURES)]


def score_customers(cust, tx, params) -> pd.DataFrame:
    p = params["anomaly_model"]
    feats = customer_features(cust, tx)
    X = StandardScaler().fit_transform(feats.values)
    model = IsolationForest(n_estimators=p["n_estimators"], contamination=p["contamination"], random_state=p["random_state"])
    model.fit(X)
    out = feats.copy()
    out["anomaly_score"] = -model.score_samples(X)  # higher = more anomalous
    out["anomaly_pct"] = out.anomaly_score.rank(pct=True)
    out["is_anomaly"] = model.predict(X) == -1
    # crude explanation: which standardized features are most extreme for this customer
    z = pd.DataFrame(X, index=feats.index, columns=feats.columns)
    out["top_drivers"] = z.apply(lambda r: ", ".join(FEATURES[k] for k in r.abs().nlargest(3).index), axis=1)
    return out.reset_index().rename(columns={"index": "customer_id"})


def combined_scores(cust, alerts, anomaly, params) -> pd.DataFrame:
    """Blend rule hits, anomaly percentile and KYC risk into one 0-100 priority score."""
    from rules import PARAM_KEYS
    w = params["combined_score_weights"]
    rule_w = alerts.rule_id.map(lambda r: params[PARAM_KEYS[r]]["weight"])
    alerts = alerts.assign(pts=rule_w * alerts.severity / 100)
    rule_pts = alerts.groupby("customer_id").pts.sum()
    rule_list = alerts.groupby("customer_id").rule_id.apply(lambda s: ",".join(sorted(set(s))))
    df = cust[["customer_id", "name", "occupation", "kyc_risk_rating"]].merge(
        anomaly[["customer_id", "anomaly_score", "anomaly_pct", "is_anomaly", "top_drivers"]], on="customer_id")
    df["n_alerts"] = df.customer_id.map(alerts.customer_id.value_counts()).fillna(0).astype(int)
    df["rules_hit"] = df.customer_id.map(rule_list).fillna("")
    df["rule_points"] = df.customer_id.map(rule_pts).fillna(0)
    pct = df.rule_points.rank(pct=True).where(df.rule_points > 0, 0)
    kyc = df.kyc_risk_rating.map({"Low": 0, "Medium": 0.5, "High": 1.0})
    df["risk_score"] = (100 * (w["rules"] * pct + w["anomaly"] * df.anomaly_pct + w["kyc_risk"] * kyc)).round(1)
    return df.sort_values("risk_score", ascending=False).reset_index(drop=True)
