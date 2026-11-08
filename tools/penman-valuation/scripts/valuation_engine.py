#!/usr/bin/env python3
"""Valuation engine for accounting-based valuation (residual operating income,
abnormal operating income growth, DCF) with a consistency check, implied-growth
solver and sensitivity grid.

Usage:
  python valuation_engine.py value        input.json
  python valuation_engine.py implied-growth input.json     (needs "price")
  python valuation_engine.py sensitivity  input.json

Input JSON (all money in the same unit, income after tax):
{
  "r": 0.086,              # required return for operations
  "g": 0.05,               # growth in ReOI / NOA after the horizon (ignored if terminal_ops_value given)
  "terminal_ops_value": null, # optional: value of operations at T from your own steady-state
                           # FCF/(r-g). Use when GAAP depreciation is not replaced 1:1 (real estate,
                           # long-lived assets): the default terminal assumes NOA and ReOI grow at g,
                           # i.e. depreciation fully reinvested forever.
  "noa0": 4551,            # beginning net operating assets (year 0 balance)
  "oi": [1175, 1269, ...], # operating income, years 1..T
  "noa": [4817, 5209, ...],# ending NOA, years 1..T
  "nfo0": -289,            # net financial obligations at t0 (negative = net financial assets)
  "minority": 0,           # optional claims on equity (minority interest, preferred)
  "overhang": 0,           # optional option overhang liability
  "shares": 263.1,         # shares outstanding (same scale as money)
  "price": 75              # optional, for implied-growth
}
"""
import json
import sys


def _series(d):
    r, g, noa0 = d["r"], d["g"], d["noa0"]
    oi, noa = d["oi"], d["noa"]
    T = len(oi)
    assert len(noa) == T and T >= 1, "oi and noa must have equal length >= 1"
    assert d.get("terminal_ops_value") is not None or r > g, "need r > g for a finite continuing value"
    prev = [noa0] + noa[:-1]
    reoi = [oi[t] - r * prev[t] for t in range(T)]
    fcf = [oi[t] - (noa[t] - prev[t]) for t in range(T)]
    return r, g, noa0, oi, noa, prev, reoi, fcf, T


def value(d):
    r, g, noa0, oi, noa, prev, reoi, fcf, T = _series(d)
    rho = 1 + r
    claims = d.get("nfo0", 0) + d.get("minority", 0) + d.get("overhang", 0)

    tov = d.get("terminal_ops_value")
    pv_reoi = sum(reoi[t] / rho ** (t + 1) for t in range(T))
    if tov is not None:
        # explicit terminal: V_ops at T supplied; ReOI and DCF stay equivalent by construction
        cv_reoi = (tov - noa[-1]) / rho ** T
        v_reoi = noa0 + pv_reoi + cv_reoi
        pv_fcf = sum(fcf[t] / rho ** (t + 1) for t in range(T))
        v_dcf = pv_fcf + tov / rho ** T
        out = {
            "value_ops": {"reoi": v_reoi, "dcf": v_dcf},
            "max_gap": abs(v_reoi - v_dcf),
            "reoi_by_year": reoi, "fcf_by_year": fcf,
            "composition": {"book_noa0": noa0, "pv_explicit_reoi": pv_reoi,
                            "pv_continuing_value": cv_reoi,
                            "continuing_value_share_of_ops": cv_reoi / v_reoi if v_reoi else None},
            "claims_deducted": claims, "value_equity": v_reoi - claims,
            "note": "explicit terminal value used; AOIG check skipped",
        }
        if d.get("shares"):
            out["value_per_share"] = out["value_equity"] / d["shares"]
        return out

    # 1) Residual operating income
    reoi_next = reoi[-1] * (1 + g)
    cv_reoi = reoi_next / (r - g) / rho ** T
    v_reoi = noa0 + pv_reoi + cv_reoi

    # 2) Abnormal operating income growth
    #    AOIG_t = ReOI_t - ReOI_{t-1}, t>=2 ; terminal AOIG_{T+1} = g * ReOI_T
    aoig = [reoi[t] - reoi[t - 1] for t in range(1, T)]  # t = 2..T
    pv_aoig = sum(aoig[k] / rho ** (k + 1) for k in range(len(aoig)))  # AOIG_t / rho^(t-1), t=k+2
    aoig_next = g * reoi[-1]
    cv_aoig = aoig_next * rho ** (1 - T) / (r - g)
    v_aoig = (oi[0] + pv_aoig + cv_aoig) / r

    # 3) DCF with terminal FCF consistent with ReOI growing at g (NOA grows at g)
    oi_next = reoi_next + r * noa[-1]
    fcf_next = oi_next - g * noa[-1]
    pv_fcf = sum(fcf[t] / rho ** (t + 1) for t in range(T))
    cv_dcf = fcf_next / (r - g) / rho ** T
    v_dcf = pv_fcf + cv_dcf

    out = {
        "value_ops": {"reoi": v_reoi, "aoig": v_aoig, "dcf": v_dcf},
        "max_gap": max(v_reoi, v_aoig, v_dcf) - min(v_reoi, v_aoig, v_dcf),
        "reoi_by_year": reoi,
        "fcf_by_year": fcf,
        "composition": {
            "book_noa0": noa0,
            "pv_explicit_reoi": pv_reoi,
            "pv_continuing_value": cv_reoi,
            "continuing_value_share_of_ops": cv_reoi / v_reoi if v_reoi else None,
        },
        "claims_deducted": claims,
        "value_equity": v_reoi - claims,
    }
    if d.get("shares"):
        out["value_per_share"] = out["value_equity"] / d["shares"]
    return out


def implied_growth(d, lo=-0.5, hi=None):
    """Find g so that value per share == price (bisection). Needs d['price'], d['shares']."""
    target = d["price"] * d["shares"]
    hi = (d["r"] - 1e-6) if hi is None else hi
    f = lambda g: value({**d, "g": g})["value_equity"] - target
    if f(lo) > 0:
        return {"implied_g": None, "note": "price below value even at the lowest growth tried"}
    if f(hi) < 0:
        return {"implied_g": None, "note": "price above value even at g -> r"}
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return {"implied_g": (lo + hi) / 2, "required_return": d["r"]}


def sensitivity(d, dr=(-0.02, -0.01, 0, 0.01, 0.02), dg=(-0.02, -0.01, 0, 0.01, 0.02)):
    grid = []
    for a in dr:
        row = []
        for b in dg:
            r2, g2 = d["r"] + a, d["g"] + b
            if r2 <= g2:
                row.append(None)
                continue
            v = value({**d, "r": r2, "g": g2})
            row.append(v.get("value_per_share", v["value_equity"]))
        grid.append(row)
    return {"r_values": [d["r"] + a for a in dr], "g_values": [d["g"] + b for b in dg], "grid": grid}


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    cmd, path = sys.argv[1], sys.argv[2]
    data = json.load(open(path))
    fn = {"value": value, "implied-growth": implied_growth, "sensitivity": sensitivity}[cmd]
    print(json.dumps(fn(data), indent=2))
