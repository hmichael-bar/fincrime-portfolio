"""Rules engine: ten AML detection scenarios with tunable thresholds.

Each rule reads only what a real monitoring system can see (KYC profile + transactions)
and returns raw "hits". `run_rules` then rolls hits up into alerts: one alert per
customer, per rule, per calendar month, which is how many vendor systems
(Actimize, Verafin, Oracle FCCM) batch alerts for an L1 queue.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reference import FREE_ZONE_MARKERS, country_risk  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CREDIT = {"CASH_DEPOSIT", "WIRE_IN", "ACH_IN", "P2P_IN", "CRYPTO_SELL"}
DEBIT = {"CASH_WITHDRAWAL", "WIRE_OUT", "ACH_OUT", "P2P_OUT", "CRYPTO_BUY", "CARD_PURCHASE"}
WIRES = {"WIRE_IN", "WIRE_OUT"}

RULE_NAMES = {
    "R01": "Structuring: cash deposits just below the $10K CTR threshold",
    "R02": "Rapid movement of funds (pass-through)",
    "R03": "Funnel account: cash deposited in multiple out-of-area states",
    "R04": "Wires to/from high-risk jurisdictions",
    "R05": "Repeated round-dollar wires",
    "R06": "Dormant account reactivation",
    "R07": "Trade-based ML: invoice-pattern wires",
    "R08": "Money mule activity (many senders, fast outflow)",
    "R09": "Activity far above KYC expected profile",
    "R10": "Device shared by multiple unrelated customers",
}
PARAM_KEYS = {
    "R01": "R01_structuring", "R02": "R02_rapid_movement", "R03": "R03_funnel_account",
    "R04": "R04_high_risk_geography", "R05": "R05_round_dollar_wires", "R06": "R06_dormant_reactivation",
    "R07": "R07_tbml_invoice_pattern", "R08": "R08_mule_activity", "R09": "R09_profile_deviation",
    "R10": "R10_shared_device",
}


def load_params(path: Path | None = None) -> dict:
    with open(path or ROOT / "config" / "thresholds.json") as f:
        return json.load(f)


def load_data():
    cust = pd.read_csv(ROOT / "data" / "customers.csv", parse_dates=["account_open_date", "last_txn_before_2026"])
    tx = pd.read_csv(ROOT / "data" / "transactions.csv", parse_dates=["timestamp"], keep_default_na=False,
                     dtype={"branch_id": str, "branch_state": str, "device_id": str, "memo": str})
    tx["amount"] = tx["amount"].astype(float)
    tx["month"] = tx["timestamp"].dt.to_period("M")
    cust["expected_countries"] = cust["expected_countries"].fillna("")
    cust["expected_goods"] = cust["expected_goods"].fillna("")
    return cust, tx


def _hit(cid, rule, date, txns, amount, details, severity):
    return dict(customer_id=cid, rule_id=rule, alert_date=pd.Timestamp(date), txn_ids=list(txns),
                amount_involved=round(float(amount), 2), details=details, severity=float(min(100, severity)))


def _fmt(x):
    return f"${x:,.0f}"


# ----------------------------------------------------------------------------- R01
def r01_structuring(cust, tx, p):
    lo, hi, W, k, agg = p["lower_bound"], p["ctr_threshold"], p["window_days"], p["min_count"], p["min_aggregate"]
    cash = tx[(tx.txn_type == "CASH_DEPOSIT") & (tx.amount >= lo) & (tx.amount < hi)]
    out = []
    for cid, g in cash.groupby("customer_id"):
        g = g.sort_values("timestamp")
        ts = g.timestamp.values
        i, n = 0, len(g)
        while i < n:
            j = i
            while j + 1 < n and ts[j + 1] - ts[i] <= np.timedelta64(W, "D"):
                j += 1
            win = g.iloc[i:j + 1]
            if len(win) >= k and win.amount.sum() >= agg:
                br = win.branch_id.nunique()
                out.append(_hit(cid, "R01", win.timestamp.max(), win.txn_id, win.amount.sum(),
                                f"{len(win)} cash deposits of {_fmt(lo)}-{_fmt(hi - 1)} in {W} days totalling "
                                f"{_fmt(win.amount.sum())} at {br} branch(es)",
                                20 * len(win) + 10 * br))
                i = j + 1
            else:
                i += 1
    return out


# ----------------------------------------------------------------------------- R02
def r02_rapid_movement(cust, tx, p):
    out = []
    big = tx[tx.txn_type.isin(CREDIT - {"P2P_IN"}) & (tx.amount >= p["min_inflow"])]
    debits = tx[tx.txn_type.isin(DEBIT - {"CARD_PURCHASE"})]
    deb_by = {cid: g.sort_values("timestamp") for cid, g in debits[debits.customer_id.isin(big.customer_id)].groupby("customer_id")}
    W = pd.Timedelta(days=p["window_days"])
    for r in big.itertuples():
        d = deb_by.get(r.customer_id)
        if d is None:
            continue
        w = d[(d.timestamp >= r.timestamp) & (d.timestamp <= r.timestamp + W)]
        ratio = w.amount.sum() / r.amount
        if ratio >= p["pass_through_ratio"]:
            out.append(_hit(r.customer_id, "R02", w.timestamp.max(), [r.txn_id, *w.txn_id], r.amount,
                            f"{_fmt(r.amount)} {r.txn_type} " + (f"from {r.counterparty_name} ({r.counterparty_country}); " if r.counterparty_name else f"at branch {r.branch_id}; ")
                            + 
                            f"outflows within {p['window_days']} days equal {ratio:.0%} of it",
                            40 + 40 * min(ratio, 1.2) + min(20, r.amount / 10000)))
    return out


# ----------------------------------------------------------------------------- R03
def r03_funnel(cust, tx, p):
    home = cust.set_index("customer_id").home_state
    cash = tx[(tx.txn_type == "CASH_DEPOSIT") & (tx.branch_state != "")].copy()
    cash = cash[cash.branch_state.values != home.reindex(cash.customer_id).values]
    out = []
    for (cid, m), g in cash.groupby(["customer_id", "month"]):
        st = g.branch_state.nunique()
        if st >= p["min_out_of_state_branch_states"] and g.amount.sum() >= p["min_out_of_state_cash"]:
            out.append(_hit(cid, "R03", g.timestamp.max(), g.txn_id, g.amount.sum(),
                            f"{len(g)} cash deposits in {st} states outside home state {home[cid]} "
                            f"({', '.join(sorted(g.branch_state.unique()))}) totalling {_fmt(g.amount.sum())}",
                            30 + 12 * st + min(30, g.amount.sum() / 2000)))
    return out


# ----------------------------------------------------------------------------- R04
def r04_high_risk_geo(cust, tx, p):
    expected = cust.set_index("customer_id").expected_countries.str.split(";").to_dict()
    w = tx[tx.txn_type.isin(WIRES)].copy()
    w["tier"] = w.counterparty_country.map(country_risk)
    keep = (w.tier == "black") | ((w.tier == "grey") & (w.amount >= p["grey_min_amount"])) | \
           ((w.tier == "corridor") & (w.amount >= p["corridor_min_amount"]))
    w = w[keep]
    if p["suppress_if_country_in_kyc_profile"]:
        in_profile = [c in expected.get(cid, []) for cid, c in zip(w.customer_id, w.counterparty_country)]
        w = w[~np.array(in_profile, dtype=bool) | (w.tier == "black").values]
    out = []
    for (cid, m), g in w.groupby(["customer_id", "month"]):
        if g.amount.sum() >= p["monthly_min_total"] or (g.tier == "black").any():
            tiers = g.tier.value_counts().to_dict()
            out.append(_hit(cid, "R04", g.timestamp.max(), g.txn_id, g.amount.sum(),
                            f"{len(g)} wire(s) totalling {_fmt(g.amount.sum())} with "
                            f"{', '.join(sorted(g.counterparty_country.unique()))} (tiers: {tiers})",
                            30 + 25 * tiers.get("black", 0) + 10 * tiers.get("grey", 0) + 5 * tiers.get("corridor", 0)
                            + min(20, g.amount.sum() / 10000)))
    return out


# ----------------------------------------------------------------------------- R05
def r05_round_dollar(cust, tx, p):
    w = tx[tx.txn_type.isin(WIRES) & (tx.amount >= p["min_amount"]) & ((tx.amount % p["round_unit"]) == 0)]
    out = []
    for (cid, m), g in w.groupby(["customer_id", "month"]):
        if len(g) >= p["min_count_per_month"]:
            out.append(_hit(cid, "R05", g.timestamp.max(), g.txn_id, g.amount.sum(),
                            f"{len(g)} round-dollar wires (multiples of {_fmt(p['round_unit'])}) totalling "
                            f"{_fmt(g.amount.sum())} to/from {g.counterparty_name.nunique()} counterparties",
                            25 + 15 * len(g) + 5 * g.counterparty_name.nunique()))
    return out


# ----------------------------------------------------------------------------- R06
def r06_dormant(cust, tx, p):
    prior = cust.set_index("customer_id").last_txn_before_2026
    gap_min = pd.Timedelta(days=p["dormancy_days"])
    W = pd.Timedelta(days=p["reactivation_window_days"])
    out = []
    for cid, g in tx.groupby("customer_id"):
        g = g.sort_values("timestamp")
        times = list(g.timestamp)
        last = prior.get(cid)
        prev = [pd.Timestamp(last)] + times[:-1] if pd.notna(last) else [None] + times[:-1]
        for i, (t, pv) in enumerate(zip(times, prev)):
            if pv is None or t - pv < gap_min:
                continue
            win = g[(g.timestamp >= t) & (g.timestamp <= t + W)]
            tot = win.amount.sum()
            if tot >= p["min_reactivation_amount"]:
                out.append(_hit(cid, "R06", win.timestamp.max(), win.txn_id, tot,
                                f"No activity for {(t - pv).days} days, then {len(win)} transactions totalling "
                                f"{_fmt(tot)} within {p['reactivation_window_days']} days",
                                30 + min(40, (t - pv).days / 5) + min(30, tot / 5000)))
    return out


# ----------------------------------------------------------------------------- R07
def r07_tbml(cust, tx, p):
    cp = cust.set_index("customer_id")
    w = tx[tx.txn_type.isin(WIRES) & tx.memo.str.contains("INV", na=False) & (tx.amount >= p["min_amount"])].copy()
    if w.empty:
        return []
    rep = w.groupby(["customer_id", "counterparty_name", "amount"]).txn_id.transform("count")
    tier = w.counterparty_country.map(country_risk)
    fz = w.counterparty_name.str.upper().apply(lambda s: any(m in s for m in FREE_ZONE_MARKERS))
    goods_ok = [(g.lower() in memo.lower()) if g else True for g, memo in zip(cp.expected_goods.reindex(w.customer_id), w.memo)]
    exp_c = cp.expected_countries.reindex(w.customer_id).values
    third_party = (w.txn_type == "WIRE_IN").values & np.array(
        [(c not in e.split(";")) and c != "United States" for c, e in zip(w.counterparty_country, exp_c)])
    w["c_geo"] = (tier != "standard").values | fz.values
    w["c_goods"] = ~np.array(goods_ok) & (w.txn_type == "WIRE_OUT").values
    w["c_repeat"] = (rep >= p["repeat_count"]).values
    w["c_third"] = third_party
    w["n_cond"] = w[["c_geo", "c_goods", "c_repeat", "c_third"]].sum(axis=1)
    w = w[w.n_cond >= p["min_conditions"]]
    out = []
    labels = {"c_geo": "free-zone/high-risk counterparty", "c_goods": "goods inconsistent with KYC",
              "c_repeat": "identical repeated invoice amounts", "c_third": "third-party payer outside profile"}
    for (cid, m), g in w.groupby(["customer_id", "month"]):
        flags = [labels[k] for k in labels if g[k].any()]
        out.append(_hit(cid, "R07", g.timestamp.max(), g.txn_id, g.amount.sum(),
                        f"{len(g)} invoice-referenced wire(s) totalling {_fmt(g.amount.sum())}; indicators: {'; '.join(flags)}",
                        30 + 12 * len(flags) + 5 * len(g)))
    return out


# ----------------------------------------------------------------------------- R08
def r08_mule(cust, tx, p):
    cp = cust.set_index("customer_id")
    dev_counts = cust.groupby("device_id").customer_id.nunique()
    tx_dev = tx[tx.device_id != ""].groupby("device_id").customer_id.nunique()
    dev_counts = pd.concat([dev_counts, tx_dev], axis=1).max(axis=1)
    out = []
    inbound = tx[tx.txn_type.isin({"P2P_IN", "ACH_IN"})]
    cand = inbound.groupby(["customer_id", "month"]).counterparty_account.nunique()
    cand = cand[cand >= p["min_unique_senders"]]
    for (cid, m), senders in cand.items():
        g = tx[(tx.customer_id == cid) & (tx.month == m)]
        cin = g[g.direction == "IN"].amount.sum()
        cout = g[(g.direction == "OUT") & (g.txn_type != "CARD_PURCHASE")].amount.sum()
        ratio = cout / cin if cin else 0
        if ratio < p["min_outflow_ratio"]:
            continue
        crypto_share = g[g.txn_type == "CRYPTO_BUY"].amount.sum() / cout if cout else 0
        age = (m.to_timestamp(how="end") - cp.account_open_date[cid]).days
        shared = dev_counts.get(cp.device_id[cid], 1)
        sec = []
        if crypto_share >= p["crypto_outflow_share"]:
            sec.append(f"{crypto_share:.0%} of outflow to crypto")
        if age < p["new_account_days"]:
            sec.append(f"account {age} days old")
        if shared >= p["shared_device_min_customers"]:
            sec.append(f"device shared by {int(shared)} customers")
        if p["require_secondary_indicator"] and not sec:
            continue
        ids = g[g.txn_type.isin({"P2P_IN", "ACH_IN", "P2P_OUT", "CRYPTO_BUY", "CASH_WITHDRAWAL", "WIRE_OUT"})].txn_id
        out.append(_hit(cid, "R08", g.timestamp.max(), ids, cin,
                        f"{senders} distinct senders paid in {_fmt(cin)}; {ratio:.0%} moved out"
                        + (f"; {'; '.join(sec)}" if sec else ""),
                        30 + min(30, senders) + 10 * len(sec)))
    return out


# ----------------------------------------------------------------------------- R09
def r09_profile_deviation(cust, tx, p):
    exp = cust.set_index("customer_id").expected_monthly_volume_usd
    vol = tx.groupby(["customer_id", "month"]).amount.sum()
    out = []
    for (cid, m), v in vol.items():
        mult = v / exp[cid]
        if mult >= p["volume_multiplier"] and v >= p["min_monthly_volume"]:
            g = tx[(tx.customer_id == cid) & (tx.month == m)].nlargest(10, "amount")
            out.append(_hit(cid, "R09", g.timestamp.max(), g.txn_id, v,
                            f"Monthly volume {_fmt(v)} is {mult:.1f}x the KYC expected {_fmt(exp[cid])}",
                            20 + min(60, 8 * mult)))
    return out


# ----------------------------------------------------------------------------- R10
def r10_shared_device(cust, tx, p):
    # devices seen in online/mobile sessions, plus devices registered at onboarding (KYC)
    d = tx[tx.device_id != ""].groupby(["device_id", "customer_id"]).timestamp.min().reset_index()
    reg = cust[["device_id", "customer_id"]].assign(timestamp=tx.timestamp.min())
    d = pd.concat([d, reg]).groupby(["device_id", "customer_id"]).timestamp.min().reset_index()
    out = []
    for dev, g in d.groupby("device_id"):
        if g.customer_id.nunique() < p["min_customers_per_device"]:
            continue
        g = g.sort_values("timestamp")
        crossed = g.timestamp.iloc[p["min_customers_per_device"] - 1]
        for r in g.itertuples():
            ids = tx[(tx.customer_id == r.customer_id) & (tx.device_id == dev)].txn_id.head(25)
            out.append(_hit(r.customer_id, "R10", max(crossed, r.timestamp), ids, 0,
                            f"Device {dev} used by {len(g)} customers: {', '.join(g.customer_id)}",
                            40 + 10 * len(g)))
    return out


RULES = {"R01": r01_structuring, "R02": r02_rapid_movement, "R03": r03_funnel, "R04": r04_high_risk_geo,
         "R05": r05_round_dollar, "R06": r06_dormant, "R07": r07_tbml, "R08": r08_mule,
         "R09": r09_profile_deviation, "R10": r10_shared_device}


def run_rule(rule_id, cust, tx, params) -> pd.DataFrame:
    hits = RULES[rule_id](cust, tx, params[PARAM_KEYS[rule_id]])
    return consolidate(pd.DataFrame(hits))


def consolidate(hits: pd.DataFrame) -> pd.DataFrame:
    """Roll raw hits into one alert per customer / rule / month."""
    cols = ["customer_id", "rule_id", "alert_month", "alert_date", "severity", "amount_involved", "n_hits", "details", "txn_ids"]
    if hits.empty:
        return pd.DataFrame(columns=cols)
    hits = hits.copy()
    hits["alert_month"] = hits.alert_date.dt.to_period("M").astype(str)
    agg = hits.groupby(["customer_id", "rule_id", "alert_month"]).agg(
        alert_date=("alert_date", "max"), severity=("severity", "max"), amount_involved=("amount_involved", "sum"),
        n_hits=("details", "size"), details=("details", lambda s: " | ".join(s.head(3)) + (f" | (+{len(s) - 3} more)" if len(s) > 3 else "")),
        txn_ids=("txn_ids", lambda s: ";".join(dict.fromkeys(t for lst in s for t in lst)))).reset_index()
    agg["severity"] = agg["severity"].round(1)
    return agg[cols]


def run_rules(cust, tx, params) -> pd.DataFrame:
    frames = []
    for rid in RULES:
        if params[PARAM_KEYS[rid]].get("enabled", True):
            frames.append(run_rule(rid, cust, tx, params))
    alerts = pd.concat([f for f in frames if not f.empty], ignore_index=True)
    alerts = alerts.sort_values(["alert_date", "customer_id"]).reset_index(drop=True)
    alerts.insert(0, "alert_id", [f"ALT-{i:05d}" for i in range(1, len(alerts) + 1)])
    alerts.insert(3, "rule_name", alerts.rule_id.map(RULE_NAMES))
    alerts["status"] = "OPEN"
    return alerts
