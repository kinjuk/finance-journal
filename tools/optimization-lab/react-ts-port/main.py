"""Optimization Lab API: wraps the SciPy engine behind one validated endpoint."""
import functools
import os
import re
import time
from datetime import date
from typing import Literal

import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator, model_validator

import engine as E

app = FastAPI(title="Optimization Lab API")
app.add_middleware(CORSMiddleware, allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(","),
                   allow_methods=["GET", "POST"], allow_headers=["*"])
TICKER = re.compile(r"^[A-Z0-9.\-=^]{1,12}$")


class Req(BaseModel):
    tickers: list[str] = Field(min_length=2, max_length=12)
    start: date = date(2015, 1, 1)
    end: date | None = None
    min_weight: float = Field(0.05, ge=0, le=0.5)
    max_weight: float = Field(0.40, gt=0, le=1)
    rf: float = Field(0.04, ge=0, le=0.15)
    estimator: Literal["arith", "log"] = "arith"

    @field_validator("tickers")
    @classmethod
    def clean(cls, v):
        v = list(dict.fromkeys(t.strip().upper() for t in v))
        bad = [t for t in v if not TICKER.match(t)]
        if bad:
            raise ValueError(f"Invalid ticker(s): {', '.join(bad)}")
        if len(v) < 2:
            raise ValueError("Need at least 2 distinct tickers")
        return v

    @model_validator(mode="after")
    def check(self):
        n = len(self.tickers)
        if (self.end or date.today()) <= self.start:
            raise ValueError("End date must be after start date")
        if not E.feasible(n, self.min_weight, self.max_weight):
            raise ValueError(f"Infeasible: {n} assets × min {self.min_weight:.0%} = {n*self.min_weight:.0%}, "
                             f"× max {self.max_weight:.0%} = {n*self.max_weight:.0%}. Need min-sum ≤ 100% ≤ max-sum.")
        return self


@functools.lru_cache(maxsize=64)
def _prices(tickers: tuple, start: str, end: str, hour: int):
    return E.load_prices(list(tickers), start, end)  # `hour` busts the cache hourly


def _m(m):
    return {"expected_annual_return": m["ret"], "annual_volatility": m["vol"],
            "sharpe_ratio": m["sharpe"], "sortino_ratio": m["sortino"]}


@app.get("/api/health")
def health():
    return {"ok": True}


@app.post("/api/optimize")
def optimize(q: Req):
    end = q.end or date.today()
    try:
        p = _prices(tuple(q.tickers), str(q.start), str(end), int(time.time() // 3600))
    except Exception:
        raise HTTPException(502, "Market data provider failed. Try again shortly.")
    missing = [t for t in q.tickers if t not in p.columns]
    if missing:
        raise HTTPException(422, f"No data for: {', '.join(missing)}")
    if len(p) < 250:
        raise HTTPException(422, "Need roughly one year of overlapping history for all tickers.")
    mu, cov, r = E.estimate(p, q.estimator)
    results = {}
    for o in E.OBJECTIVES:
        x = E.solve(o, mu, cov, r, q.rf, q.min_weight, q.max_weight)
        results[o] = ({"ok": False, "message": str(x["msg"])} if not x["ok"] else
                      {"ok": True, "weights": {k: float(v) for k, v in x["w"].items()}, "metrics": _m(x["m"]),
                       "at_bounds": x["bound"], "turnover": x["turnover"], "message": str(x["msg"])})
    eq = E.perf(np.full(len(mu), 1 / len(mu)), mu, cov, r, q.rf)
    cl = E.cloud(mu, cov, q.min_weight, q.max_weight)
    corr = r.corr().fillna(0)
    return {"period": {"start": str(p.index[0].date()), "end": str(p.index[-1].date()), "days": len(p)},
            "assumptions": {"estimator": q.estimator, "risk_free": q.rf, "min_weight": q.min_weight, "max_weight": q.max_weight},
            "results": results, "equal_weight": _m(eq),
            "frontier": E.frontier(mu, cov, q.min_weight, q.max_weight).to_dict("records"),
            "cloud": cl.sample(min(600, len(cl)), random_state=0).to_dict("records"),
            "assets": [{"ticker": t, "ret": float(mu[t]), "vol": float(np.sqrt(cov.loc[t, t]))} for t in mu.index],
            "correlation": {"labels": list(corr.columns), "matrix": corr.values.tolist()}}
