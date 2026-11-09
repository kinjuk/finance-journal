# Advanced techniques (Kaufman Ch. 20, distilled)

Not distilled: option-implied volatility mechanics, the VIX strategy rules in detail (Connors CVR-9), the full volatility-filter result tables, expert-system and fuzzy-logic worked examples, fractal-dimension and entropy calculations beyond the idea, neural-network architecture and genetic-algorithm mechanics, hedge-fund replication math. Code: `volatility_measures`, `high_vol_exit_signal` in scripts/indicators.py. The author is cautious about the AI/chaos tools: they overfit unless held to the out-of-sample rules in testing.md.

## Contents
1. Volatility and the price-volatility relationship
2. Five volatility measures
3. Using volatility for trading
4. Volatility filters on entries and exits
5. Liquidity
6. Noise and trend speed
7. Trends and interest-rate carry
8. Expert systems, fuzzy logic, chaos, neural nets, genetic algorithms
9. Hedge-fund replication

## 1. Price-volatility relationship
- Volatility rises and falls with the price level: roughly lognormal (percentage-growth). Check: volatility at p_t ~ volatility at p_s x ln(p_t)/ln(p_s) (price 20, volatility $1.00 -> price 40, volatility $1.23). Use a log scale/percent returns for charts and risk across price levels. Use natural log (ln), not log10.
- Volatility grows with the interval measured (roughly with the square root of time); two stocks at the same price can have very different volatility (news flow), which matters for sizing, pairs balance and portfolio risk.
- Base price: commodities have a production-cost floor where volatility collapses; adjust price: d = ln(p/p0) or ln(p - p0); estimate p0 from a linear regression or the lowest sustainable level. Exceptions: interest rates (use YIELD, not futures price), FX (no base, only equilibrium; volatility rises away from it), energy (cartel-managed range; shocks when supply changes).

## 2. Five volatility measures (n recent days)
1. Change in price over n: |C_t - C_(t-n)| (depends on two points only; always lower than range-based measures).
2. Maximum fluctuation: highest high - lowest low over n (estimates the largest move for the holding period; basis for stops/targets).
3. Average true range (ATR(n)): the most popular; stops/targets = factor x ATR; guides risk.
4. Sum of |close changes| over n (misses the gap to the prior close; use returns for stocks).
5. Classic annualized volatility = stdev(daily returns) x sqrt(252).
- Ratio of short-term to long-term volatility (e.g. 10 vs 60 days) detects expansion; lag the longer period to avoid overlap; relative volatility compares the same market over time.

## 3. Using volatility for trading
- Intraday volatility and volume share the same U shape (highest at open, lowest mid-session, up again toward the close; R = 0.595 in NASDAQ-100); options view: long gamma at open/close, short theta mid-session.
- Predicting tomorrow's range (Brower, S&P 1987-95): higher volatility follows (1) a 3-day average true range above a threshold (very good), (2) RSI(3) below 40 (good), (3) a close far from the prior close levels; weak predictors: inside days; lower volatility after outside days (modest); Mondays lowest, Tuesdays/Fridays highest. Small-sample rules marked "few cases" are unreliable.
- On-Balance True Range (Bierovic): OBV logic with true range in place of volume, smoothed with a 9-day EMA; crossovers confirm volatility regime.
- VIX is mean-reverting and read as a risk gauge; Connors' VIX reversal systems fade VIX range expansion (buy S&P after a VIX spike). Treat as an idea to test; see testing.md.

## 4. Volatility filters
- High volatility at entry = high risk, worse return/risk; extreme low volatility = no direction, small frequent losses. Decide per system whether to ELIMINATE or DELAY: fast/short-term systems eliminate (many trades); slow trend systems delay (missing the big move is costly).
- Construct: fast and slow trend (10 and 60 days in the test); volatility = 20-day stdev (excluding today); enter on the close only if volatility is above the low threshold or below the high threshold; optional exit when volatility exceeds the high threshold and the day's move is favorable (profit-taking) or adverse. Thresholds expressed in standard deviations above average volatility (1 sd = top 16%, 2 = top 2.5%, 3 = top 0.13%; test beyond 3 because 20-day volatility jumps). Test across very different markets (Eurodollar, yen, crude, IBM, S&P; $15 per side; 1990-2011). The filter always removes good trades too; judge by improved profit factor/information ratio, not trade count.
- High-volatility EXIT for trend systems (30-year bonds 2000-2011): 40-day MA direction signals; exit when today's return exceeds 20-day volatility x factor (10 = only extreme moves); do not re-enter until the trend changes (slightly better) OR re-enter in the same direction once volatility falls to 1/4 of the exit-day return (considerably better: the shock is over). Matches pitfalls.md: after a shock, take the windfall or wait out the reversal.
- Appel mutual-fund ranking: choose funds with average-to-below-average volatility, rank by 3-month + 12-month performance, hold the top 10%.
- Summary: you cannot remove risk, only delay or move it; a system with "no risk" signals a development flaw.

## 5. Liquidity
- Backtests assume you can trade at any price printed; real volume is concentrated at the open/close (central body of the intraday volume curve) and thin at the day's extremes where a single trade may have printed. A countertrend system profits mostly at extremes where nothing could actually be executed; a trend system buying/selling breakouts at the extreme gets no profit there (first day is usually a loss). Haircut results from intraday/counter-trend systems for realistic fills (Ginter/Ritchie); see daytrading.md and testing.md live monitoring.

## 6. Noise and trend speed
- Noise has statistical attributes (not pure white noise): ~half of price moves reverse next day; ~25% continue 2 days, 12.5% 3 days; shock size also behaves like halving frequencies (50% small, 25% twice as large...). A move cannot be classified as noise vs trend until it continues; structural change (policy turn) is the only near-definite signal.
- Eurodollar (low noise) lets a simple breakout capture most of a move; EURUSD (more noise) enters/exits later; equity indices (extreme noise) enter and exit too late to net a profit. A small price change is probably noise; as the change grows, the chance of a true trend rises quickly, so longer trends are more reliable but suffer interim swings. Rule: trend period must exceed the market's noise scale; as markets mature and noise increases, use longer periods (smaller returns) or switch to mean reversion with short holds: noise dominates the short term, trends the long term.

## 7. Trends and interest-rate carry
- Rates near zero: a long trend position in rate futures still earns roll carry. Each quarterly roll moves from ~15 days to >= 105 days to expiry; the longer contract trades lower (discount or higher yield), so staying long through repeated rolls extracts carry. Accumulated carry can be significant even at low rates; check whether back-adjusted data includes it.

## 8. Expert systems, fuzzy logic, chaos, neural nets, genetic algorithms
- Expert system: if-then-else rule base (decision tree) collected by a knowledge engineer; transparent but only as good as the rules.
- Fuzzy logic: replaces hard thresholds (RSI > 70) with degrees of membership; smooths binary rule edges. Same overfitting rules apply.
- Fractal dimension and entropy: fractal dimension measures path roughness (see the efficiency ratio in foundations.md as the practical alternative); conditional entropy H(y|x) = -sum p(x) sum p(y|x) log2 p(y|x) measures how much a pattern x tells you about the next move y (lower H = more predictive in the author's table form; sample size per cell must be adequate: a cell with 1 observation means nothing).
- Neural networks: fewer layers/neurons/inputs = more robust; many elements fit past noise. Test on out-of-sample data; run several times with different random seeds. NNs "find the solution in a closed system," but markets are open systems, so no guarantee exists. Behavioral design idea: weight an economic report in only if it moves > 1.5 sd, otherwise 0.
- Genetic algorithms: fast search; may give a local peak; run ~10 times with different seeds and accept only if solutions agree; split data 60/40 or 50/50 and expect out-of-sample deterioration; count every GA run in the tests tally.
- Combined message with testing.md: more power means more overfitting risk; start general, add specificity in clear steps, and stop early.

## 9. Hedge-fund replication
- Regress a fund's returns on a set of tradable instruments to infer constant weights (Solver/regression); update daily or when tracking error exceeds a threshold (monthly rebalance gives large tracking error); tradeoff: tracking error vs cost. Claimed ~85% of hedge-fund returns replicated with ~15% tracking error, cheaper than fund-of-funds fees. Only works if the fund's positions are stable and sector exposures are tradeable.
