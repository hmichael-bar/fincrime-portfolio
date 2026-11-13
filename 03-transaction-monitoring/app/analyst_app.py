"""L1 analyst workbench (Streamlit). SYNTHETIC DATA ONLY.

Run from the project folder:
    streamlit run app/analyst_app.py

Pick an alert from the queue, review the customer's KYC profile and transaction
timeline, then record a disposition. Dispositions are appended to
outputs/dispositions_log.csv (an audit trail: who decided what, when, and why).
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from rules import RULE_NAMES, load_data  # noqa: E402

LOG = ROOT / "outputs" / "dispositions_log.csv"
WORKED = ROOT / "dispositions"

DECISIONS = ["Close - false positive", "Close - activity consistent with KYC / explained",
             "Escalate to Level 2 investigation", "Escalate - recommend SAR filing"]
REASONS = ["Activity matches stated occupation / business", "Documented one-off life event",
           "Counterparty verified as legitimate", "Known payroll / government / platform source",
           "Pattern consistent with structuring", "Pass-through with no economic purpose",
           "Funnel / third-party cash deposits", "Mule indicators (many senders, fast outflow)",
           "High-risk jurisdiction without explanation", "Trade activity inconsistent with KYC",
           "Other (explain in narrative)"]

st.set_page_config(page_title="TM Analyst Workbench (synthetic)", layout="wide")


@st.cache_data
def load():
    cust, tx = load_data()
    alerts = pd.read_csv(ROOT / "outputs" / "alerts.csv", parse_dates=["alert_date"])
    scores = pd.read_csv(ROOT / "outputs" / "customer_risk_scores.csv")
    return cust, tx, alerts, scores


def load_log() -> pd.DataFrame:
    if LOG.exists():
        return pd.read_csv(LOG)
    return pd.DataFrame(columns=["timestamp", "analyst", "alert_id", "customer_id", "rule_id", "decision", "reason_code", "narrative"])


cust, tx, alerts, scores = load()
log = load_log()
score_by = scores.set_index("customer_id")
worked = {p.stem.split("_")[0]: p for p in WORKED.glob("ALT-*.md")}

st.title("Transaction Monitoring: L1 Analyst Workbench")
st.caption("Meridian Harbor Bank (fictional). All customers, accounts and transactions are synthetic.")

# ----------------------------------------------------------------------- queue
with st.sidebar:
    st.header("Alert queue")
    rules_sel = st.multiselect("Rule", sorted(alerts.rule_id.unique()), format_func=lambda r: f"{r} {RULE_NAMES[r][:28]}")
    status_sel = st.radio("Status", ["Open", "Dispositioned", "All"], horizontal=True)
    only_worked = st.checkbox("Only alerts with a worked example", value=False)
    sort_by = st.selectbox("Sort by", ["Customer risk score", "Severity", "Alert date"])
    q = alerts.copy()
    q["risk_score"] = q.customer_id.map(score_by.risk_score)
    q["customer"] = q.customer_id.map(cust.set_index("customer_id").name)
    done = set(log.alert_id)
    q["status"] = q.alert_id.map(lambda a: "Dispositioned" if a in done else "Open")
    if rules_sel:
        q = q[q.rule_id.isin(rules_sel)]
    if status_sel != "All":
        q = q[q.status == status_sel]
    if only_worked:
        q = q[q.alert_id.isin(worked)]
    key = {"Customer risk score": "risk_score", "Severity": "severity", "Alert date": "alert_date"}[sort_by]
    q = q.sort_values(key, ascending=False)
    st.caption(f"{len(q)} alerts")
    if q.empty:
        st.info("No alerts match the filters.")
        st.stop()
    label = q.apply(lambda r: f"{r.alert_id} | {r.rule_id} | {r.customer_id} | score {r.risk_score:.0f}", axis=1)
    pick = st.selectbox("Open alert", q.alert_id, format_func=dict(zip(q.alert_id, label)).get)

a = alerts.set_index("alert_id").loc[pick]
c = cust.set_index("customer_id").loc[a.customer_id]
s = score_by.loc[a.customer_id]
ctx = tx[tx.customer_id == a.customer_id].copy()
flagged = set(str(a.txn_ids).split(";"))
ctx["flagged"] = ctx.txn_id.isin(flagged)

# --------------------------------------------------------------- alert header
st.subheader(f"{pick}: {a.rule_name}")
m = st.columns(5)
m[0].metric("Rule", a.rule_id)
m[1].metric("Alert date", a.alert_date.strftime("%Y-%m-%d"))
m[2].metric("Severity", f"{a.severity:.0f}")
m[3].metric("Amount involved", f"${a.amount_involved:,.0f}")
m[4].metric("Customer risk score", f"{s.risk_score:.0f} / 100")
st.info(f"**Why it fired:** {a.details}")

left, right = st.columns([1, 1])
with left:
    st.markdown("#### Customer profile (KYC)")
    prof = {
        "Customer": f"{c['name']} ({a.customer_id})", "Type": c.customer_type, "Occupation / business": c.occupation,
        "Beneficial owner": c.beneficial_owner or "n/a", "Age": c.age, "Nationality": c.nationality,
        "Home state / branch": f"{c.home_state} / {c.home_branch}",
        "Account opened": pd.Timestamp(c.account_open_date).date(),
        "Expected monthly volume": f"${c.expected_monthly_volume_usd:,.0f}",
        "Expected monthly txns": c.expected_monthly_txn_count, "Expected cash activity": c.expected_cash_activity,
        "Expected countries": c.expected_countries or "none (domestic only)",
        "Expected goods": c.expected_goods or "n/a", "PEP": "Yes" if c.pep_flag else "No",
        "KYC risk rating": c.kyc_risk_rating,
    }
    st.table(pd.DataFrame(prof.items(), columns=["Field", "Value"]).set_index("Field").astype(str))
with right:
    st.markdown("#### Risk context")
    st.write(f"**Anomaly model:** percentile {s.anomaly_pct:.0%}" + (" (flagged as outlier)" if s.is_anomaly else ""))
    st.write(f"**Top anomaly drivers:** {s.top_drivers}")
    other = alerts[(alerts.customer_id == a.customer_id) & (alerts.alert_id != pick)]
    st.write(f"**Other alerts on this customer:** {len(other)}")
    if len(other):
        st.dataframe(other[["alert_id", "rule_id", "alert_month", "severity", "details"]], hide_index=True, height=200)
    mon = ctx.groupby([ctx.timestamp.dt.to_period("M").astype(str), "direction"]).amount.sum().unstack(fill_value=0)
    mon["expected"] = c.expected_monthly_volume_usd
    st.markdown("**Monthly in/out vs expected volume**")
    st.dataframe(mon.style.format("${:,.0f}"))

# ------------------------------------------------------------------- timeline
st.markdown("#### Transaction timeline")
ctx["plot_amount"] = ctx.amount.clip(lower=1)
ctx["signed"] = ctx.apply(lambda r: r.amount if r.direction == "IN" else -r.amount, axis=1)
chart = alt.Chart(ctx).mark_circle(opacity=0.75).encode(
    x=alt.X("timestamp:T", title=None),
    y=alt.Y("plot_amount:Q", scale=alt.Scale(type="log"), title="Amount (USD, log scale)"),
    color=alt.Color("txn_type:N", title="Type"),
    size=alt.condition(alt.datum.flagged, alt.value(140), alt.value(25)),
    stroke=alt.condition(alt.datum.flagged, alt.value("#0b0b0b"), alt.value(None)),
    tooltip=["txn_id", "timestamp:T", "txn_type", alt.Tooltip("amount:Q", format="$,.2f"), "counterparty_name",
             "counterparty_country", "branch_id", "memo", "flagged"],
).properties(height=320).interactive()
rule_line = alt.Chart(pd.DataFrame({"y": [10000]})).mark_rule(strokeDash=[4, 4], color="#898781").encode(y="y:Q")
st.altair_chart(chart + rule_line, width="stretch")
st.caption("Large outlined dots = transactions that triggered this alert. Dashed line = $10,000 CTR threshold.")

cols = ["txn_id", "timestamp", "txn_type", "amount", "channel", "branch_id", "branch_state", "counterparty_name",
        "counterparty_country", "memo", "device_id"]
st.markdown("**Triggering transactions**")
st.dataframe(ctx[ctx.flagged][cols].style.format({"amount": "${:,.2f}"}), hide_index=True)
with st.expander(f"All {len(ctx)} transactions for this customer"):
    st.dataframe(ctx[cols + ["flagged"]].sort_values("timestamp"), hide_index=True)
with st.expander("Counterparty summary"):
    cp = ctx.groupby(["counterparty_name", "counterparty_country", "direction"]).amount.agg(["count", "sum"]).sort_values("sum", ascending=False)
    st.dataframe(cp.style.format({"sum": "${:,.0f}"}))

# ----------------------------------------------------------------- disposition
st.markdown("---")
st.markdown("#### Disposition")
if pick in worked:
    with st.expander("Worked example for this alert (from /dispositions)", expanded=False):
        st.markdown(worked[pick].read_text())
prior = log[log.alert_id == pick]
if len(prior):
    st.warning("This alert already has a disposition on file:")
    st.dataframe(prior, hide_index=True)
with st.form("disposition"):
    analyst = st.text_input("Analyst ID", value="L1-ANALYST-01")
    decision = st.radio("Decision", DECISIONS)
    reason = st.selectbox("Primary reason code", REASONS)
    narrative = st.text_area("Rationale (facts reviewed, what explains or does not explain the activity)", height=160,
                             placeholder="Reviewed 6 months of activity. ... Activity is consistent with ... Closing as ... / Escalating because ...")
    submitted = st.form_submit_button("Save disposition")
if submitted:
    if len(narrative.strip()) < 40:
        st.error("Write a rationale of at least a couple of sentences. An examiner must be able to follow your reasoning.")
    else:
        row = pd.DataFrame([dict(timestamp=datetime.now().isoformat(timespec="seconds"), analyst=analyst, alert_id=pick,
                                 customer_id=a.customer_id, rule_id=a.rule_id, decision=decision, reason_code=reason,
                                 narrative=narrative.strip())])
        row.to_csv(LOG, mode="a", header=not LOG.exists(), index=False)
        st.success(f"Saved disposition for {pick}: {decision}")
