import datetime as dt
import os

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import engine as E

HF, MF = "data/investors_13f.csv", "data/cusip_map.csv"
st.set_page_config("Efficiency Lab", "🧪", layout="wide")


def load_map():
    return {} if not os.path.exists(MF) else pd.read_csv(MF, dtype=str, keep_default_na=False).set_index("cusip").ticker.to_dict()


# ---------------- sidebar ----------------
with st.sidebar:
    st.markdown("### Efficiency Lab")
    dark = st.toggle("Dark mode", True)
    goal = st.selectbox("Goal", list(E.GOAL_MULT), 1)
    risk = st.selectbox("Risk tolerance", ["Low", "Medium", "High"], 1)
    horizon = st.slider("Horizon (years)", 1, 30, 10)
    years = st.slider("History window (years)", 2, 15, 5)
    rf = st.slider("Risk-free rate %", 0.0, 8.0, 4.0, .25) / 100
    skip = st.toggle("Skip assets with data problems", True, help="Crypto, mutual funds or new listings with <1y of data are dropped and weights renormalised instead of breaking the app.")
    n_p = st.slider("Portfolios to compare", 1, 3, 1)
    with st.expander("Score weights"):
        wts = {k: st.slider(k, 0, 100, d) for k, d in zip(E.COMPONENTS, [25, 25, 20, 10, 20])}
    with st.expander("13F investor data"):
        zips = st.file_uploader("SEC Form 13F data set zip(s)", type="zip", accept_multiple_files=True)
        if zips and st.button("Process zip(s)"):
            with st.spinner("Parsing 13F filings and mapping CUSIPs (can take a minute)…"):
                h = E.ingest_13f(zips)
                if h.empty:
                    st.error("None of the tracked investors found in these files.")
                else:
                    cm = E.map_cusips(h.cusip.unique(), load_map())
                    os.makedirs("data", exist_ok=True)
                    h.to_csv(HF, index=False)
                    pd.Series(cm, name="ticker").rename_axis("cusip").to_csv(MF)
                    st.rerun()
        if os.path.exists(HF):
            hh = pd.read_csv(HF)
            st.caption(f"{hh.investor.nunique()} investors loaded · latest period {hh.period.max()}")
            st.download_button("Download holdings CSV", hh.to_csv(index=False), "investors_13f.csv")
            if os.path.exists(MF):
                st.download_button("Download CUSIP map", open(MF).read(), "cusip_map.csv")
            st.caption("Commit both files to data/ in GitHub to make them permanent.")

C = dict(bg="#0b1220", card="#111a2e", fg="#e6edf7", mut="#8da2c0", line="#22304d") if dark else \
    dict(bg="#f4f6fa", card="#ffffff", fg="#0f1a2b", mut="#5b6b82", line="#dbe2ec")
ACC = "#4f9dff" if dark else "#1f6feb"
PAL = ["#4f9dff", "#f5b942", "#3ddc97", "#ff6b6b", "#b48cff", "#2ec4d6"]
st.markdown(f"""<style>
.stApp{{background:{C['bg']};-webkit-font-smoothing:antialiased;font-variant-numeric:tabular-nums}}
[data-testid=stSidebar]{{background:{C['card']}}}
h1,h2,h3,h4,label,p,li,[data-testid=stMetricValue],[data-testid=stMetricLabel],[data-testid=stCaptionContainer]{{color:{C['fg']}!important}}
[data-testid=stMetric]{{background:{C['card']};border:1px solid {C['line']};border-radius:12px;padding:14px 16px}}
.block-container{{padding-top:2rem;max-width:1300px}} h1{{text-wrap:balance}}
:focus-visible{{outline:2px solid {ACC};outline-offset:2px}}
[data-baseweb=tab-highlight]{{background-color:{ACC}!important}}
[data-baseweb=tab-panel]:not([hidden]){{opacity:1;transition:opacity 140ms cubic-bezier(.23,1,.32,1)}}
@starting-style{{[data-baseweb=tab-panel]:not([hidden]){{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{[data-baseweb=tab-panel]{{transition:none!important}}}}
</style>""", unsafe_allow_html=True)


def sty(fig, h=380):
    return fig.update_layout(template="plotly_dark" if dark else "plotly_white", height=h, paper_bgcolor="rgba(0,0,0,0)",
                             plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=10, t=40, b=10),
                             legend=dict(orientation="h", y=-.2), font=dict(color=C["fg"]))


# ---------------- input ----------------
st.title("Efficiency Lab")
st.caption("Enter holdings, get a diagnostic score, suggestions and comparisons. Historical, in-sample analysis: not financial advice.")
cols = ["A %", "B %", "C %"][:n_p]
base = pd.DataFrame({"Ticker": ["VTI", "BND", "QQQ", "GLD", "BTC-USD"], "A %": [40, 30, 15, 10, 5]})
for c in cols[1:]:
    base[c] = base["A %"]
ed = st.data_editor(base[["Ticker"] + cols], num_rows="dynamic", hide_index=True, key=f"ed{n_p}", width="stretch")
ed = ed.dropna(subset=["Ticker"])
ed["Ticker"] = ed.Ticker.astype(str).str.strip().str.upper()
ed = ed[ed.Ticker != ""].drop_duplicates("Ticker").set_index("Ticker")
W = {}
for c, name in zip(cols, "ABC"):
    s = ed[c].fillna(0).astype(float)
    s = s[s > 0]
    if s.empty:
        continue
    if abs(s.sum() - 100) > .01:
        st.caption(f"Portfolio {name}: weights sum to {s.sum():.1f}%, normalised to 100%.")
    W[name] = s / s.sum()
if not W:
    st.info("Enter at least one holding with a positive weight."); st.stop()

# ---------------- data ----------------
pool = {k: pd.Series(v, dtype=float) for k, v in {**E.BENCH, **E.MODELS}.items()}
cand = E.candidates(pd.read_csv(HF), load_map()) if os.path.exists(HF) else {}
inv = {k: v[0] for k, v in cand.items()}
tick = sorted(set().union(*[w.index for w in W.values()], *[p.index for p in pool.values()], *[p.index for p in inv.values()]))


@st.cache_data(ttl=21600, show_spinner="Downloading prices…")
def get(t, start):
    return E.weekly(t, start)


@st.cache_data(ttl=86400, show_spinner=False)
def meta1(t):
    return E.info(t)


try:
    P = get(tuple(tick), str(dt.date.today() - dt.timedelta(days=365 * years + 10)))
except Exception as ex:
    st.error(f"Price download failed: {ex}"); st.stop()
R = E.rets(P)
bad = sorted({t for w in W.values() for t in w.index if t not in R.columns or R[t].notna().sum() < 52})
if bad and not skip:
    st.error(f"Insufficient data for: {', '.join(bad)}. Enable “Skip assets with data problems” or remove them."); st.stop()
if bad:
    st.warning(f"Skipped (under 1 year of data or not found): {', '.join(bad)}. Remaining weights renormalised.")

eff, tv = E.effective(risk, goal, horizon)
res = {}
for name, w in W.items():
    pr, w2, sub = E.port(w, R)
    if len(pr) < 52:
        st.error(f"Portfolio {name}: not enough overlapping history."); st.stop()
    M = {t: meta1(t) for t in w2.index}
    res[name] = dict(pr=pr, w=w2, sub=sub, M=M, sc=E.score(w2, sub, pr, M, rf, eff, tv, wts))
st.caption(f"Profile: {goal} · {risk} risk tolerance · {horizon}y horizon → scored against {eff}-risk target volatility of {tv:.1%} · "
           f"overlap window {min(len(r['pr']) for r in res.values())} weeks")

tabs = st.tabs(["Score", "Suggestions", "Compare", "Similar investors", "Data & caveats"])

# ---------------- score ----------------
with tabs[0]:
    for col, (name, r) in zip(st.columns(len(res)), res.items()):
        tot, comp, s, kw, er = r["sc"]
        with col:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=tot, title={"text": f"Portfolio {name}"},
                                         gauge={"axis": {"range": [0, 100]}, "bar": {"color": ACC},
                                                "steps": [{"range": [0, 40], "color": "rgba(255,107,107,.25)"},
                                                          {"range": [40, 70], "color": "rgba(245,185,66,.25)"},
                                                          {"range": [70, 100], "color": "rgba(61,220,151,.25)"}]}))
            st.plotly_chart(sty(fig, 260), width="stretch")
            a, b = st.columns(2)
            a.metric("CAGR", f"{s['cagr']:.1%}"); b.metric("Volatility", f"{s['vol']:.1%}")
            a.metric("Sharpe", f"{s['sharpe']:.2f}"); b.metric("Max drawdown", f"{s['mdd']:.1%}")
    fig = go.Figure([go.Bar(name=f"Portfolio {n}", x=E.COMPONENTS, y=[r["sc"][1][k] for k in E.COMPONENTS], marker_color=PAL[i])
                     for i, (n, r) in enumerate(res.items())])
    fig.update_layout(barmode="group", title="Score components (0-100)", yaxis_range=[0, 100])
    st.plotly_chart(sty(fig), width="stretch")

# ---------------- suggestions ----------------
with tabs[1]:
    n = st.selectbox("Portfolio", list(res), key="sg")
    r = res[n]
    st.subheader("Rule-based flags")
    fl = E.rules(r["w"], r["sub"], r["M"], r["sc"][2], tv)
    for x in fl or ["No rule violations found."]:
        st.markdown(f"- {x}")
    st.subheader("Optimizer what-if")
    t = E.tilt(r["w"], r["sub"], rf) if len(r["w"]) > 1 else None
    if t is None:
        st.write("No improving shift found within ±10 percentage points.")
    else:
        d, s0, s1 = t
        st.markdown(f"Shifting weights by at most 10 points would move the historical Sharpe from **{s0:.2f}** to **{s1:.2f}**:")
        for k, v in d.items():
            st.markdown(f"- {'Increase' if v > 0 else 'Reduce'} **{k}** by {abs(v) * 100:.0f} pp ({r['w'][k]:.0%} → {r['w'][k] + v:.0%})")
        st.caption("In-sample optimisation on past returns: it describes history and overfits. Treat as a what-if, not a recommendation.")

# ---------------- compare ----------------
allp = {f"Your {n}": (r["pr"], r["w"]) for n, r in res.items()}
for grp in (pool, inv):
    for k, w in grp.items():
        pr, w2, _ = E.port(w, R)
        if len(pr) >= 52:
            allp[k] = (pr, w2)
with tabs[2]:
    rows = []
    for k, (pr, _) in allp.items():
        s = E.summ(pr, rf)
        rows.append({"Portfolio": k, "CAGR": s["cagr"], "Volatility": s["vol"], "Sharpe": s["sharpe"], "Max drawdown": s["mdd"], "Weeks": len(pr)})
    st.dataframe(pd.DataFrame(rows).style.format({"CAGR": "{:.1%}", "Volatility": "{:.1%}", "Sharpe": "{:.2f}", "Max drawdown": "{:.1%}"}),
                 hide_index=True, width="stretch")
    pick = st.multiselect("Plot growth of 1", list(allp), default=[k for k in allp if k.startswith("Your")] + ["SPY (US equity)"])
    fig = go.Figure()
    for i, k in enumerate(pick):
        g = (1 + allp[k][0]).cumprod()
        fig.add_scatter(x=g.index, y=g / g.iloc[0], name=k, line=dict(color=PAL[i % 6]))
    st.plotly_chart(sty(fig, 420), width="stretch")

# ---------------- similar ----------------
with tabs[3]:
    n = st.selectbox("Compare portfolio", list(res), key="sm")
    wu, pu = res[n]["w"], res[n]["pr"]
    rows = []
    for k in [*E.MODELS, *inv]:
        if k not in allp:
            continue
        sim, ov, co = E.similarity(wu, pu, allp[k][1], allp[k][0])
        cv = cand.get(k)
        rows.append({"Name": k, "Type": "13F" if cv else "Model", "Similarity": sim, "Holdings overlap": ov, "Return correlation": co,
                     "13F weight mapped": cv[1] if cv else np.nan, "As of": cv[2] if cv else "—"})
    if not rows:
        st.info("No candidates available.")
    else:
        df = pd.DataFrame(rows).sort_values("Similarity", ascending=False)
        st.dataframe(df.style.format({"Similarity": "{:.0%}", "Holdings overlap": "{:.0%}", "Return correlation": "{:.2f}", "13F weight mapped": "{:.0%}"}),
                     hide_index=True, width="stretch")
        top = df.head(5)
        fig = go.Figure(go.Bar(x=top.Similarity, y=top.Name, orientation="h", marker_color=ACC))
        fig.update_layout(title="Most similar", xaxis_tickformat=".0%", yaxis_autorange="reversed")
        st.plotly_chart(sty(fig, 300), width="stretch")
    if not cand:
        st.info("No 13F data loaded yet: upload a 13F zip in the sidebar to add investors. Models are shown meanwhile.")
    st.caption("Similarity = 50% holdings overlap + 25% return correlation + 25% volatility closeness (return-profile proxy for style: no sector data).")

# ---------------- data ----------------
with tabs[4]:
    st.markdown("""**Method.** Weekly returns for every asset (one convention for stocks and 24/7 crypto), annualised ×52. Score = weighted average of five 0-100 components:
diversification (effective holdings + weighted average correlation), Sharpe (1.5 = full marks), drawdown vs your risk tolerance, expense ratio (1% = zero), and volatility distance from the profile target.
Short horizons cap the effective risk tolerance.

**Caveats.**
- Everything is historical and in-sample; the score is a diagnostic, not a forecast.
- Expense ratios come from Yahoo and are often missing for mutual funds and non-US funds: unknowns are excluded from the cost average, not assumed zero.
- 13F filings cover US long equity only, up to 45 days stale, excluding bonds, cash, shorts and non-US holdings. Berkshire's 13F is the company, not Buffett personally.
- CUSIP→ticker mapping (OpenFIGI) is incomplete; the “13F weight mapped” column shows how much of each investor's reported portfolio was used.
- Models are ETF approximations of famous allocations, not what those investors actually hold.""")
    for n, r in res.items():
        unk = [t for t, m in r["M"].items() if m["er"] is None]
        st.caption(f"Portfolio {n}: expense ratio unknown for {', '.join(unk) or 'none'} ({1 - r['sc'][3]:.0%} of weight)")
