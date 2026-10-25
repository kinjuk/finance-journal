import numpy as np
import pandas as pd
import pytest
from fastapi.testclient import TestClient

import engine as E
import main


def fake(tickers, start, end):
    n, k = 1500, len(tickers)
    rng = np.random.default_rng(0)
    r = rng.normal(np.linspace(2e-4, 5e-4, k), np.linspace(.004, .013, k), (n, k))
    return pd.DataFrame(100 * np.exp(np.cumsum(r, 0)), index=pd.bdate_range("2018-01-01", periods=n), columns=list(tickers))


@pytest.fixture(autouse=True)
def patch(monkeypatch):
    monkeypatch.setattr(E, "load_prices", fake)
    main._prices.cache_clear()


client = TestClient(main.app)
BODY = {"tickers": ["AAA", "BBB", "CCC", "DDD", "EEE"]}


def test_contract_and_constraints():
    j = client.post("/api/optimize", json=BODY).json()
    for o in ("sharpe", "sortino", "minvol"):
        r = j["results"][o]
        w = list(r["weights"].values())
        assert r["ok"] and abs(sum(w) - 1) < 1e-6 and min(w) >= .05 - 1e-6 and max(w) <= .4 + 1e-6
    assert len(j["frontier"]) > 10 and len(j["correlation"]["matrix"]) == 5


def test_optimizers_dominate_equal_weight():
    j = client.post("/api/optimize", json=BODY).json()
    assert j["results"]["sharpe"]["metrics"]["sharpe_ratio"] >= j["equal_weight"]["sharpe_ratio"] - 1e-9
    assert j["results"]["minvol"]["metrics"]["annual_volatility"] <= j["equal_weight"]["annual_volatility"] + 1e-9


@pytest.mark.parametrize("patchbody", [{"min_weight": .3}, {"max_weight": .1}, {"tickers": ["AAA", "bad ticker!"]}, {"tickers": ["AAA", "AAA"]}])
def test_validation_rejects(patchbody):
    assert client.post("/api/optimize", json={**BODY, **patchbody}).status_code == 422


def test_provider_failure_is_502(monkeypatch):
    def boom(*a):
        raise RuntimeError("down")
    monkeypatch.setattr(E, "load_prices", boom)
    main._prices.cache_clear()
    assert client.post("/api/optimize", json=BODY).status_code == 502
