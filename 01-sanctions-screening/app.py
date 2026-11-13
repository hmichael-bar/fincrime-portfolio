"""Streamlit UI for the sanctions screening engine.   Run:  streamlit run app.py"""
from __future__ import annotations

import io
from pathlib import Path

import pandas as pd
import streamlit as st

from sanctions_screener import Screener
from sanctions_screener.batch import screen_customers
from sanctions_screener.matcher import DEFAULT_THRESHOLD

st.set_page_config(page_title="OFAC Sanctions Screener", page_icon="🛡️", layout="wide")

BADGE = {"True Match": "🔴", "Potential Match - escalate": "🟠", "False Positive": "🔵", "No Match": "🟢"}


@st.cache_resource(show_spinner="Loading OFAC lists...")
def get_screener(include_cons: bool) -> Screener:
    return Screener(include_consolidated=include_cons)


with st.sidebar:
    st.header("Settings")
    threshold = st.slider("Match threshold", 60, 100, DEFAULT_THRESHOLD, 1,
                          help="Hits scoring below this are not shown. Lower = more alerts, fewer misses.")
    include_cons = st.checkbox("Include Consolidated (non-SDN) list", True)
    max_hits = st.number_input("Max hits per customer", 1, 20, 5)
    s = get_screener(include_cons)
    st.caption(f"{s.stats['sdn_entries']:,} SDN + {s.stats['consolidated_entries']:,} non-SDN entries, "
               f"{s.stats['names_incl_aliases']:,} names incl. aliases.")
    st.caption("Source: U.S. Treasury OFAC public list files. Demo tool - not legal advice.")

st.title("🛡️ OFAC Sanctions Screening Engine")
st.write("Fuzzy name screening against the SDN and Consolidated lists, with transliteration-aware "
         "handling of Arabic names. Every hit comes with the reasons it matched and a suggested disposition.")

tab1, tab2 = st.tabs(["Screen a name", "Batch screen a CSV"])

with tab1:
    c1, c2, c3, c4 = st.columns([3, 1.2, 1.2, 1.4])
    name = c1.text_input("Name (Latin or Arabic script)", "Moammar Abu Minyar El-Gaddafi")
    ctype = c2.selectbox("Type", ["individual", "entity"])
    dob = c3.text_input("DOB (YYYY-MM-DD or YYYY)", "1942")
    nat = c4.text_input("Nationality", "Libya")
    owners = ""
    if ctype == "entity":
        owners = st.text_input("Beneficial owners (Name|pct; Name|pct) - for the 50% Rule",
                               "Rami Makhluf|35;Iyad Makhlouf|20;Karim Haddad|45")
    if name.strip():
        r = s.screen(name, ctype, dob, nat, threshold=threshold, max_hits=max_hits, owners=owners)
        st.subheader(f"{BADGE.get(r.disposition, '')} {r.disposition}")
        st.markdown(f"**Normalised:** `{r.normalized.text}`")
        for n in r.normalized.notes:
            st.markdown(f"- {n}")
        if r.ownership_note:
            st.warning(r.ownership_note)
        if not r.hits:
            st.success("No list names at or above the threshold.")
        for i, h in enumerate(r.hits, 1):
            d = h.to_dict()
            with st.expander(f"{BADGE.get(d['disposition'], '')} {d['score']:.0f} - {d['primary_name']} "
                             f"({', '.join(d['programs'])}) - {d['disposition']}", expanded=(i == 1)):
                a, b = st.columns(2)
                a.markdown(f"**List:** {d['list']} `{d['uid']}`  \n**Type:** {d['type']}  \n"
                           f"**Matched on:** {d['matched_on']} - *{d['matched_name']}*  \n"
                           f"**Programs:** {', '.join(d['programs'])}")
                b.markdown(f"**DOB:** {'; '.join(d['dob']) or '-'}  \n**POB:** {'; '.join(d['pob']) or '-'}  \n"
                           f"**Nationality:** {', '.join(d['nationality']) or '-'}  \n"
                           f"**Address countries:** {', '.join(d['address_countries']) or '-'}")
                st.markdown(f"**Suggested disposition:** {d['disposition']} - {d['disposition_reason']}")
                st.markdown("**Why it matched**\n" + "\n".join(f"- {x}" for x in d["reasons"]))
                if d["secondary_checks"]:
                    st.markdown("**Secondary identifier checks**\n" +
                                "\n".join(f"- {x}" for x in d["secondary_checks"]))
                st.caption("Score components: " + ", ".join(f"{k} {v}" for k, v in d["score_components"].items()))

with tab2:
    st.write("CSV columns: `customer_id, name, type, dob, nationality, owners` (only `name` is required).")
    up = st.file_uploader("Upload customers CSV", type="csv")
    use_sample = st.button("Use the sample file (40 fictional customers)")
    df = None
    if up is not None:
        df = pd.read_csv(up, dtype=str).fillna("")
    elif use_sample:
        df = pd.read_csv(Path(__file__).parent / "sample_data" / "customers.csv", dtype=str).fillna("")
    if df is not None:
        customers = [{k.strip().lower(): v for k, v in row.items()} for row in df.to_dict("records")]
        with st.spinner(f"Screening {len(customers)} customers..."):
            results = screen_customers(s, customers, threshold, max_hits)
        rows = []
        for c, r in results:
            t = r.top
            rows.append({"ID": c.get("customer_id", ""), "Customer": c.get("name", ""),
                         "Disposition": f"{BADGE.get(r.disposition, '')} {r.disposition}",
                         "Score": round(t.score) if t else None, "Best match": t.entry.name if t else "",
                         "Program": ", ".join(t.entry.programs) if t else "",
                         "Hits": len(r.hits), "Reason": t.disposition_reason if t else r.ownership_note[:80]})
        out = pd.DataFrame(rows)
        counts = out["Disposition"].value_counts()
        cols = st.columns(len(counts))
        for col, (k, v) in zip(cols, counts.items()):
            col.metric(k, v)
        st.dataframe(out, use_container_width=True, hide_index=True)
        buf = io.StringIO()
        out.to_csv(buf, index=False)
        st.download_button("Download results CSV", buf.getvalue(), "screening_results.csv", "text/csv")
