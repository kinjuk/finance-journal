import datetime as dt
import json
import os

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

import engine as E

st.set_page_config("Optimization Lab", "📈", layout="wide")

# ---------------- sidebar ----------------
with st.sidebar:
    st.markdown("### Optimization Lab")
    dark = st.toggle("Dark mode", True)
    raw = st.text_input("Tickers (comma-separated)", "SPY, BND, GLD, QQQ, VTI")
    tickers = list(dict.fromkeys(t.strip().upper() for t in raw.split(",") if t.strip()))
    live = st.toggle("Live (end = today)", False)
    start = st.date_input("Start", dt.date(2015, 1, 1))
    end = dt.date.today() if live else st.date_input("End", dt.date(2025, 10, 23))
    primary = st.radio("Primary objective", list(E.OBJECTIVES), format_func=E.OBJECTIVES.get)
    lo = st.slider("Min weight %", 0, 30, 5) / 100
    hi = st.slider("Max weight %", 10, 100, 40) / 100
    rf = st.slider("Risk-free rate %", 0.0, 8.0, 4.0, 0.25) / 100
    method = st.radio("Return estimator", ["arith", "log"],
                      format_func=lambda m: "Arithmetic (consistent)" if m == "arith" else "Legacy log-mean (original script)")
    years = st.slider("Projection horizon (yrs)", 1, 30, 10)

C = dict(bg="#0b1220", card="#111a2e", fg="#e6edf7", mut="#8da2c0", line="#22304d") if dark else \
    dict(bg="#f4f6fa", card="#ffffff", fg="#0f1a2b", mut="#5b6b82", line="#dbe2ec")
PAL = ["#4f9dff", "#f5b942", "#3ddc97", "#ff6b6b", "#b48cff", "#2ec4d6", "#ff9f68", "#9aa5b1"]
st.markdown(f"""<style>
.stApp{{background:{C['bg']}}} [data-testid=stSidebar]{{background:{C['card']}}}
h1,h2,h3,h4,label,p,li,[data-testid=stMetricValue],[data-testid=stMetricLabel],[data-testid=stCaptionContainer]{{color:{C['fg']}!important}}
[data-testid=stMetric]{{background:{C['card']};border:1px solid {C['line']};border-radius:12px;padding:14px 16px}}
.block-container{{padding-top:2rem;max-width:1300px}}
</style>""", unsafe_allow_html=True)


def style(fig, h=380):
    fig.update_layout(template="plotly_dark" if dark else "plotly_white", height=h,
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      margin=dict(l=10, r=10, t=40, b=10), legend=dict(orientation="h", y=-0.15),
                      font=dict(color=C["fg"]))
    return fig


# ---------------- data ----------------
@st.cache_data(ttl=3600, show_spinner="Downloading prices…")
def get_prices(t, s, e):
    try:
        p = E.load_prices(t, s, e)
        if p.empty:
            raise ValueError("empty")
        return p, "yfinance"
    except Exception:
        if os.path.exists("data/prices_fallback.csv"):
            p = pd.read_csv("data/prices_fallback.csv", index_col=0, parse_dates=True)
            cols = [c for c in t if c in p.columns]
            return p.loc[s:e, cols].dropna(), "fallback CSV"
        raise


st.title("Optimization Lab")
if len(tickers) < 2:
    st.error("Need at least 2 tickers."); st.stop()
if not E.feasible(len(tickers), lo, hi):
    st.error(f"Infeasible: {len(tickers)} assets × min {lo:.0%} = {len(tickers)*lo:.0%}, "
             f"× max {hi:.0%} = {len(tickers)*hi:.0%}. Need min-sum ≤ 100% ≤ max-sum."); st.stop()
try:
    prices, source = get_prices(tuple(tickers), str(start), str(end))
except Exception as ex:
    st.error(f"Data download failed ({ex}). Check tickers or add data/prices_fallback.csv."); st.stop()
missing = [t for t in tickers if t not in prices.columns]
if missing:
    st.warning(f"No data for: {', '.join(missing)} (dropped).")
if prices.shape[1] < 2 or len(prices) < 250:
    st.error("Not enough overlapping history (need ≥2 assets, ≥250 days)."); st.stop()
if not E.feasible(prices.shape[1], lo, hi):
    st.error("Constraints infeasible after dropping tickers."); st.stop()

mu, cov, r = E.estimate(prices, method)
n = len(mu)
res = {o: E.solve(o, mu, cov, r, rf, lo, hi) for o in E.OBJECTIVES}
eq = np.full(n, 1 / n)
eqm = E.perf(eq, mu, cov, r, rf)
P = res[primary]
if not P["ok"]:
    st.error(f"Solver failed: {P['msg']}"); st.stop()
m = P["m"]

st.caption(f"{prices.index[0]:%Y-%m-%d} → {prices.index[-1]:%Y-%m-%d} · {len(prices)} days · "
           f"source: {source} · estimator: {method} · in-sample historical estimates, not forecasts")

# ---------------- KPIs ----------------
k = st.columns(4)
k[0].metric("Expected return", f"{m['ret']:.2%}", f"{(m['ret']-eqm['ret'])*100:+.2f} pp vs equal-wt")
k[1].metric("Volatility", f"{m['vol']:.2%}", f"{(m['vol']-eqm['vol'])*100:+.2f} pp vs equal-wt", delta_color="inverse")
k[2].metric("Sharpe", f"{m['sharpe']:.3f}", f"{m['sharpe']-eqm['sharpe']:+.3f}")
k[3].metric("Sortino", f"{m['sortino']:.3f}", f"{m['sortino']-eqm['sortino']:+.3f}")

if P["bound"]:
    pinned = ", ".join(f"{t} @ {s} ({P['w'][t]:.0%})" for t, s in P["bound"].items())
    st.warning(f"**Constraints are driving this result.** Pinned at bounds: {pinned}. "
               f"The optimizer wants more than you allow — see the sensitivity chart before trusting these weights.")

tabs = st.tabs(["Allocation", "Frontier", "Risk & Backtest", "Projection", "Diagnostics & Export"])

# ---------------- allocation ----------------
with tabs[0]:
    a, b = st.columns([1, 1.3])
    w = P["w"]
    fig = go.Figure(go.Pie(labels=w.index, values=w.values, hole=0.6, marker=dict(colors=PAL),
                           textinfo="label+percent", sort=False))
    fig.add_annotation(text=f"<b>{E.OBJECTIVES[primary]}</b>", showarrow=False, font=dict(size=14))
    a.plotly_chart(style(fig), width="stretch")
    fig = go.Figure()
    for i, o in enumerate(E.OBJECTIVES):
        if res[o]["ok"]:
            fig.add_bar(name=E.OBJECTIVES[o], x=list(res[o]["w"].index), y=res[o]["w"].values, marker_color=PAL[i])
    fig.add_hline(y=hi, line_dash="dot", line_color=C["mut"], annotation_text="max")
    fig.add_hline(y=lo, line_dash="dot", line_color=C["mut"], annotation_text="min")
    fig.update_layout(barmode="group", title="Weights by objective", yaxis_tickformat=".0%")
    b.plotly_chart(style(fig), width="stretch")

    rows = []
    for o, x in res.items():
        if x["ok"]:
            rows.append({"Objective": E.OBJECTIVES[o], "Return": x["m"]["ret"], "Vol": x["m"]["vol"],
                         "Sharpe": x["m"]["sharpe"], "Sortino": x["m"]["sortino"], "Turnover vs EW": x["turnover"],
                         "At bounds": ", ".join(x["bound"]) or "—"})
    rows.append({"Objective": "Equal weight", "Return": eqm["ret"], "Vol": eqm["vol"], "Sharpe": eqm["sharpe"],
                 "Sortino": eqm["sortino"], "Turnover vs EW": 0.0, "At bounds": "—"})
    st.dataframe(pd.DataFrame(rows).style.format({"Return": "{:.2%}", "Vol": "{:.2%}", "Sharpe": "{:.3f}",
                 "Sortino": "{:.3f}", "Turnover vs EW": "{:.1%}"}), hide_index=True, width="stretch")

    # sensitivity of Sharpe to the max-weight cap
    caps = [c for c in np.round(np.arange(max(1 / n, lo + 0.05), 1.01, 0.1), 2) if E.feasible(n, lo, c)]
    sens = []
    for c in caps:
        x = E.solve("sharpe", mu, cov, r, rf, lo, float(c))
        if x["ok"]:
            sens.append((c, x["m"]["sharpe"]))
    if sens:
        s = pd.DataFrame(sens, columns=["cap", "sharpe"])
        fig = go.Figure(go.Scatter(x=s.cap, y=s.sharpe, mode="lines+markers", line=dict(color=PAL[0])))
        fig.add_vline(x=hi, line_dash="dot", line_color=C["mut"], annotation_text="current cap")
        fig.update_layout(title="Sensitivity: max Sharpe vs max-weight cap", xaxis_tickformat=".0%")
        st.plotly_chart(style(fig, 300), width="stretch")

# ---------------- frontier ----------------
with tabs[1]:
    fr = E.frontier(mu, cov, lo, hi)
    cl = E.cloud(mu, cov, lo, hi)
    fig = go.Figure()
    fig.add_scatter(x=cl.vol, y=cl.ret, mode="markers", name="Random feasible portfolios",
                    marker=dict(size=3, color=C["mut"], opacity=0.35))
    fig.add_scatter(x=fr.vol, y=fr.ret, mode="lines", name="Efficient frontier", line=dict(color=PAL[0], width=3))
    for i, o in enumerate(E.OBJECTIVES):
        if res[o]["ok"]:
            fig.add_scatter(x=[res[o]["m"]["vol"]], y=[res[o]["m"]["ret"]], mode="markers", name=E.OBJECTIVES[o],
                            marker=dict(size=14, symbol="star", color=PAL[i + 1], line=dict(width=1, color=C["fg"])))
    fig.add_scatter(x=[eqm["vol"]], y=[eqm["ret"]], mode="markers", name="Equal weight",
                    marker=dict(size=11, symbol="diamond", color=PAL[3]))
    for t in mu.index:
        fig.add_scatter(x=[np.sqrt(cov.loc[t, t])], y=[mu[t]], mode="markers+text", text=[t], textposition="top center",
                        showlegend=False, marker=dict(size=7, color=C["fg"]))
    fig.update_layout(xaxis_title="Volatility", yaxis_title="Expected return", xaxis_tickformat=".0%",
                      yaxis_tickformat=".0%", title="Efficient frontier under your constraints")
    st.plotly_chart(style(fig, 520), width="stretch")

# ---------------- risk ----------------
with tabs[2]:
    a, b = st.columns([1, 1.6])
    corr = r.corr()
    fig = go.Figure(go.Heatmap(z=corr.values, x=corr.columns, y=corr.index, zmin=-1, zmax=1, colorscale="RdBu_r",
                               text=np.round(corr.values, 2), texttemplate="%{text}"))
    fig.update_layout(title="Correlation")
    a.plotly_chart(style(fig, 420), width="stretch")
    pr = pd.Series(r.values @ P["w"].values, index=r.index)
    er = pd.Series(r.values @ eq, index=r.index)
    g = pd.DataFrame({E.OBJECTIVES[primary]: (1 + pr).cumprod(), "Equal weight": (1 + er).cumprod()})
    dd = g / g.cummax() - 1
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3], vertical_spacing=0.04)
    for i, c in enumerate(g):
        fig.add_scatter(x=g.index, y=g[c], name=c, line=dict(color=PAL[i * 3]), row=1, col=1)
        fig.add_scatter(x=dd.index, y=dd[c], name=c, showlegend=False, line=dict(color=PAL[i * 3], width=1), row=2, col=1)
    fig.update_yaxes(tickformat=".0%", row=2, col=1)
    fig.update_layout(title="Growth of 1 & drawdown (constant weights, in-sample)")
    b.plotly_chart(style(fig, 420), width="stretch")
    st.caption(f"Max drawdown — optimized: {dd.iloc[:, 0].min():.1%} · equal weight: {dd.iloc[:, 1].min():.1%}. "
               "This backtest uses weights fitted on the same data: it is optimistic by construction.")

# ---------------- projection ----------------
with tabs[3]:
    q = E.project(m["ret"], m["vol"], years)
    x = np.arange(1, q.shape[1] + 1) / 12
    fig = go.Figure()
    fig.add_scatter(x=x, y=q[0], line=dict(width=0), showlegend=False)
    fig.add_scatter(x=x, y=q[4], fill="tonexty", line=dict(width=0), name="5–95%", fillcolor="rgba(79,157,255,.15)")
    fig.add_scatter(x=x, y=q[1], line=dict(width=0), showlegend=False)
    fig.add_scatter(x=x, y=q[3], fill="tonexty", line=dict(width=0), name="25–75%", fillcolor="rgba(79,157,255,.3)")
    fig.add_scatter(x=x, y=q[2], name="Median", line=dict(color=PAL[0], width=3))
    fig.update_layout(title=f"Simulated growth of 1 over {years}y (lognormal, uses the point estimates above)",
                      xaxis_title="Years")
    st.plotly_chart(style(fig, 460), width="stretch")
    st.caption("Illustrative only. Garbage-in: the return estimate is a noisy historical mean; the fan width understates real uncertainty.")

# ---------------- diagnostics ----------------
with tabs[4]:
    st.subheader("Solver")
    st.dataframe(pd.DataFrame([{"Objective": E.OBJECTIVES[o], "Converged": x["ok"], "Message": x["msg"]}
                               for o, x in res.items()]), hide_index=True, width="stretch")
    st.subheader("Inputs")
    a, b = st.columns(2)
    a.dataframe(pd.DataFrame({"Ann. return": mu, "Ann. vol": np.sqrt(np.diag(cov))}).style.format("{:.2%}"))
    b.dataframe(cov.style.format("{:.4f}"))
    st.markdown(f"""**Assumptions:** returns/covariance estimated from {len(r)} daily observations, annualised ×{E.TD}. 
Estimator `{method}`: {"arithmetic mean, consistent with the covariance" if method=="arith" else "compounded mean log return (inconsistent with arithmetic covariance — kept to reproduce the original script)"}. 
Sortino uses downside deviation below the risk-free rate on daily portfolio returns. No transaction costs, taxes or out-of-sample validation.""")
    out = {"objective": primary, "status": "completed", "period": [str(prices.index[0].date()), str(prices.index[-1].date())],
           "metrics": {"expected_annual_return": m["ret"], "annual_volatility": m["vol"], "sharpe_ratio": m["sharpe"],
                       "sortino_ratio": m["sortino"]},
           "weights": P["w"].round(6).to_dict(), "constraints": {"min_weight": lo, "max_weight": hi, "risk_free": rf},
           "at_bounds": P["bound"], "estimator": method}
    c = st.columns(3)
    c[0].download_button("Result JSON", json.dumps(out, indent=2), "aletheia_result.json")
    c[1].download_button("Weights CSV", P["w"].to_csv(), "weights.csv")
    c[2].download_button("Prices CSV", prices.to_csv(), "prices.csv")
