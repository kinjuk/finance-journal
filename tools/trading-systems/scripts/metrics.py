#!/usr/bin/env python3
"""Performance and robustness metrics per Kaufman, Trading Systems and Methods (Ch. 21, 23).

Usage (CLI):  python metrics.py returns.csv [--col NAME] [--periods 252] [--rf 0.0] [--mar 0.0]
Input: CSV with one column of PERIODIC (daily) fractional returns, e.g. 0.004 = +0.4%.
Library:      from metrics import report, walk_forward, sensitivity_layers
"""
import sys, math, argparse
import numpy as np


def _equity(r):
    return np.cumprod(1.0 + np.asarray(r, float))


def drawdowns(r):
    eq = _equity(r)
    peak = np.maximum.accumulate(np.concatenate(([1.0], eq)))[1:]
    return (peak - eq) / peak          # D_i >= 0, zero on new highs


def report(r, periods=252, rf=0.0, mar=0.0):
    """rf, mar: annualized rates. Returns dict of Kaufman's risk/return measures."""
    r = np.asarray(r, float)
    n = len(r)
    eq = _equity(r)
    arr = eq[-1] ** (periods / n) - 1.0            # annualized rate of return
    vol = r.std(ddof=1) * math.sqrt(periods)       # annualized volatility
    dd = drawdowns(r)
    mdd = dd.max()
    below = dd[dd > 0]
    downside = below.std(ddof=1) if len(below) > 1 else float("nan")  # std of non-zero excursions
    out = {
        "ann_return": arr,
        "ann_vol": vol,
        "information_ratio": arr / vol if vol else float("nan"),       # no risk-free
        "sharpe": (arr - rf) / vol if vol else float("nan"),
        "max_drawdown": mdd,
        "calmar": arr / mdd if mdd else float("nan"),
        "sortino": (arr - mar) / downside if downside == downside and downside else float("nan"),
        "ulcer_index": math.sqrt(np.mean(dd ** 2)),
        "avg_max_retracement": dd.mean(),                              # Schwager AMR (daily approx.)
        "pct_time_in_drawdown": float((dd > 0).mean()),
        "worst_period": r.min(),
        "best_period": r.max(),
        "n": n,
    }
    # time to recovery: longest stretch below a prior high
    longest = cur = 0
    for d in dd:
        cur = cur + 1 if d > 0 else 0
        longest = max(longest, cur)
    out["longest_drawdown_periods"] = longest
    # share of total profit from the best 5% of periods (price-shock dependence check)
    pos = np.sort(r[r > 0])[::-1]
    k = max(1, int(0.05 * n))
    out["profit_share_top5pct_periods"] = pos[:k].sum() / pos.sum() if pos.size else float("nan")
    return out


def walk_forward(price_or_ret, fit_fn, apply_fn, in_len, out_len):
    """Generic step-forward harness (Kaufman Ch. 21).
    fit_fn(train) -> params ; apply_fn(test, params) -> array of out-of-sample returns.
    Returns (concatenated OOS returns, list of chosen params). Inspect params for instability."""
    oos, chosen, i = [], [], 0
    n = len(price_or_ret)
    while i + in_len + out_len <= n:
        train = price_or_ret[i:i + in_len]
        test = price_or_ret[i + in_len:i + in_len + out_len]
        p = fit_fn(train)
        chosen.append(p)
        oos.append(np.asarray(apply_fn(test, p), float))
        i += out_len
    return (np.concatenate(oos) if oos else np.array([])), chosen


def sensitivity_layers(param_grid, scores, core, layers=10):
    """n-space sensitivity (Ch. 21). param_grid: (m,k) array of tested parameter sets (normalize columns first);
    scores: (m,) performance; core: (k,) chosen values. Returns mean score per concentric radius layer."""
    P = np.asarray(param_grid, float); s = np.asarray(scores, float)
    r = np.sqrt(((P - np.asarray(core, float)) ** 2).sum(axis=1))
    order = np.argsort(r)
    return [float(s[idx].mean()) for idx in np.array_split(order, layers) if len(idx)]


def pct_step_values(start, stop, factor=1.5):
    """Percentage-step parameter ladder (Ch. 21): dense at small values, sparse at large."""
    v, x = [], float(start)
    while x <= stop:
        v.append(round(x)); x *= factor
    return sorted(set(v))


def risk_of_ruin(avg_win, avg_loss, p_win, investment, max_risk):
    """Kaufman Ch.23 (Vince/Griffin approximation). max_risk as fraction of investment (e.g. 0.25)."""
    pw, pl = p_win, 1.0 - p_win
    w, l = abs(avg_win) / investment, abs(avg_loss) / investment
    Z = pw * w - pl * l
    A = math.sqrt((pw * w) ** 2 + (pl * l) ** 2)
    P = 0.5 * (1 + Z / A)
    return min(1.0, ((1 - P) / P) ** (max_risk / A)) if P > 0 else 1.0


def vol_stabilize(returns, target_vol=0.12, window=10, periods=252, threshold=0.0):
    """Kaufman Ch.24: scale returns by LAGGED factor = target / rolling annualized vol.
    threshold: no resize unless factor changes by this fraction (reduces switching cost)."""
    r = np.asarray(returns, float)
    out = np.zeros_like(r); vf_prev = 1.0
    for i in range(len(r)):
        if i >= window:
            vol = r[i - window:i].std(ddof=1) * math.sqrt(periods)   # uses data up to i-1 (lagged)
            vf = target_vol / vol if vol > 0 else vf_prev
            if abs(vf / vf_prev - 1.0) >= threshold:
                vf_prev = vf
        out[i] = r[i] * vf_prev
    return out


def cap_positions(exposures, cap):
    """Scale ALL positions by cap/total_exposure if total exceeds the cap (apply last)."""
    e = np.asarray(exposures, float); tot = np.abs(e).sum()
    return e * (cap / tot) if tot > cap else e


def efficiency_ratio(prices, n=20):
    """Kaufman noise measure: |net change over n| / sum of |daily changes|. ~1 trend, ~0 noise."""
    p = np.asarray(prices, float)
    out = np.full(len(p), np.nan)
    d = np.abs(np.diff(p))
    for i in range(n, len(p)):
        path = d[i - n:i].sum()
        out[i] = abs(p[i] - p[i - n]) / path if path else np.nan
    return out


def price_density(high, low, n=10):
    """Sum of (H-L) over n days / (n-day highest high - lowest low)."""
    h, l = np.asarray(high, float), np.asarray(low, float)
    out = np.full(len(h), np.nan)
    for i in range(n - 1, len(h)):
        rng = h[i - n + 1:i + 1].max() - l[i - n + 1:i + 1].min()
        out[i] = (h[i - n + 1:i + 1] - l[i - n + 1:i + 1]).sum() / rng if rng else np.nan
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("csv"); ap.add_argument("--col", default=None)
    ap.add_argument("--periods", type=int, default=252)
    ap.add_argument("--rf", type=float, default=0.0); ap.add_argument("--mar", type=float, default=0.0)
    a = ap.parse_args()
    import csv
    rows = list(csv.DictReader(open(a.csv)))
    col = a.col or list(rows[0].keys())[-1]
    rets = [float(x[col]) for x in rows if x[col] != ""]
    for k, v in report(rets, a.periods, a.rf, a.mar).items():
        print(f"{k:32s} {v:.4f}" if isinstance(v, float) else f"{k:32s} {v}")
