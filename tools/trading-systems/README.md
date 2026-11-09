# trading-systems

A Claude skill for designing, testing, stress-testing, sizing and monitoring systematic trading strategies, distilled from Perry Kaufman's *Trading Systems and Methods* (5th ed.).

It acts as the validation and risk backbone for any strategy idea: demand a premise first, validate out-of-sample, test robustness (sensitivity, walk-forward, cross-market), size by volatility, and monitor live results against test expectations.

## Contents

- `SKILL.md` - workflow, non-negotiable rules, coverage map and known limits (the file Claude reads).
- `references/` - one file per topic area, covering all 24 chapters: `testing`, `risk-sizing`, `portfolio`, `pitfalls`, `foundations`, `swing-regression-ma`, `trend`, `momentum`, `seasonality`, `cycles`, `volume`, `spreads`, `behavioral`, `patterns`, `daytrading`, `adaptive`, `distribution`, `timeframes`, `advanced`. Each file lists at the top what it leaves out.
- `scripts/metrics.py` - performance report (Sharpe, Sortino, Calmar, Ulcer, drawdown), walk-forward harness, n-space sensitivity, risk of ruin, volatility stabilization, exposure cap.
- `scripts/indicators.py` - moving averages, regression, breakout, swing/pivots, momentum and oscillators, volume, seasonal table, pairs/spreads, adaptive, distribution, volatility, VaR, ADX/CSI, Kelly/optimal f.
- `scripts/example_walkforward.py` - runnable template of the walk-forward workflow.

## Usage

```
cd scripts
python example_walkforward.py          # synthetic demo; replace `price` with real closes
python metrics.py returns.csv --col ret --periods 252
```

## Notes

- The skill contains the method distilled in original wording. It does not reproduce text from the book.
- Indicator code is smoke-tested only, not validated against live data or the book's published results (except the risk-of-ruin and VaR examples). Where the source was inconsistent or garbled by text extraction, the reference says so.
- The source is futures-centric and dates from 2013; re-check its cost and edge assumptions against current data.
