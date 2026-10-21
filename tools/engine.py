"""Efficiency Lab engine. No UI imports."""
import time
import zipfile

import numpy as np
import pandas as pd
import requests
import yfinance as yf
from scipy.optimize import minimize

PER = 52  # weekly returns everywhere: one convention for stocks (252d) and crypto (365d)
COMPONENTS = ["Diversification", "Risk-adjusted return", "Drawdown", "Costs", "Goal fit"]
TARGET_VOL = {"Low": .08, "Medium": .14, "High": .22}
MDD_LIMIT = {"Low": .15, "Medium": .30, "High": .50}
GOAL_MULT = {"Growth": 1.0, "Balanced": .9, "Income": .8, "Preservation": .6}

BENCH = {"SPY (US equity)": {"SPY": 1}, "60/40 (SPY/AGG)": {"SPY": .6, "AGG": .4}, "VT (global equity)": {"VT": 1}}
MODELS = {  # ETF approximations of well-known allocations, not the investors' actual holdings
    "Buffett 90/10 (approx.)": {"SPY": .9, "SHV": .1},
    "Dalio All Weather (approx.)": {"VTI": .3, "TLT": .4, "IEF": .15, "GLD": .075, "DBC": .075},
    "Swensen Yale model (approx.)": {"VTI": .3, "VEA": .15, "VWO": .05, "VNQ": .2, "IEF": .15, "TIP": .15},
    "Bogleheads 3-fund": {"VTI": .5, "VXUS": .3, "BND": .2},
    "Permanent Portfolio": {"VTI": .25, "TLT": .25, "GLD": .25, "SHV": .25}}
INVESTORS = {  # display name -> text matched inside the 13F filer name (edit freely)
    "Warren Buffett (Berkshire)": "BERKSHIRE HATHAWAY INC", "Michael Burry (Scion)": "SCION ASSET MANAGEMENT",
    "Bill Ackman (Pershing Square)": "PERSHING SQUARE CAPITAL", "Ray Dalio (Bridgewater)": "BRIDGEWATER ASSOCIATES",
    "Stan Druckenmiller (Duquesne)": "DUQUESNE FAMILY OFFICE", "Seth Klarman (Baupost)": "BAUPOST GROUP",
    "George Soros (Soros Fund)": "SOROS FUND MANAGEMENT", "Dan Loeb (Third Point)": "THIRD POINT LLC",
    "Chase Coleman (Tiger Global)": "TIGER GLOBAL MANAGEMENT", "David Tepper (Appaloosa)": "APPALOOSA"}


# ---------- market data ----------
def weekly(tickers, start):
    p = yf.download(list(tickers), start=start, auto_adjust=True, progress=False)["Close"]
    if isinstance(p, pd.Series):
        p = p.to_frame(list(tickers)[0])
    p.index = pd.to_datetime(p.index).tz_localize(None)
    return p.resample("W-FRI").last()


def rets(p):
    return p.pct_change(fill_method=None)


def info(t):
    try:
        i = yf.Ticker(t).info
    except Exception:
        i = {}
    q, er = i.get("quoteType", ""), i.get("annualReportExpenseRatio")
    if er is None and i.get("netExpenseRatio") is not None:
        er = i["netExpenseRatio"] / 100
    if er is None and q in ("EQUITY", "CRYPTOCURRENCY"):
        er = 0.0
    return {"type": q, "er": er}


# ---------- portfolio maths ----------
def port(w, R, min_weeks=52):
    """Weekly portfolio return series; drops tickers lacking history and renormalises."""
    cols = [c for c in w.index if c in R.columns and R[c].notna().sum() >= min_weeks]
    if not cols:
        return pd.Series(dtype=float), pd.Series(dtype=float), pd.DataFrame()
    w2 = w[cols] / w[cols].sum()
    sub = R[cols].dropna()
    return sub @ w2, w2, sub


def summ(pr, rf):
    m, v = pr.mean() * PER, pr.std(ddof=1) * np.sqrt(PER)
    cum = (1 + pr).cumprod()
    return {"cagr": cum.iloc[-1] ** (PER / len(pr)) - 1, "vol": v,
            "sharpe": (m - rf) / v if v > 0 else 0.0, "mdd": (cum / cum.cummax() - 1).min()}


def effective(risk, goal, horizon):
    lv = ["Low", "Medium", "High"]
    cap = 0 if horizon < 3 else 1 if horizon < 7 else 2
    eff = lv[min(lv.index(risk), cap)]
    return eff, TARGET_VOL[eff] * GOAL_MULT[goal]


def score(w, sub, pr, meta, rf, eff, tv, wts):
    s = summ(pr, rf)
    h = float(np.sum(w.values ** 2))
    C = sub.corr().values
    avgc = (w.values @ C @ w.values - h) / (1 - h) if len(w) > 1 and h < 1 else 1.0
    known = [(x, meta[t]["er"]) for t, x in w.items() if meta[t]["er"] is not None]
    kw = sum(x for x, _ in known)
    er = sum(x * e for x, e in known) / kw if kw else 0.0
    comp = {"Diversification": 100 * (.6 * min(1, (1 / h - 1) / 7) + .4 * (1 - np.clip(avgc, 0, 1))),
            "Risk-adjusted return": 100 * np.clip(s["sharpe"] / 1.5, 0, 1),
            "Drawdown": 100 * np.clip(1 - abs(s["mdd"]) / MDD_LIMIT[eff], 0, 1),
            "Costs": 100 * np.clip(1 - er / .01, 0, 1),
            "Goal fit": 100 * max(0.0, 1 - abs(s["vol"] - tv) / tv)}
    tot = sum(wts[k] * comp[k] for k in COMPONENTS) / sum(wts.values())
    return tot, comp, s, kw, er


def rules(w, sub, meta, s, tv):
    out = []
    for t, x in w.items():
        ty, er = meta[t]["type"], meta[t]["er"]
        if ty in ("EQUITY", "CRYPTOCURRENCY") and x > .10:
            out.append(f"**{t}** is {x:.0%} in a single {'coin' if ty == 'CRYPTOCURRENCY' else 'stock'}: concentration risk above 10%.")
        elif x > .40:
            out.append(f"**{t}** is {x:.0%} of the portfolio: one holding dominates.")
        if er and er > .005:
            out.append(f"**{t}** charges {er:.2%}/yr: look for a cheaper equivalent.")
    C = sub.corr()
    for i, a in enumerate(C.columns):
        for b in C.columns[i + 1:]:
            if C.loc[a, b] > .9:
                out.append(f"**{a}** and **{b}** are {C.loc[a, b]:.2f} correlated: you are paying twice for the same exposure.")
    if s["vol"] > tv * 1.3:
        out.append(f"Volatility {s['vol']:.1%} is well above the {tv:.1%} suited to your profile.")
    elif s["vol"] < tv * .6:
        out.append(f"Volatility {s['vol']:.1%} is well below the {tv:.1%} suited to your profile: you may be under-using risk budget.")
    return out


def tilt(w, sub, rf, step=.10):
    """Max-Sharpe within +/- step of current weights. In-sample: a what-if, not advice."""
    w0, mu, cov = w.values, sub.mean().values * PER, sub.cov().values * PER
    f = lambda x: -((x @ mu - rf) / np.sqrt(x @ cov @ x))
    o = minimize(f, w0, method="SLSQP", bounds=[(max(0, a - step), min(1, a + step)) for a in w0],
                 constraints=[{"type": "eq", "fun": lambda x: x.sum() - 1}])
    if not o.success:
        return None
    d = pd.Series(o.x - w0, index=w.index)
    return d[d.abs() >= .01].sort_values(), -f(w0), -o.fun


def similarity(wu, pru, wc, prc):
    ov = float(sum(min(wu.get(t, 0), wc.get(t, 0)) for t in set(wu.index) | set(wc.index)))
    j = pd.concat([pru, prc], axis=1, join="inner").dropna()
    if len(j) < 26:
        return .5 * ov, ov, np.nan
    corr = j.iloc[:, 0].corr(j.iloc[:, 1])
    vu, vc = j.iloc[:, 0].std(), j.iloc[:, 1].std()
    return .5 * ov + .25 * max(corr, 0) + .25 * (1 - abs(vu - vc) / max(vu, vc)), ov, corr


# ---------- 13F ----------
def ingest_13f(files, top=40):
    """SEC Form 13F data-set zip(s) -> latest holdings (top N by value) for tracked investors."""
    best = {}
    for f in files:
        z = zipfile.ZipFile(f)
        nm = {n.split("/")[-1].upper(): n for n in z.namelist()}
        rd = lambda k, **kw: pd.read_csv(z.open(nm[k]), sep="\t", dtype=str, **kw)
        m = rd("COVERPAGE.TSV", usecols=["ACCESSION_NUMBER", "FILINGMANAGER_NAME"]).merge(
            rd("SUBMISSION.TSV", usecols=["ACCESSION_NUMBER", "SUBMISSIONTYPE", "PERIODOFREPORT"]))
        m = m[m.SUBMISSIONTYPE == "13F-HR"]
        acc = {}
        for inv, pat in INVESTORS.items():
            h = m[m.FILINGMANAGER_NAME.str.upper().str.contains(pat, regex=False, na=False)]
            if len(h):
                r = h.assign(p=pd.to_datetime(h.PERIODOFREPORT, errors="coerce")).sort_values("p").iloc[-1]
                acc[inv] = (r.ACCESSION_NUMBER, r.p)
        if not acc:
            continue
        ids = {a for a, _ in acc.values()}
        parts = []
        for ch in pd.read_csv(z.open(nm["INFOTABLE.TSV"]), sep="\t", dtype=str, chunksize=500_000,
                              usecols=["ACCESSION_NUMBER", "NAMEOFISSUER", "CUSIP", "VALUE", "PUTCALL"]):
            ch = ch[ch.ACCESSION_NUMBER.isin(ids) & ch.PUTCALL.isna()]
            if len(ch):
                parts.append(ch)
        if not parts:
            continue
        t = pd.concat(parts)
        t["VALUE"] = pd.to_numeric(t.VALUE, errors="coerce")  # units cancel: weights are within-filing
        for inv, (a, p) in acc.items():
            g = t[t.ACCESSION_NUMBER == a].groupby(["CUSIP", "NAMEOFISSUER"], as_index=False).VALUE.sum()
            if g.empty or (inv in best and p <= best[inv][0]):
                continue
            g["weight"] = g.VALUE / g.VALUE.sum()
            best[inv] = (p, g.nlargest(top, "weight").assign(investor=inv, period=p.date()))
    if not best:
        return pd.DataFrame()
    return pd.concat([b for _, b in best.values()]).rename(columns={"CUSIP": "cusip", "NAMEOFISSUER": "issuer"})[
        ["investor", "period", "cusip", "issuer", "weight"]]


def map_cusips(cusips, known):
    """CUSIP -> Yahoo ticker via OpenFIGI (free tier: 10 per request, ~25 requests/min). Resumable."""
    todo = [c for c in dict.fromkeys(cusips) if c not in known]
    for i in range(0, len(todo), 10):
        chunk = todo[i:i + 10]
        try:
            r = requests.post("https://api.openfigi.com/v3/mapping", timeout=20,
                              json=[{"idType": "ID_CUSIP", "idValue": c, "exchCode": "US"} for c in chunk])
            if r.status_code != 200:
                break
            for c, x in zip(chunk, r.json()):
                known[c] = ((x.get("data") or [{}])[0].get("ticker") or "").replace("/", "-")
        except Exception:
            break
        time.sleep(2.6)
    return known


def candidates(h, cmap):
    out = {}
    for inv, g in h.groupby("investor"):
        g = g.assign(t=g.cusip.map(cmap))
        g = g[g.t.notna() & (g.t != "")]
        if g.empty:
            continue
        w = g.groupby("t").weight.sum()
        out[inv] = (w / w.sum(), float(w.sum()), str(g.period.iloc[0]))
    return out
