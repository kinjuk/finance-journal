---
name: trading-systems
description: Framework for designing, testing, stress-testing, sizing and monitoring systematic trading strategies, distilled from Perry Kaufman's Trading Systems and Methods. Use whenever the user wants to build, backtest, optimize, validate, critique or compare a trading strategy or system (trend following, momentum, mean reversion, breakout, spreads, day trading, portfolio of strategies), asks whether a backtest is trustworthy or overfit, needs walk-forward or out-of-sample design, performance metrics (Sharpe, Sortino, Calmar, Ulcer Index, drawdown), position sizing, volatility targeting, stop-loss design, risk of ruin, or leverage. Trigger even if they do not say "trading system", e.g. "is my backtest any good", "how should I size this", "optimize my moving average".
---

# Trading Systems (Kaufman framework)

Purpose: be the validation-and-risk backbone for ANY strategy idea. Most failed systems fail from bad testing and sizing, not bad ideas. Be blunt: if a result is likely overfit, say so and say why.

## Workflow

1. **Classify the request**: design a strategy, evaluate an existing backtest, stress-test/robustness, size/risk, or compare systems.
2. **Demand the premise first.** Every strategy needs a stated economic or price-behavior reason it works, plus written expectations (time frame, expected risk, expected % winners, objective metric) BEFORE any test. No premise + lots of testing = discovery by overfitting. Refuse to bless results with no stated premise.
3. **Load the right reference** (only what the task needs):
   - Testing, optimization, overfitting, walk-forward, data choice -> `references/testing.md`
   - Metrics, leverage, volatility targeting, position size, stops, ruin -> `references/risk-sizing.md`
   - Portfolio allocation, diversification, volatility stabilization -> `references/portfolio.md`
   - Practical pitfalls, price shocks, system trade-offs, signal similarity -> `references/pitfalls.md`
   - Trend following (MA, breakout, multi-trend, speed choice) -> `references/trend.md`
   - Momentum, RSI, MACD, stochastic, divergence -> `references/momentum.md`
   - Seasonality and calendar effects -> `references/seasonality.md`
   - Cycles -> `references/cycles.md`
   - Volume, open interest, breadth -> `references/volume.md`
   - Spreads, pairs trading, market neutral, carry -> `references/spreads.md`
   - News/event trading, COT, sentiment, Fibonacci folklore -> `references/behavioral.md`
   - Pattern studies (gaps, weekday, projections), computer pattern recognition -> `references/patterns.md`
   - Day trading, intraday costs, opening range breakout, shock fades -> `references/daytrading.md`
   - Adaptive methods (KAMA, parabolic SAR, adaptive RSI/stochastic) -> `references/adaptive.md`
   - Distribution methods (Bollinger, zones, skew/kurtosis, Market Profile) -> `references/distribution.md`
   - Multiple time frames (Triple Screen, KST, trend + timing) -> `references/timeframes.md`
   - Volatility filters, liquidity, noise, AI/GA/NN cautions, replication -> `references/advanced.md`
   - Basics, returns/volatility conventions, noise measurement, charting -> `references/foundations.md`
   - Swing/P&F, regression signals, moving average and EMA math -> `references/swing-regression-ma.md`
4. **Compute, don't eyeball.** Use `scripts/metrics.py` (`report`, `walk_forward`, `sensitivity_layers`, `pct_step_values`, `risk_of_ruin`, `vol_stabilize`, `cap_positions`) on a daily returns series and `scripts/indicators.py` for signals and noise.
5. **Verdict format**: (a) what passes, (b) what fails or is unproven, (c) the single most likely way it breaks live, (d) the next test to run. Quantify with metrics; benchmark against buy-and-hold or 60/40.

## Non-negotiable rules (each explained in testing.md / risk-sizing.md)
- Testing validates; it does not discover. Define parameter ranges before testing and never widen them to rescue a result.
- One-shot out-of-sample. Any change after seeing it turns it into in-sample (feedback = overfitting).
- Choose a broad plateau, never the peak. If all neighbors of the chosen parameters are worse, it is overfit. Run sensitivity (including n-space layers) and a cross-market check.
- Count ALL tests across ALL ideas when judging significance. Robust systems have few parameters (about four or fewer) and a sound premise.
- Costs and slippage must be realistic; per-trade edge smaller than round-trip cost is dead. Fast systems die here first.
- Profits must be spread through time and not dominated by one price shock or one bull market. Check share of profit from the best few periods.
- Size by volatility to a target risk, scale to the drawdown you can survive; historic max drawdown understates future drawdown.
- Trade exactly what was tested, on the data you tested, and monitor slippage and live-vs-test gaps.
- Real results will be worse than the backtest. Simple and general beats complex and tuned.

## Coverage
All 24 chapters of the book are distilled; each reference file lists at the top what it leaves out.
- Ch. 1-4 `foundations.md`; Ch. 5-7 `swing-regression-ma.md`; Ch. 8 `trend.md`; Ch. 9 `momentum.md`; Ch. 10 `seasonality.md`; Ch. 11 `cycles.md`; Ch. 12 `volume.md`; Ch. 13 `spreads.md`; Ch. 14 `behavioral.md`; Ch. 15 `patterns.md`; Ch. 16 `daytrading.md`; Ch. 17 `adaptive.md`; Ch. 18 `distribution.md`; Ch. 19 `timeframes.md`; Ch. 20 `advanced.md`; Ch. 21 `testing.md`; Ch. 22 `pitfalls.md`; Ch. 23 `risk-sizing.md`; Ch. 24 `portfolio.md`.
- Code: `scripts/metrics.py` (performance report, walk-forward harness, n-space sensitivity, percent-step parameter ladders, risk of ruin, volatility stabilization, exposure cap) and `scripts/indicators.py` (moving averages, regression, breakout, swing/pivots, momentum/oscillators, volume, seasonal table, spreads/pairs, adaptive, distribution, volatility, VaR, ADX/CSI, Kelly/optimal f). `scripts/example_walkforward.py` is a runnable template of the walk-forward workflow.
- Not in the skill (say so, and label any answer as general knowledge, not from the book): option-implied-volatility mechanics and AI-tool internals (Ch. 20), genetic-algorithm solver internals (Ch. 24), numeric probability tables (Ch. 15), binomial/chi-square tables (Ch. 23).
- Where the source is internally inconsistent or garbled by text extraction, the reference says so (VaR example in risk-sizing.md, McGinley and CSI formulas, Jackson zones, kurtosis sell rule). Trust the flagged corrections.
- The indicator code is smoke-tested only. It has never been validated against live data or the book's published results, except the risk-of-ruin and VaR examples. Say so when a user relies on a signal's output.

## Known limits of the source
Kaufman (5th ed., 2013) is futures-centric and pre-dates today's crowding of classic trend rules, low-cost retail execution, and crypto/ETF markets. Treat his numbers (slippage, benchmarks) as illustrative, and re-check them with current data.
