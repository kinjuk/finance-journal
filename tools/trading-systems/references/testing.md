# Testing and validation (Kaufman Ch. 21)

Core thesis: testing exists to VALIDATE an idea you specified in advance, not to DISCOVER one. Computers do not think; unlimited testing power plus no prior expectations produces overfit systems that fail live.

## Contents
1. Before any test
2. Parameters
3. Test data
4. Testing integrity (in/out-of-sample, step-forward)
5. Searching for the best result
6. Refining rules
7. Robustness and validity
8. Performance criteria and benchmarks
9. Sensitivity testing
10. Final parameter selection checklist
11. Live monitoring

## 1. Before any test: expectations
Write down BEFORE running anything:
- Objective metric (not "max profit"). Max profit rewards one or two huge winners and hides a long string of small losses (e.g. gold flat 1985-2005 then a spike). Industry default: Sharpe/information ratio = (annualized return - risk-free) / annualized risk. Also record max drawdown, % profitable trades, avg win / avg loss, and for day trading profit per share/contract (costs and slippage dominate there).
- Time frame (hourly/daily/weekly), expected relative risk, expected % winners.
- If results contradict expectations, something is wrong; do not just accept the number. If you had no expectations, you cannot tell a good idea from an overfit one.

## 2. Parameters
- A parameter is any value that changes speed or timing: MA period, smoothing constant, band width, RSI period, stop size, max holding period.
- Limit the ranges up front. Forcing that decision keeps the test near validation and away from indiscriminate exploration. (250 MA x 30 RSI x 30 stops = 225,000 runs: possible, but meaningless.)
- Space values by PERCENTAGE steps, not equal steps: dense at small values, sparse at large (e.g. x1.5 each: 1, 1.5, 2.3, 3.4, 5, 7.6...). A 49 vs 50 day MA differs 2%; 2 vs 3 differs 50%. Equal steps overweight the slow end and bias averages.
- Test one parameter at a time in order of importance (the one carrying the big picture first: trend period, then entry timing, then stops). A strategy should not be driven by its stop size.
- Variable types: continuous (%), discrete (integer days), coded (rule/regime switch such as A=single MA, B=double MA, C=regression). Only continuous/discrete parameters should show a smooth pattern; do not plot or "smooth" coded results as if they were continuous.

## 3. Test data
- Best series = built from the contract/instrument you will actually trade. For futures: back-adjusted, rolled on the volume/open-interest switch (most liquid). Keep a second unadjusted series, rolled on the same dates, for true price levels.
- Back-adjusted futures: percent-of-price calculations break (older prices shift, can go negative). Fine for MAs and momentum. Never compare historic highs/lows on the adjusted series.
- Split-adjusted stocks: prices scale but volatility/price relationship does not (a $12.50 adjusted stock behaves like the original $50 stock).
- Indexed (percentage-return) series: good for cross-market comparison and portfolios, closest to volatility-adjusted, but you must trade off the same indexed values.
- Full individual contracts: overlap makes some periods tested 6x and others once; biased.
- Constant-maturity ("perpetual") series: smoother than anything tradable, no real price occurred; expect understated risk and profit, overstated trend reliability.
- Cash/spot data is not a substitute for futures (basis, interest differentials; FX: use interest-rate parity to approximate).
- Synthetic data: shuffling real segments (Monte Carlo) separates bull runs from their tops, unrealistic. Random-number series lack long runs and fat tails. Useful for sanity checks only; if a system exploits structure you built in, it proves nothing.

## 4. Testing integrity
- Split data: ~50% in-sample (develop, torture freely), ~50% out-of-sample (final validation, ONE use).
- In-sample choices, best to worst: alternating random periods fixed at project start > alternating equal blocks > first half > last half. First/last half bakes in one volatility regime.
- Evaluate alternating periods as one concatenated stream of DAILY returns, never as per-block total profit (block-boundary gains/losses = cheating).
- Use a different random split for each system so the same data is not reused for everything.
- Out-of-sample is a one-shot test. Typical result: ~50% of in-sample return. Information ratio 2.0 -> 1.0 is acceptable; 2.0 -> 0.4 is a failure.
- FEEDBACK RULE: once you look at out-of-sample and then change anything, it is in-sample now. The result is overfitting. No second chance. If you need another test, reserve fresh data (or accept the system is dead).
- Step-forward (walk-forward) procedure: choose total period -> choose in-sample window (e.g. 2y) -> optimize -> apply best params to the next out-of-sample slice (e.g. 6m) -> roll forward by that slice -> accumulate ONLY the out-of-sample slices as the result.
- Walk-forward bias: short in-sample windows favor fast systems (slow ones see few trades). Diagnostic: the "best" parameter jumps around (10d, then 50d, then 15d). Fix: lengthen windows (2y -> 5y), at the cost of data.
- Walk-forward also suffers feedback if repeated while tweaking rules: hold back a final untouched block.

## 5. Searching for the best result
- "Best" = most ROBUST parameter region, not the maximum of the objective. The maximum is almost never the robust choice.
- Count tests before starting (time AND storage). If too many, scan a coarse grid first, then refine the promising region.
- Sequential optimization (fix best param, move to next) cuts n1*n2*n3 to n1+n2+n3 but can miss the peak. Fix: seeding, i.e. repeat from several random starting values; if 3+ seeds converge on the same peak, trust it.
- Mathematical/automatic search (steepest descent, genetic algorithms) only makes sense for continuous, smooth results. Never average or auto-select across coded rule switches (e.g. long-only/short-only/both).

## 6. Refining rules (in-sample only)
- A new rule that fixes one situation but turns other parameter settings into bigger losses (average same, distribution more extreme) is curve fitting. High kurtosis of results is a symptom.
- Accept a rule only if it improves performance across essentially ALL parameter values. A rule that touches one or two trades will not survive.

## 7. Robustness and validity
- Verify good results as hard as you verify bad ones; people audit failures and wave through successes.
- One famous call (short before 1987, before 2008) proves nothing; a computer can always find an indicator combo that did it. Do not extrapolate from a well-chosen example.
- Data skewed one way (1990s equities, 1980s-2012 long bonds) yields a biased system. Ask what happens in the opposite scenario.
- Test data must contain price shocks, or you cannot know if you survive one.
- Robust = fewest parameters over the most data. Best-performing systems in Futures Truth data commonly had four or fewer variables.
- Three requirements of a robust system, all needed together:
  1. Sound premise: each rule exploits a real fundamental or price phenomenon. A pattern found only by optimization is probably an illusion (test enough patterns and one fits).
  2. Adapts to changing conditions: no fixed dollar/price levels; volatility-scaled stops; position size varying with risk.
  3. Tested properly: most data, bull/bear/sideways, in/out-of-sample, or paper trade until the trade count supports comparison.
- Significance: if you tested 1,000 parameter values or 100 strategies, one winner is not significant. Count the cumulative number of tests across ALL ideas tried, not just the final one. Rough heuristic: robust if ~70% of tests over a pre-set, reasonable range are profitable (invalid if you narrowed the range after peeking).

## 8. Performance criteria and benchmarks
- Fix the parameter test ranges BEFORE testing (e.g. short MA 3-15, RSI 3-10). If the sensible range is unprofitable, revisit the concept; do not widen the range until something works.
- Benchmark everything (S&P, Treasury index, CTA index such as BarclayHedge). If simple buy-and-hold beats the system, the system is not adding value. Published benchmarks hide survivorship bias (dead funds drop their last, worst months). -50% then +50% = -25%, not flat.
- Chase consistency, not the single best month; top monthly performers are usually the most erratic.
- Criteria, in order of usefulness:
  1. Information ratio (annualized return / annualized stdev). The single most important measure. Profit factor (gross profit / gross loss) is an alternative.
  2. Net profit (necessary, not sufficient for choosing parameters).
  3. Number of trades: few trades = statistically unreliable.
  4. % profitable: above 60% = steady profit capture; a trend system working correctly shows only 30-40%.
  5. Average net return per trade: compare to round-trip cost. A $50 per-trade edge in currencies dies to ~$100 round-trip slippage. Fast systems look good until realistic costs are applied. Always test with correct transaction costs.

## 9. Sensitivity testing (do after choosing parameters)
- Shift each parameter, and combinations, up and down by small amounts. Robust = modest decay moving away from the choice. If every neighbor is worse, you picked a peak: overfit.
- n-space method: with core values (w0, x0, y0, z0), radius r_i^2 = sum of squared differences per parameter (normalize parameters to comparable scale first). Sort all tests by r, split into ~10 concentric layers, average performance per layer, inspect the decay curve. Optionally sample random parameter sets in the range and look for the most robust layer.
- Cross-market check: a system that works on the S&P but loses on NASDAQ/Dow is overfit. Similar markets are free out-of-sample data.
- Systems sold for one market with high profit/low risk and hidden rules: assume fitted and unverifiable.

## 10. Final parameter selection checklist
Apply in this order. All must pass before trading.
a. After in/out-of-sample passes, a final run on ALL data (to stay current) is acceptable for choosing final values.
b. Choose from a broad plateau of average results, not the peak.
c. Profits spread evenly across the test period; decaying profits (e.g. trend on 1990s S&P) are a red flag, mild improvement in recent years is fine.
d. Check share of profit from price shocks. If >50% of shocks were windfalls, or the largest shock was a windfall, risk is understated; real trading has far fewer windfall shocks. Results with no large negative shock jumps are unrealistic.
e. Scale to personal risk: annual return 50% with annual stdev 20% means ~2.5% chance of -40% in a year; if you tolerate only -20% at 2.5%, halve leverage and expect ~25%.
f. Prefer the parameter set with less time in the market at comparable returns (being flat is the only shock defense; do not reverse positions needlessly; separate exits from entries to improve slippage).
g. Out-of-sample must validate. If no fresh data, use similar markets or older data; further decay there = overfit.

## 11. Live monitoring
- Trade EXACTLY the rules tested; a "simple version" in test and a richer one live, or an untested last-minute rule, voids the test.
- Trade the same data you tested (back-adjusted continuous series omits roll costs; FX test data from different banks than live quotes differ).
- Track slippage versus system price: it gives true execution cost, capacity, and best time of day. Compare live results to test expectations; no comparison = no basis for judging.
- Development never ends: markets, correlations, and volatility drift. Reallocate based on monitoring.
- Real-time results will be worse than historic. Simplest and most general rules/parameters have lower backtest returns but best odds of holding up. Begin simple, add complexity slowly, stop early.
