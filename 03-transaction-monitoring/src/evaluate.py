"""Score the detection stack against the seeded ground truth and run threshold-tuning sweeps.

Ground truth is read HERE ONLY, after detection has run.
Unit of evaluation: the customer. An alert is a "true positive alert" when it fires on a
customer who was seeded as a bad actor (the way a bank would judge an alert after
investigation). Recall = share of bad-actor customers with at least one alert.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.metrics import average_precision_score, roc_auc_score  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from anomaly import score_customers  # noqa: E402
from rules import PARAM_KEYS, RULE_NAMES, run_rule, run_rules  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
CHARTS = OUT / "charts"

TARGET = {"R01": "structuring", "R02": "rapid_movement", "R03": "funnel", "R04": "high_risk_geo",
          "R05": "round_dollar", "R06": "dormant_reactivation", "R07": "tbml", "R08": "mule_network",
          "R09": None, "R10": "mule_network"}

# chart styling: validated reference palette (light mode, static PNG)
INK, INK2, MUTED, GRID, BASE, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "axes.edgecolor": BASE,
                     "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.spines.top": False,
                     "axes.spines.right": False, "font.size": 10, "axes.titlesize": 11,
                     "axes.titleweight": "bold", "axes.titlecolor": INK, "legend.frameon": False})


def load_truth():
    gt = pd.read_csv(ROOT / "data" / "ground_truth_customers.csv")
    return gt.set_index("customer_id")


def rule_metrics(alerts, gt):
    sus = gt[gt.is_suspicious]
    rows = []
    for rid in sorted(RULE_NAMES):
        a = alerts[alerts.rule_id == rid]
        tp = a.customer_id.map(gt.is_suspicious).fillna(False)
        tgt = TARGET[rid]
        tgt_ids = set(sus.index) if tgt is None else set(sus[sus.typology == tgt].index)
        caught = len(tgt_ids & set(a.customer_id))
        rows.append(dict(rule_id=rid, rule=RULE_NAMES[rid], alerts=len(a), true_positive_alerts=int(tp.sum()),
                         precision=round(tp.mean(), 3) if len(a) else np.nan,
                         customers_alerted=a.customer_id.nunique(),
                         target_typology=tgt or "(all typologies)",
                         target_recall=round(caught / len(tgt_ids), 3) if tgt_ids else np.nan))
    return pd.DataFrame(rows)


def typology_table(alerts, anomaly, gt):
    sus = gt[gt.is_suspicious]
    alerted = set(alerts.customer_id)
    flagged = set(anomaly[anomaly.is_anomaly].customer_id)
    designed = {t: set(alerts[alerts.rule_id.isin([r for r, tt in TARGET.items() if tt == t])].customer_id) for t in sus.typology.unique()}
    rows = []
    for t, g in sus.groupby("typology"):
        ids = set(g.index)
        rows.append(dict(typology=t, customers=len(ids), caught_by_any_rule=len(ids & alerted),
                         caught_by_designed_rule=len(ids & designed[t]), flagged_by_isolation_forest=len(ids & flagged),
                         caught_by_rules_or_model=len(ids & (alerted | flagged))))
    return pd.DataFrame(rows)


def precision_at_k(scores: pd.Series, labels: pd.Series, k: int) -> float:
    top = scores.sort_values(ascending=False).head(k).index
    return float(labels.reindex(top).mean())


def sweep(rule_id, param, values, cust, tx, params, gt):
    sus = gt[gt.is_suspicious]
    tgt = TARGET[rule_id]
    tgt_ids = set(sus.index) if tgt is None else set(sus[sus.typology == tgt].index)
    rows = []
    for v in values:
        p = copy.deepcopy(params)
        p[PARAM_KEYS[rule_id]][param] = v
        a = run_rule(rule_id, cust, tx, p)
        tp = a.customer_id.map(gt.is_suspicious).fillna(False) if len(a) else pd.Series(dtype=bool)
        rows.append(dict(rule_id=rule_id, parameter=param, value=v, alerts=len(a), true_positive_alerts=int(tp.sum()),
                         false_positive_alerts=int(len(a) - tp.sum()),
                         precision=round(tp.mean(), 3) if len(a) else np.nan,
                         target_recall=round(len(tgt_ids & set(a.customer_id)) / len(tgt_ids), 3),
                         is_production=v == params[PARAM_KEYS[rule_id]][param]))
    return pd.DataFrame(rows)


SWEEPS = [
    ("R01", "lower_bound", [5000, 6000, 7000, 7500, 8000, 8500, 9000, 9500]),
    ("R02", "pass_through_ratio", [0.5, 0.6, 0.7, 0.8, 0.9, 0.95]),
    ("R02", "min_inflow", [10000, 15000, 20000, 30000, 50000, 75000]),
    ("R04", "suppress_if_country_in_kyc_profile", [False, True]),
    ("R05", "min_count_per_month", [1, 2, 3, 4]),
    ("R07", "min_conditions", [1, 2, 3]),
    ("R08", "min_unique_senders", [4, 6, 8, 10, 15, 20, 30]),
    ("R08", "require_secondary_indicator", [False, True]),
    ("R09", "volume_multiplier", [1.5, 2.0, 3.0, 4.0, 6.0, 10.0]),
    ("R10", "min_customers_per_device", [2, 3, 4]),
]

PRESETS = {  # whole-program settings: what an institution might choose
    "aggressive": {"R01_structuring": {"lower_bound": 6000}, "R02_rapid_movement": {"pass_through_ratio": 0.6, "min_inflow": 10000},
                   "R04_high_risk_geography": {"suppress_if_country_in_kyc_profile": False},
                   "R05_round_dollar_wires": {"min_count_per_month": 1}, "R07_tbml_invoice_pattern": {"min_conditions": 1},
                   "R08_mule_activity": {"min_unique_senders": 6, "require_secondary_indicator": False},
                   "R09_profile_deviation": {"volume_multiplier": 2.0}, "R10_shared_device": {"min_customers_per_device": 2}},
    "baseline": {},
    "conservative": {"R01_structuring": {"lower_bound": 9000, "min_count": 3}, "R02_rapid_movement": {"pass_through_ratio": 0.9, "min_inflow": 50000},
                     "R05_round_dollar_wires": {"min_count_per_month": 3}, "R07_tbml_invoice_pattern": {"min_conditions": 3},
                     "R08_mule_activity": {"min_unique_senders": 20}, "R09_profile_deviation": {"volume_multiplier": 6.0},
                     "R10_shared_device": {"min_customers_per_device": 4}},
}


def apply_preset(params, preset):
    p = copy.deepcopy(params)
    for k, v in PRESETS[preset].items():
        p[k].update(v)
    return p


# ------------------------------------------------------------------------- charts
def chart_tradeoff(sw: pd.DataFrame, rule_id, param, path):
    """Alert volume (x) vs detection (y), one point per threshold. Single axis by design."""
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.plot(sw.alerts, sw.target_recall * 100, color=SERIES[0], lw=2, marker="o", ms=8,
            markeredgecolor=SURF, markeredgewidth=2, zorder=3)
    prod = sw[sw.is_production]
    ax.scatter(prod.alerts, prod.target_recall * 100, s=150, facecolor="none", edgecolor=SERIES[1], lw=2, zorder=4)
    for i, r in enumerate(sw.itertuples()):  # alternate above/below so neighbouring labels don't collide
        ax.annotate(f"{r.value}", (r.alerts, r.target_recall * 100), textcoords="offset points",
                    xytext=(4, 9 if i % 2 else -15), fontsize=8, color=INK2)
    ax.set_xlabel("Alerts generated (6 months)")
    ax.set_ylabel(f"Recall on {TARGET[rule_id] or 'all typologies'} (%)")
    ax.set_ylim(-5, 108)
    ax.set_title(f"{rule_id}: alert volume vs detection, sweeping {param}", loc="left")
    ax.text(0, -0.2, "Each point is one threshold value. Ringed point = current production setting.",
            transform=ax.transAxes, fontsize=8, color=MUTED)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def chart_presets(pre: pd.DataFrame, path):
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))
    names = list(pre.preset)
    axes[0].bar(names, pre.alerts, color=SERIES[0], width=0.55)
    axes[0].set_title("Alert volume", loc="left")
    for i, v in enumerate(pre.alerts):
        axes[0].text(i, v, f"{v:,}", ha="center", va="bottom", fontsize=9, color=INK)
    axes[1].bar(names, pre.customer_recall * 100, color=SERIES[2], width=0.55)
    axes[1].set_title("Bad actors detected (%)", loc="left")
    axes[1].set_ylim(0, 110)
    for i, v in enumerate(pre.customer_recall * 100):
        axes[1].text(i, v, f"{v:.0f}%", ha="center", va="bottom", fontsize=9, color=INK)
    for ax in axes:
        ax.grid(axis="x", visible=False)
    fig.suptitle("Program-wide threshold presets: workload vs detection", x=0.01, ha="left", fontweight="bold", color=INK)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def chart_contamination(cs: pd.DataFrame, path):
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.plot(cs.contamination * 100, cs.recall * 100, color=SERIES[0], lw=2, marker="o", ms=7, label="Recall")
    ax.plot(cs.contamination * 100, cs.precision * 100, color=SERIES[1], lw=2, marker="s", ms=7, label="Precision")
    for name, col, ser in (("Recall", SERIES[0], cs.recall), ("Precision", SERIES[1], cs.precision)):
        ax.annotate(name, (cs.contamination.iloc[-1] * 100, ser.iloc[-1] * 100), xytext=(6, 0),
                    textcoords="offset points", color=INK2, fontsize=9, va="center")
    ax.set_xlabel("Share of customers the Isolation Forest flags (%)")
    ax.set_ylabel("%")
    ax.set_ylim(0, 105)
    ax.legend(loc="lower center", ncol=2, bbox_to_anchor=(0.5, 1.0))
    ax.set_title("Isolation Forest: how many to flag?", loc="left", pad=24)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def chart_precision_at_k(pk: pd.DataFrame, path):
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    labels = {"combined_score": "Combined (rules + model)", "rules_only": "Rule points only",
              "anomaly_only": "Isolation Forest only", "combined_plus_10pct_kyc": "Combined + 10% KYC rating"}
    for i, col in enumerate(labels):
        ax.plot(pk.k, pk[col] * 100, lw=2, marker="o", ms=7, color=SERIES[i], label=labels[col])
    ax.axhline(pk.base_rate.iloc[0] * 100, color=MUTED, lw=1, ls="--")
    ax.text(pk.k.iloc[-1], pk.base_rate.iloc[0] * 100 + 2, "random review", ha="right", fontsize=8, color=MUTED)
    ax.set_xlabel("Top-k customers reviewed")
    ax.set_ylabel("Share that are seeded bad actors (%)")
    ax.set_ylim(0, 105)
    ax.legend(loc="lower center", ncol=2, bbox_to_anchor=(0.5, 1.0), fontsize=8)
    ax.set_title("Prioritising the queue: precision@k", loc="left", pad=34)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


# ------------------------------------------------------------------------ report
def md_table(df: pd.DataFrame, floatfmt="{:.2f}") -> str:
    def f(x):
        if isinstance(x, float):
            return "" if np.isnan(x) else floatfmt.format(x)
        return str(x)
    head = "| " + " | ".join(df.columns) + " |\n|" + "|".join("---" for _ in df.columns) + "|\n"
    return head + "\n".join("| " + " | ".join(f(v) for v in row) + " |" for row in df.itertuples(index=False))


def evaluate(cust, tx, params, alerts, anomaly, scores):
    CHARTS.mkdir(parents=True, exist_ok=True)
    gt = load_truth()
    labels = gt.is_suspicious
    rm = rule_metrics(alerts, gt)
    tt = typology_table(alerts, anomaly, gt)

    alerted = set(alerts.customer_id)
    tp_alerts = alerts.customer_id.map(labels).fillna(False)
    overall = dict(customers=len(cust), transactions=len(tx), seeded_bad_actors=int(labels.sum()),
                   alerts=len(alerts), true_positive_alerts=int(tp_alerts.sum()),
                   alert_precision=round(float(tp_alerts.mean()), 3),
                   customers_alerted=len(alerted),
                   good_customers_alerted=int((~labels.reindex(list(alerted)).astype(bool)).sum()),
                   customer_recall=round(len(alerted & set(labels[labels].index)) / int(labels.sum()), 3),
                   alerts_per_analyst_day=round(len(alerts) / 125, 1))

    an = anomaly.set_index("customer_id")
    y = labels.reindex(an.index).astype(int)
    iso = dict(roc_auc=round(roc_auc_score(y, an.anomaly_score), 3),
               average_precision=round(average_precision_score(y, an.anomaly_score), 3),
               flagged=int(an.is_anomaly.sum()),
               precision=round(float(y[an.is_anomaly].mean()), 3),
               recall=round(float(an.is_anomaly[y == 1].mean()), 3),
               ml_only_bad_actors=sorted(set(an[an.is_anomaly].index) & set(labels[labels].index) - alerted),
               ml_only_good=int(len(set(an[an.is_anomaly].index) - set(labels[labels].index) - alerted)))

    sc = scores.set_index("customer_id")
    p_kyc = copy.deepcopy(params)
    p_kyc["combined_score_weights"] = {"rules": 0.45, "anomaly": 0.45, "kyc_risk": 0.10}
    from anomaly import combined_scores
    sc_kyc = combined_scores(cust, alerts, anomaly, p_kyc).set_index("customer_id")
    pk_rows = []
    for k in (10, 25, 50, 75, 100):
        pk_rows.append(dict(k=k, combined_score=precision_at_k(sc.risk_score, labels, k),
                            rules_only=precision_at_k(sc.rule_points + 1e-9 * sc.anomaly_pct, labels, k),
                            anomaly_only=precision_at_k(sc.anomaly_score, labels, k),
                            combined_plus_10pct_kyc=precision_at_k(sc_kyc.risk_score, labels, k),
                            base_rate=float(labels.mean())))
    pk = pd.DataFrame(pk_rows)

    # tuning
    sweeps = []
    for rid, param, vals in SWEEPS:
        sw = sweep(rid, param, vals, cust, tx, params, gt)
        sweeps.append(sw)
        if param not in ("suppress_if_country_in_kyc_profile", "require_secondary_indicator"):
            chart_tradeoff(sw, rid, param, CHARTS / f"tuning_{rid}_{param}.png")
    sweeps = pd.concat(sweeps, ignore_index=True)

    pre_rows = []
    for name in PRESETS:
        a = run_rules(cust, tx, apply_preset(params, name))
        tp = a.customer_id.map(labels).fillna(False)
        caught = set(a.customer_id) & set(labels[labels].index)
        rescued = (set(an[an.is_anomaly].index) & set(labels[labels].index)) - caught
        pre_rows.append(dict(preset=name, alerts=len(a), alert_precision=round(float(tp.mean()), 3),
                             customer_recall=round(len(caught) / int(labels.sum()), 3),
                             missed_bad_actors=int(labels.sum()) - len(caught),
                             of_which_isolation_forest_flags=len(rescued)))
    pre = pd.DataFrame(pre_rows)
    chart_presets(pre, CHARTS / "presets_volume_vs_detection.png")

    cs_rows = []
    for c in (0.02, 0.05, 0.08, 0.10, 0.15, 0.20, 0.30):
        p = copy.deepcopy(params)
        p["anomaly_model"]["contamination"] = c
        s = score_customers(cust, tx, p).set_index("customer_id")
        yy = labels.reindex(s.index).astype(int)
        cs_rows.append(dict(contamination=c, flagged=int(s.is_anomaly.sum()), precision=round(float(yy[s.is_anomaly].mean()), 3),
                            recall=round(float(s.is_anomaly[yy == 1].mean()), 3)))
    cs = pd.DataFrame(cs_rows)
    chart_contamination(cs, CHARTS / "isolation_forest_contamination.png")
    chart_precision_at_k(pk, CHARTS / "precision_at_k.png")

    rm.to_csv(OUT / "rule_metrics.csv", index=False)
    sweeps.to_csv(OUT / "tuning_results.csv", index=False)
    pre.to_csv(OUT / "preset_results.csv", index=False)
    metrics = dict(overall=overall, isolation_forest=iso, presets=pre_rows, precision_at_k=pk_rows)
    (OUT / "metrics.json").write_text(json.dumps(metrics, indent=2, default=str))
    write_report(overall, rm, tt, iso, pk, sweeps, pre, cs, params)
    return metrics


def write_report(overall, rm, tt, iso, pk, sweeps, pre, cs, params):
    o = overall
    lines = [
        "# Evaluation report (auto-generated)",
        "",
        "> Synthetic data. Generated by `src/run_pipeline.py`. Do not edit by hand; rerun the pipeline.",
        "",
        "## Headline",
        "",
        f"- **{o['customers']}** customers, **{o['transactions']:,}** transactions, **{o['seeded_bad_actors']}** seeded bad actors.",
        f"- Production thresholds produced **{o['alerts']}** alerts on **{o['customers_alerted']}** customers.",
        f"- Alert precision **{o['alert_precision']:.0%}** ({o['true_positive_alerts']} alerts were on bad actors); "
        f"**{o['good_customers_alerted']}** legitimate customers were alerted at least once.",
        f"- Customer recall **{o['customer_recall']:.0%}**: share of bad actors with at least one alert.",
        f"- Workload: about **{o['alerts_per_analyst_day']}** alerts per business day over the 6 months.",
        "",
        "Why precision looks high: this population is *enriched*. About 11% of customers are bad actors; in a real bank "
        "it is well under 1%, so real alert precision is often in the single digits. The relative comparisons "
        "between thresholds are the useful part.",
        "",
        "## Per-rule performance",
        "",
        "`target_recall` = share of the customers seeded with the typology the rule was designed for who got at least one alert from that rule.",
        "",
        md_table(rm),
        "",
        "## Detection by typology",
        "",
        md_table(tt),
        "",
        "Customers caught by a rule *other than* the designed one were caught for the wrong reason. That still counts "
        "at customer level (the investigator reviews the whole relationship), but it is luck, not design.",
        "",
        "## Second line: Isolation Forest",
        "",
        f"- ROC AUC **{iso['roc_auc']}**, average precision **{iso['average_precision']}** (random = {o['seeded_bad_actors'] / o['customers']:.2f}).",
        f"- At contamination {params['anomaly_model']['contamination']}: flags **{iso['flagged']}** customers, "
        f"precision **{iso['precision']:.0%}**, recall **{iso['recall']:.0%}**.",
        f"- Bad actors flagged by the model but missed by every rule: **{len(iso['ml_only_bad_actors'])}** "
        f"{iso['ml_only_bad_actors'] or ''}; legitimate customers flagged only by the model: **{iso['ml_only_good']}**.",
        "",
        md_table(cs),
        "",
        "![contamination](charts/isolation_forest_contamination.png)",
        "",
        "## Prioritising the queue (precision@k)",
        "",
        "If an analyst team can only work the top k customers, how many are real? Combined score = "
        f"{params['combined_score_weights']['rules']} x rule-points percentile + {params['combined_score_weights']['anomaly']} x anomaly percentile "
        f"+ {params['combined_score_weights']['kyc_risk']} x KYC risk.",
        "",
        md_table(pk),
        "",
        "Adding the static KYC risk rating *lowers* precision here: the rating describes exposure (cash-intensive "
        "business, import/export, foreign nationality), and most seeded bad actors were onboarded as ordinary "
        "low-risk individuals. Behaviour beats profile for ranking alerts; the rating still matters for EDD and review frequency.",
        "",
        "![precision at k](charts/precision_at_k.png)",
        "",
        "## Threshold tuning",
        "",
        "### Program-wide presets",
        "",
        md_table(pre),
        "",
        "![presets](charts/presets_volume_vs_detection.png)",
        "",
        "### Single-parameter sweeps",
        "",
        md_table(sweeps.drop(columns=["is_production"]).assign(value=sweeps.value.astype(str))),
        "",
    ]
    for rid, param, _ in SWEEPS:
        if param not in ("suppress_if_country_in_kyc_profile", "require_secondary_indicator"):
            lines += [f"![{rid} {param}](charts/tuning_{rid}_{param}.png)", ""]
    (OUT / "evaluation_report.md").write_text("\n".join(lines))
