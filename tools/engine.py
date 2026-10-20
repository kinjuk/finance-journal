"""Optimization Lab engine: estimation, optimizers, frontier. No UI imports."""
import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import minimize, linprog

TD = 252
OBJECTIVES = {"sharpe": "Max Sharpe", "sortino": "Max Sortino", "minvol": "Min Volatility"}


def load_prices(tickers, start, end):
    p = yf.download(list(tickers), start=start, end=end, auto_adjust=True, progress=False)["Close"]
    if isinstance(p, pd.Series):
        p = p.to_frame(tickers[0])
    return p.sort_index().dropna(how="all").dropna(axis=1, how="all").ffill().dropna()


def estimate(p, method="arith"):
    """arith: annualised arithmetic mean (consistent with covariance, classic Markowitz).
    log: legacy compounded mean-log-return (reproduces the original script)."""
    r = p.pct_change().dropna()
    if method == "log":
        mu = np.exp(np.log(p / p.shift(1)).dropna().mean() * TD) - 1
    else:
        mu = r.mean() * TD
    return mu, r.cov() * TD, r


def feasible(n, lo, hi):
    return n * lo <= 1 + 1e-9 and n * hi >= 1 - 1e-9


def perf(w, mu, cov, r, rf):
    w = np.asarray(w)
    ret = float(w @ mu.values)
    vol = float(np.sqrt(w @ cov.values @ w))
    d = np.minimum(r.values @ w - rf / TD, 0.0)
    dd = float(np.sqrt((d ** 2).mean() * TD))  # annualised downside deviation vs rf
    return {"ret": ret, "vol": vol,
            "sharpe": (ret - rf) / vol if vol > 0 else 0.0,
            "sortino": (ret - rf) / dd if dd > 0 else 0.0}


def solve(obj, mu, cov, r, rf, lo, hi, seed=0):
    n = len(mu)
    f = {"sharpe": lambda w: -perf(w, mu, cov, r, rf)["sharpe"],
         "sortino": lambda w: -perf(w, mu, cov, r, rf)["sortino"],
         "minvol": lambda w: float(w @ cov.values @ w)}[obj]
    cons = [{"type": "eq", "fun": lambda w: w.sum() - 1}]
    rng = np.random.default_rng(seed)
    starts = [np.full(n, 1 / n)] + [lo + (1 - n * lo) * rng.dirichlet(np.ones(n)) for _ in range(4)]
    best = None
    for x0 in starts:
        o = minimize(f, np.clip(x0, lo, hi), method="SLSQP", bounds=[(lo, hi)] * n,
                     constraints=cons, options={"maxiter": 1000, "ftol": 1e-10})
        if o.success and (best is None or o.fun < best.fun):
            best = o
    if best is None:
        return {"obj": obj, "ok": False, "msg": o.message}
    w = pd.Series(best.x, index=mu.index)
    bound = {t: ("max" if abs(x - hi) < 1e-4 else "min") for t, x in w.items()
             if abs(x - hi) < 1e-4 or abs(x - lo) < 1e-4}
    return {"obj": obj, "ok": True, "msg": best.message, "w": w, "m": perf(w.values, mu, cov, r, rf),
            "bound": bound, "turnover": float(0.5 * np.abs(w.values - 1 / n).sum())}


def frontier(mu, cov, lo, hi, k=40):
    n = len(mu)
    top = -linprog(-mu.values, A_eq=np.ones((1, n)), b_eq=[1], bounds=[(lo, hi)] * n).fun
    bottom = float(mu.values @ solve_minvol_w(cov, lo, hi, n))
    pts = []
    for t in np.linspace(bottom, top, k):
        o = minimize(lambda w: w @ cov.values @ w, np.full(n, 1 / n), method="SLSQP",
                     bounds=[(lo, hi)] * n,
                     constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1},
                                  {"type": "eq", "fun": lambda w, t=t: w @ mu.values - t}])
        if o.success:
            pts.append((float(np.sqrt(o.fun)), float(t)))
    return pd.DataFrame(pts, columns=["vol", "ret"])


def solve_minvol_w(cov, lo, hi, n):
    o = minimize(lambda w: w @ cov.values @ w, np.full(n, 1 / n), method="SLSQP",
                 bounds=[(lo, hi)] * n, constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1}])
    return o.x


def cloud(mu, cov, lo, hi, N=4000, seed=1):
    n = len(mu)
    w = lo + (1 - n * lo) * np.random.default_rng(seed).dirichlet(np.ones(n), N)
    w = w[(w <= hi + 1e-9).all(1)]
    return pd.DataFrame({"ret": w @ mu.values, "vol": np.sqrt(np.einsum("ij,jk,ik->i", w, cov.values, w))})


def project(ret, vol, years, paths=1000, seed=2):
    """Model-based fan (lognormal), NOT a forecast."""
    rng = np.random.default_rng(seed)
    m = int(years * 12)
    step = rng.normal((ret - 0.5 * vol ** 2) / 12, vol / np.sqrt(12), (paths, m))
    v = np.exp(np.cumsum(step, axis=1))
    return np.percentile(v, [5, 25, 50, 75, 95], axis=0)
