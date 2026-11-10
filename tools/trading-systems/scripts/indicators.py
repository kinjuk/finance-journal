#!/usr/bin/env python3
"""Kaufman indicators (Ch. 1, 4-8). numpy only. All series are numpy arrays; leading values are NaN."""
import numpy as np


def sma(p, n):
    p = np.asarray(p, float); out = np.full(len(p), np.nan)
    c = np.cumsum(np.insert(p, 0, 0.0))
    out[n - 1:] = (c[n:] - c[:-n]) / n
    return out


def ema(p, a=None, n=None):
    """Exponential smoothing E_t = E_(t-1) + a (p_t - E_(t-1)); a = 2/(n+1) if n given (Hutson)."""
    if a is None: a = 2.0 / (n + 1)
    p = np.asarray(p, float); e = np.empty(len(p)); e[0] = p[0]
    for i in range(1, len(p)): e[i] = e[i - 1] + a * (p[i] - e[i - 1])
    return e


def geometric_ma(p, n):
    return np.exp(sma(np.log(np.asarray(p, float)), n))


def reg_stats(p, n):
    """Rolling linear regression of price on 1..n: returns (slope, forecast_next, resid_std, R)."""
    p = np.asarray(p, float); N = len(p)
    sl = np.full(N, np.nan); fc = sl.copy(); rs = sl.copy(); R = sl.copy()
    x = np.arange(1, n + 1, dtype=float)
    for t in range(n - 1, N):
        y = p[t - n + 1:t + 1]
        b, a = np.polyfit(x, y, 1)
        res = y - (a + b * x)
        sl[t] = b; fc[t] = a + b * (n + 1); rs[t] = res.std(ddof=2)
        R[t] = np.corrcoef(x, y)[0, 1] if y.std() > 0 else 0.0
    return sl, fc, rs, R


def regression_band_signal(close, n=20, k=2.0):
    """Buy when C(t+1) > F(t+1)+k*R, sell when < F-k*R. Returns position array (+1/-1/0, held)."""
    c = np.asarray(close, float); sl, fc, rs, R = reg_stats(c, n)
    pos = np.zeros(len(c)); cur = 0
    for t in range(n, len(c)):
        up, lo = fc[t - 1] + k * rs[t - 1], fc[t - 1] - k * rs[t - 1]   # forecast made yesterday for today
        if c[t] > up: cur = 1
        elif c[t] < lo: cur = -1
        pos[t] = cur
    return pos


def slope_signal(close, n=40):
    """Long when regression slope > 0, short when < 0."""
    sl = reg_stats(close, n)[0]
    return np.where(np.isnan(sl), 0.0, np.sign(sl))


def ma_direction_signal(close, n=40, kind="sma"):
    m = sma(close, n) if kind == "sma" else ema(close, n=n)
    pos = np.zeros(len(m)); pos[1:] = np.sign(np.diff(m)); pos[np.isnan(pos)] = 0
    return pos


def breakout_signal(high, low, close=None, n=20, confirm_close=False):
    """N-day breakout, always in market. Reverses when the opposite N-day extreme breaks."""
    h, l = np.asarray(high, float), np.asarray(low, float)
    c = np.asarray(close if close is not None else high, float)
    pos = np.zeros(len(h)); cur = 0
    for t in range(n, len(h)):
        hh, ll = h[t - n:t].max(), l[t - n:t].min()
        px_up = c[t] if confirm_close else h[t]; px_dn = c[t] if confirm_close else l[t]
        if px_up > hh: cur = 1
        elif px_dn < ll: cur = -1
        pos[t] = cur
    return pos


def swing_chart(high, low, filt):
    """Swing filter (Kaufman Ch.5). Returns list of (index, price, 'H'|'L') swing points."""
    h, l = np.asarray(high, float), np.asarray(low, float)
    pts = []; up = True; sh, shi, sl_, sli = h[0], 0, l[0], 0
    for t in range(1, len(h)):
        if up:
            if h[t] > sh: sh, shi = h[t], t
            elif sh - l[t] >= filt:
                pts.append((shi, sh, 'H')); up = False; sl_, sli = l[t], t
        else:
            if l[t] < sl_: sl_, sli = l[t], t
            elif h[t] - sl_ >= filt:
                pts.append((sli, sl_, 'L')); up = True; sh, shi = h[t], t
    return pts


def pivot_points(high, low, k=2):
    """Highest high / lowest low with k bars each side. Returns (high_idx, low_idx); confirmed k bars late."""
    h, l = np.asarray(high, float), np.asarray(low, float)
    hi = [i for i in range(k, len(h) - k) if h[i] == h[i - k:i + k + 1].max() and h[i] > h[i - 1:i].max()]
    lo = [i for i in range(k, len(l) - k) if l[i] == l[i - k:i + k + 1].min() and l[i] < l[i - 1:i].min()]
    return hi, lo


def cci(high, low, close, n=20):
    tp = (np.asarray(high, float) + np.asarray(low, float) + np.asarray(close, float)) / 3.0
    m = sma(tp, n); out = np.full(len(tp), np.nan)
    for t in range(n - 1, len(tp)):
        md = np.abs(tp[t - n + 1:t + 1] - m[t]).mean()
        out[t] = (tp[t] - m[t]) / (0.015 * md) if md else 0.0
    return out


def moving_channel(high, low, close, n=20, f=1.0):
    """Kaufman moving channel: M = mean typical price, R = mean(H-L); bands project M's slope."""
    h, l, c = (np.asarray(x, float) for x in (high, low, close))
    M = sma((h + l + c) / 3.0, n); R = sma(h - l, n)
    U = M + np.insert(np.diff(M), 0, np.nan) + f * R
    L = M + np.insert(np.diff(M), 0, np.nan) - f * R
    return M, U, L


def forecast_oscillator(close, n=5, smooth=3):
    c = np.asarray(close, float); sl, fc, rs, R = reg_stats(c, n)
    # fitted value at t (end of window): forecast_next - slope
    fitted = fc - sl
    pct = 100.0 * (c - fitted) / c
    return pct, sma(np.nan_to_num(pct), smooth)


def index_series(prices, base=100.0):
    p = np.asarray(prices, float); return base * p / p[0]


def momentum(p, n):
    p = np.asarray(p, float); out = np.full(len(p), np.nan); out[n:] = p[n:] - p[:-n]; return out


def rsi(p, n=14, lag=1):
    """Wilder RSI with Kaufman's average-off update; lag=2 gives the 2-day-change RSI variant."""
    p = np.asarray(p, float); out = np.full(len(p), np.nan)
    d = np.full(len(p), np.nan); d[lag:] = p[lag:] - p[:-lag]
    up, dn = np.maximum(d, 0), np.maximum(-d, 0)
    if len(p) <= n + lag: return out
    au, ad = np.nansum(up[lag:lag + n]) , np.nansum(dn[lag:lag + n])
    for t in range(lag + n - 1, len(p)):
        if t > lag + n - 1:
            au = au - au / n + up[t]; ad = ad - ad / n + dn[t]
        out[t] = 100.0 - 100.0 / (1.0 + au / ad) if ad > 0 else 100.0
    return out


def cmo(p, n=14):
    p = np.asarray(p, float); d = np.diff(p, prepend=p[0]); out = np.full(len(p), np.nan)
    for t in range(n, len(p)):
        su = np.maximum(d[t - n + 1:t + 1], 0).sum(); sd = np.maximum(-d[t - n + 1:t + 1], 0).sum()
        out[t] = 100.0 * (su - sd) / (su + sd) if su + sd else 0.0
    return out


def macd(p, fast=12, slow=26, signal=9):
    m = ema(p, n=fast) - ema(p, n=slow); s = ema(m, n=signal); return m, s, m - s


def stochastic(high, low, close, n=10, d=3):
    h, l, c = (np.asarray(x, float) for x in (high, low, close))
    k = np.full(len(c), np.nan)
    for t in range(n - 1, len(c)):
        hh, ll = h[t - n + 1:t + 1].max(), l[t - n + 1:t + 1].min()
        k[t] = 100.0 * (c[t] - ll) / (hh - ll) if hh > ll else 50.0
    dd = sma(np.nan_to_num(k, nan=50.0), d); dslow = sma(np.nan_to_num(dd, nan=50.0), d)
    return k, dd, dslow


def tsi(close, r=25, s=13):
    c = np.asarray(close, float); d = np.diff(c, prepend=c[0])
    num = ema(ema(d, n=r), n=s); den = ema(ema(np.abs(d), n=r), n=s)
    return 100.0 * num / np.where(den == 0, np.nan, den)


def seasonal_table(dates_month, prices, indexed=True):
    """Kaufman Ch.10. dates_month: array of (year, month) per row (month-end prices); prices: array.
    Returns dict month -> {'avg','median','pct_up','vol','n'} of monthly % (or $) changes."""
    p = np.asarray(prices, float)
    chg = (p[1:] / p[:-1] - 1.0) if indexed else np.diff(p)
    months = np.array([m for (_, m) in dates_month])[1:]
    out = {}
    for m in range(1, 13):
        x = chg[months == m]
        if len(x):
            out[m] = {"avg": float(x.mean()), "median": float(np.median(x)), "pct_up": float((x > 0).mean()),
                      "vol": float(x.std(ddof=1)) if len(x) > 1 else float("nan"), "n": int(len(x))}
    return out


def triangular_ma(p, P):
    """Kaufman triangular average: center weight 2.0, weights step 2/(P/2); even P drops oldest value."""
    p = np.asarray(p, float)
    P = P if P % 2 == 1 else P - 1 + 0  # keep odd length window (drop oldest when even)
    half = (P + 1) // 2
    step = 2.0 / half
    w = np.array([step * (i + 1) if i < half else step * (P - i) for i in range(P)])
    out = np.full(len(p), np.nan)
    for t in range(P - 1, len(p)):
        out[t] = (w * p[t - P + 1:t + 1]).sum() / w.sum()
    return out


def cycle_oscillator(p, cycle_len):
    """Detrended cycle proxy: price minus its simple MA of length cycle_len (Ch.11)."""
    p = np.asarray(p, float); return p - sma(p, cycle_len)


def obv(close, volume):
    c = np.asarray(close, float); v = np.asarray(volume, float)
    s = np.sign(np.diff(c, prepend=c[0])); return np.cumsum(s * v)


def filtered_obv(close, volume, n=50, vol_k=1.0, price_k=0.0):
    """OBV ignoring days with volume < mean - vol_k*std, and |dP| < price_k * std(dP) (Kaufman Ch.12)."""
    c = np.asarray(close, float); v = np.asarray(volume, float)
    dp = np.diff(c, prepend=c[0]); out = np.zeros(len(c))
    for t in range(1, len(c)):
        lo = t - n if t >= n else 0
        vt = v[lo:t + 1].mean() - vol_k * v[lo:t + 1].std() if t - lo > 2 else -np.inf
        pt = price_k * dp[lo:t + 1].std() if t - lo > 2 else 0.0
        out[t] = out[t - 1] if (v[t] < vt or abs(dp[t]) < pt) else out[t - 1] + np.sign(dp[t]) * v[t]
    return out


def force_index(close, volume, smooth_n=13):
    c = np.asarray(close, float); fi = np.diff(c, prepend=c[0]) * np.asarray(volume, float)
    return ema(fi, n=smooth_n)


def volume_oscillator(volume, short=14, long=34, ratio=True):
    v = np.asarray(volume, float); s, l = sma(v, short) * short, sma(v, long) * long
    return s / l if ratio else sma(v, short) - sma(v, long)


def volume_spike(volume, n=60, T=2.0, lag=5):
    """True where V_t > T * mean(V over n days ending lag days ago)."""
    v = np.asarray(volume, float); out = np.zeros(len(v), bool)
    for t in range(n + lag, len(v)):
        out[t] = v[t] > T * v[t - n - lag + 1:t - lag + 1].mean()
    return out


def market_facilitation(high, low, volume):
    return (np.asarray(high, float) - np.asarray(low, float)) / np.asarray(volume, float)


def ad_index(advances, declines):
    return np.cumsum(np.asarray(advances, float) - np.asarray(declines, float))


def stress_indicator(close1, close2, n=14, hi=95, lo=5):
    """Kaufman Ch.13 pairs 'stress': stochastic of the difference of two raw stochastics.
    Returns (stress, signal) signal +1 = long leg1/short leg2 (stress<lo), -1 = short leg1/long leg2 (stress>hi)."""
    def raw_stoch(c):
        c = np.asarray(c, float); out = np.full(len(c), np.nan)
        for t in range(n, len(c)):
            w = c[t - n:t]; r = w.max() - w.min()
            out[t] = (c[t] - w.min()) / r if r > 0 else 0.5
        return out
    D = raw_stoch(close1) - raw_stoch(close2)
    st = np.full(len(D), np.nan)
    for t in range(2 * n, len(D)):
        w = D[t - n:t]; r = np.nanmax(w) - np.nanmin(w)
        st[t] = 100.0 * (D[t] - np.nanmin(w)) / r if r > 0 else 50.0
    sig = np.where(st > hi, -1, np.where(st < lo, 1, 0)); return st, sig


def atr_pair_sizes(high1, low1, close1, high2, low2, close2, invest=1000.0, n=20):
    """Equal-risk shares per leg: invest / ATR$ (simple average true range)."""
    def atr(h, l, c):
        h, l, c = (np.asarray(x, float) for x in (h, l, c))
        tr = np.maximum(h[1:] - l[1:], np.maximum(abs(h[1:] - c[:-1]), abs(l[1:] - c[:-1])))
        return tr[-n:].mean()
    return invest / atr(high1, low1, close1), invest / atr(high2, low2, close2)


def spread_risk_ratio(a, b):
    """stdev of daily changes of the spread (A-B) divided by the average stdev of the legs. <1 = real risk reduction."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    da, db, ds = np.diff(a), np.diff(b), np.diff(a - b)
    return ds.std(ddof=1) / ((da.std(ddof=1) + db.std(ddof=1)) / 2.0)


def volatility_ratio(high, low, close, n=60, m=30):
    """Kaufman Ch.14: true range_t / ATR of the n days ending m days ago. > 3 = news shock."""
    h, l, c = (np.asarray(x, float) for x in (high, low, close))
    tr = np.empty(len(c)); tr[0] = h[0] - l[0]
    tr[1:] = np.maximum(h[1:] - l[1:], np.maximum(abs(h[1:] - c[:-1]), abs(l[1:] - c[:-1])))
    out = np.full(len(c), np.nan)
    for t in range(n + m, len(c)):
        a = tr[t - m - n + 1:t - m + 1].mean(); out[t] = tr[t] / a if a else np.nan
    return out


def cot_index(net_long, n=156):
    """COT Index (Briese): stochastic of a group's net long position. n in reports (156 weekly ~ 3 years)."""
    x = np.asarray(net_long, float); out = np.full(len(x), np.nan)
    for t in range(n - 1, len(x)):
        w = x[t - n + 1:t + 1]; r = w.max() - w.min()
        out[t] = 100.0 * (x[t] - w.min()) / r if r > 0 else 50.0
    return out


def pivot_levels(h, l, c):
    p = (h + l + c) / 3.0; r1, s1 = 2 * p - l, 2 * p - h
    return {"P": p, "R1": r1, "S1": s1, "R2": (p - s1) + r1, "S2": p - (r1 - s1)}


def demark_projection(o, h, l, c):
    """Kaufman/DeMark next-day projected (high, low); o = today's open."""
    if c < o: x = (h + c + 2 * l) / 2.0
    elif c > o: x = (2 * h + l + c) / 2.0
    else: x = (h + l + 2 * c) / 2.0
    return x - l, x - h


def weekday_pattern_counts(dates_weekday, closes):
    """Count XO codes by week: Monday=X; later days X if same direction as Fri->Mon move else O.
    dates_weekday: array of 0-4 (Mon-Fri); closes: array. Returns dict pattern -> count (complete Mon-Fri weeks only)."""
    wd = np.asarray(dates_weekday); c = np.asarray(closes, float); out = {}
    i = 1
    while i + 4 < len(c):
        if wd[i] == 0 and all(wd[i + k] == k for k in range(5)):
            mon = np.sign(c[i] - c[i - 1]); code = "X"
            for k in range(1, 5):
                code += "X" if np.sign(c[i + k] - c[i + k - 1]) == mon else "O"
            out[code] = out.get(code, 0) + 1; i += 5
        else: i += 1
    return out


def opening_range_breakout(open_, high, low, close, k, inside_filter=False):
    """Daily-bar proxy for Crabel ORB: long if high >= open+k, short if low <= open-k (reverse; exit at close).
    Returns per-day return in price units. If both hit, assumes the first-listed direction (long) -- use intraday data for truth."""
    o, h, l, c = (np.asarray(x, float) for x in (open_, high, low, close))
    pnl = np.zeros(len(c))
    for t in range(1, len(c)):
        if inside_filter and not (h[t - 1] <= h[max(t - 2, 0)] and l[t - 1] >= l[max(t - 2, 0)]): continue
        up, dn = h[t] >= o[t] + k, l[t] <= o[t] - k
        if up and not dn: pnl[t] = c[t] - (o[t] + k)
        elif dn and not up: pnl[t] = (o[t] - k) - c[t]
        elif up and dn: pnl[t] = c[t] - (o[t] + k)   # ambiguous: daily bars cannot resolve order
    return pnl


def intraday_shock_signals(high, low, close, factor=3.0, n=100, edge=0.2):
    """Bar-level shock fade: True-range > factor*avg and close in top/bottom edge of range -> -1 (fade up) / +1 (fade down)."""
    h, l, c = (np.asarray(x, float) for x in (high, low, close))
    tr = np.empty(len(c)); tr[0] = h[0] - l[0]
    tr[1:] = np.maximum(h[1:] - l[1:], np.maximum(abs(h[1:] - c[:-1]), abs(l[1:] - c[:-1])))
    avg = np.full(len(c), np.nan)
    for t in range(n, len(c)): avg[t] = tr[t - n:t].mean()
    pos = (c - l) / np.where(h > l, h - l, np.nan); sig = np.zeros(len(c))
    big = tr > factor * avg
    sig[big & (pos >= 1 - edge)] = -1; sig[big & (pos <= edge)] = 1
    return sig


def kama(close, n=10, fast=2, slow=30):
    c = np.asarray(close, float); fa, sa = 2.0 / (fast + 1), 2.0 / (slow + 1)
    er = efficiency_ratio(c, n); out = np.full(len(c), np.nan); out[n] = c[n]
    for t in range(n + 1, len(c)):
        sc = (er[t] * (fa - sa) + sa) ** 2
        out[t] = out[t - 1] + sc * (c[t] - out[t - 1])
    return out


def parabolic_sar(high, low, af0=0.02, af_step=0.02, af_max=0.20):
    """Wilder parabolic SAR (Kaufman Ch.17). Returns (sar, position +1/-1)."""
    h, l = np.asarray(high, float), np.asarray(low, float); n = len(h)
    sar = np.zeros(n); pos = np.zeros(n); long_ = True; af = af0
    ext = h[0]; sar[0] = l[0]; pos[0] = 1
    for t in range(1, n):
        sar[t] = sar[t - 1] + af * (ext - sar[t - 1])
        if long_:
            sar[t] = min(sar[t], l[t - 1], l[max(t - 2, 0)])
            if l[t] < sar[t]:
                long_, sar[t], ext, af = False, ext, l[t], af0
            elif h[t] > ext: ext, af = h[t], min(af + af_step, af_max)
        else:
            sar[t] = max(sar[t], h[t - 1], h[max(t - 2, 0)])
            if h[t] > sar[t]:
                long_, sar[t], ext, af = True, ext, h[t], af0
            elif l[t] < ext: ext, af = l[t], min(af + af_step, af_max)
        pos[t] = 1 if long_ else -1
    return sar, pos


def mcginley(close, n=10, k=0.6):
    """Book form: MD_t = MD_(t-1) + (p_t - MD_(t-1)) / (k*n*(p_t/MD_(t-1))). (Common published form uses ratio**4.)"""
    c = np.asarray(close, float); md = np.empty(len(c)); md[0] = c[0]
    for t in range(1, len(c)): md[t] = md[t - 1] + (c[t] - md[t - 1]) / (k * n * (c[t] / md[t - 1]))
    return md


def adaptive_stochastic(high, low, close, n_er=10, fast=2, slow=30, smooth=3):
    h, l, c = (np.asarray(x, float) for x in (high, low, close)); er = efficiency_ratio(c, n_er)
    raw = np.full(len(c), np.nan)
    for t in range(max(n_er, slow), len(c)):
        per = int(slow - er[t] * (slow - fast)); per = max(per, 2)
        hh, ll = h[t - per + 1:t + 1].max(), l[t - per + 1:t + 1].min()
        raw[t] = 100.0 * (c[t] - ll) / (hh - ll) if hh > ll else 50.0
    return sma(np.nan_to_num(raw, nan=50.0), smooth)


def trend_adjusted_oscillator(high, low, close, n=10, mid=50.0):
    h, l, c = (np.asarray(x, float) for x in (high, low, close))
    o = 100.0 * (c - l) / np.where(h > l, h - l, np.nan); o = np.nan_to_num(o, nan=50.0)
    on = np.nan_to_num(sma(o, n), nan=mid); mao = np.nan_to_num(sma(on, n), nan=mid)
    return mid - (mao - on)


def variable_ma(close, nmin=5, nmax=30, lo=0.25, hi=1.75, win=30):
    c = np.asarray(close, float); d = np.diff(c, prepend=c[0]); out = np.full(len(c), np.nan)
    for t in range(win, len(c)):
        s = d[t - win + 1:t + 1].std()
        z = abs(d[t]) / s if s > 0 else lo
        k = (nmax - nmin) * np.clip((z - lo) / (hi - lo), 0, 1)
        out[t] = c[max(0, t - int(round(nmax - k)) + 1):t + 1].mean()   # more volatile -> shorter period
    return out


def efficiency_ratio(prices, n=20):
    """Kaufman noise measure: |net change over n| / sum of |daily changes|. ~1 trend, ~0 noise."""
    p = np.asarray(prices, float); out = np.full(len(p), np.nan); d = np.abs(np.diff(p))
    for i in range(n, len(p)):
        path = d[i - n:i].sum(); out[i] = abs(p[i] - p[i - n]) / path if path else np.nan
    return out


def elder_ray(high, low, close, n=13):
    e = ema(close, n=n); return np.asarray(high, float) - e, np.asarray(low, float) - e


def kst(close, specs=((24, 9, 4), (18, 9, 3), (12, 6, 2), (6, 6, 1))):
    """Pring KST: sum of weight * SMA(ROC(period), smooth). Book weights 4,3,2,1 (18-period smoothing assumed 9)."""
    c = np.asarray(close, float); out = np.zeros(len(c))
    for per, sm, w in specs:
        roc = np.full(len(c), np.nan); roc[per:] = 100.0 * (c[per:] / c[:-per] - 1.0)
        out += w * np.nan_to_num(sma(np.nan_to_num(roc, nan=0.0), sm))
    return out


def bollinger(close, n=20, k=2.0):
    c = np.asarray(close, float); m = sma(c, n); s = np.full(len(c), np.nan)
    for t in range(n - 1, len(c)): s[t] = c[t - n + 1:t + 1].std(ddof=0)
    return m, m + k * s, m - k * s


def jackson_zones(h, l, c):
    """Jackson daily zones from yesterday's H, L, C. Returns dict of levels."""
    avg = (h + l + c) / 3.0; high1 = 2 * avg - l; low1 = 2 * avg - h
    return {"high2": avg + high1 - low1, "high1": high1, "average": avg, "low1": low1, "low2": avg - (high1 - low1)}


def rolling_moments(close, n=20):
    """Rolling skew and excess kurtosis of price changes (standard moments)."""
    d = np.diff(np.asarray(close, float), prepend=close[0]); sk = np.full(len(d), np.nan); ku = sk.copy()
    for t in range(n, len(d)):
        w = d[t - n + 1:t + 1]; s = w.std(ddof=0)
        if s > 0: z = (w - w.mean()) / s; sk[t] = (z ** 3).mean(); ku[t] = (z ** 4).mean() - 3.0
    return sk, ku


def kurtosis_skew_signals(high, low, close, k_n=40, s_n=15, atr_n=10, min_vol=0.0, mode="trend"):
    """Kaufman Ch.18: trend mode = buy if kurt crosses below 0, skew>0, ATR>min; mean-rev uses crosses above 0 with opposite skew."""
    h, l, c = (np.asarray(x, float) for x in (high, low, close))
    _, ku = rolling_moments(c, k_n); sk, _ = rolling_moments(c, s_n)
    tr = np.empty(len(c)); tr[0] = h[0] - l[0]
    tr[1:] = np.maximum(h[1:] - l[1:], np.maximum(abs(h[1:] - c[:-1]), abs(l[1:] - c[:-1])))
    atr = sma(tr, atr_n); sig = np.zeros(len(c))
    for t in range(max(k_n, s_n) + 1, len(c)):
        if np.isnan(atr[t]) or atr[t] <= min_vol or np.isnan(ku[t]) or np.isnan(ku[t - 1]): continue
        down = ku[t - 1] > 0 >= ku[t]; up = ku[t - 1] <= 0 < ku[t]
        if mode == "trend":
            if down and sk[t] > 0: sig[t] = 1
            elif down and sk[t] < 0: sig[t] = -1
        else:
            if up and sk[t] < 0: sig[t] = 1
            elif up and sk[t] > 0: sig[t] = -1
    return sig


def value_area(prices, pct=0.60, bins=50):
    """Central cluster of a price histogram: returns (low, high) leaving (1-pct)/2 of observations on each end."""
    p = np.sort(np.asarray(prices, float)); k = int(round(len(p) * (1 - pct) / 2))
    return float(p[k]), float(p[len(p) - 1 - k])


def volatility_measures(high, low, close, n=20, periods=252):
    """Kaufman Ch.20: the five volatility measures at the last bar (returns dict)."""
    h, l, c = (np.asarray(x, float) for x in (high, low, close))
    tr = np.maximum(h[1:] - l[1:], np.maximum(abs(h[1:] - c[:-1]), abs(l[1:] - c[:-1])))
    r = np.diff(c) / c[:-1]
    return {"change_n": abs(c[-1] - c[-1 - n]), "max_range_n": h[-n:].max() - l[-n:].min(), "atr_n": tr[-n:].mean(),
            "sum_abs_changes_n": np.abs(np.diff(c))[-n:].sum(), "annualized_vol": r[-n:].std(ddof=1) * np.sqrt(periods)}


def high_vol_exit_signal(close, n_ma=40, vol_n=20, factor=10.0, reset=0.25):
    """Trend (MA direction) with exit when |return| > factor * prior vol_n-day stdev; re-enter same direction only when
    |return| < reset * exit-day |return|, or on a trend change. Returns position array."""
    c = np.asarray(close, float); r = np.diff(c, prepend=c[0]) / np.where(np.roll(c, 1) == 0, 1, np.roll(c, 1))
    m = sma(c, n_ma); pos = np.zeros(len(c)); cur = 0; locked = False; exit_r = 0.0; prev_dir = 0
    for t in range(max(n_ma, vol_n) + 1, len(c)):
        d = np.sign(m[t] - m[t - 1]); sd = r[t - vol_n:t].std(ddof=1)
        if d != prev_dir: locked = False; cur = d if d != 0 else cur; prev_dir = d
        if not locked and cur != 0 and abs(r[t]) > factor * sd: cur_exit, locked, exit_r = cur, True, abs(r[t])
        if locked and abs(r[t]) < reset * exit_r: locked = False
        pos[t] = 0 if locked else cur
    return pos


def var_historical(returns_matrix, weights, conf_sd=2.33):
    """Kaufman historical VaR: apply current weights (position values) to k days of returns (k x n). Returns negative number."""
    R = np.asarray(returns_matrix, float) @ np.asarray(weights, float)
    return float(R.mean() - conf_sd * R.std(ddof=1))


def var_variance_covariance(values, daily_sd, corr, z=1.65, horizon_days=1):
    """Variance-covariance VaR for positions: values (USD), daily_sd (fractions), corr matrix. Returns positive USD."""
    v = np.asarray(values, float) * np.asarray(daily_sd, float) * z
    C = np.asarray(corr, float)
    return float(np.sqrt(v @ C @ v) * np.sqrt(horizon_days))


def adx(high, low, close, n=14):
    """Wilder DM/ADX/ADXR (Kaufman Ch.23 average-off form). Returns (pdi, mdi, adx, adxr)."""
    h, l, c = (np.asarray(x, float) for x in (high, low, close)); N = len(c)
    pdm = np.zeros(N); mdm = np.zeros(N); tr = np.zeros(N)
    for t in range(1, N):
        up, dn = h[t] - h[t - 1], l[t - 1] - l[t]
        pdm[t] = up if (up > dn and up > 0) else 0.0
        mdm[t] = dn if (dn > up and dn > 0) else 0.0
        tr[t] = max(h[t] - l[t], abs(h[t] - c[t - 1]), abs(l[t] - c[t - 1]))
    P, M, T = pdm[1:n + 1].sum(), mdm[1:n + 1].sum(), tr[1:n + 1].sum()
    pdi = np.full(N, np.nan); mdi = pdi.copy(); dx = pdi.copy(); a = pdi.copy()
    for t in range(n, N):
        if t > n: P, M, T = P - P / n + pdm[t], M - M / n + mdm[t], T - T / n + tr[t]
        pdi[t], mdi[t] = 100 * P / T, 100 * M / T
        dx[t] = 100 * abs(pdi[t] - mdi[t]) / (pdi[t] + mdi[t]) if pdi[t] + mdi[t] else 0.0
        a[t] = dx[t] if t == n else a[t - 1] + 0.133 * (dx[t] - a[t - 1])
    adxr = np.full(N, np.nan); adxr[2 * n:] = (a[2 * n:] + a[n:N - n]) / 2.0
    return pdi, mdi, a, adxr


def commodity_selection_index(adxr, atr14, v, margin, commission):
    """CSI = ADXR x ATR14 x K; K = 100 * (v / sqrt(margin)) * (1 / (150 + commission)). (Wilder form; verify vs source.)"""
    K = 100.0 * (v / np.sqrt(margin)) * (1.0 / (150.0 + commission))
    return adxr * atr14 * K


def kelly_fraction(p_win, payoff_ratio):
    """f = (p (PLR+1) - 1) / PLR; <=0 means no edge."""
    return (p_win * (payoff_ratio + 1.0) - 1.0) / payoff_ratio


def optimal_f(trade_returns, grid=None):
    """Vince optimal f: maximize geometric mean of (1 + f * R_i / |largest loss|). Returns (f, geometric_mean)."""
    r = np.asarray(trade_returns, float); big = abs(r.min())
    grid = np.arange(0.01, 1.0001, 0.01) if grid is None else grid
    gm = [np.prod(np.maximum(1.0 + f * r / big, 1e-12)) ** (1.0 / len(r)) for f in grid]
    i = int(np.argmax(gm)); return float(grid[i]), float(gm[i])


def prob_losing_streak(p_loss, n_losses, n_trades=None):
    """P(n_losses in a row starting at a given trade) = p^n; with n_trades, P(at least one such run) by dynamic programming."""
    if n_trades is None: return p_loss ** n_losses
    k = n_losses; state = np.zeros(k); state[0] = 1.0; hit = 0.0          # state[j] = prob current streak length j (no run yet)
    for _ in range(n_trades):
        new = np.zeros(k); new[0] = state.sum() * (1 - p_loss)
        for j in range(k - 1): new[j + 1] = state[j] * p_loss
        hit += state[k - 1] * p_loss; state = new
    return float(hit)
