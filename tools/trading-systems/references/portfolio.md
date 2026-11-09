# Diversification and portfolio allocation (Kaufman Ch. 24, distilled)

Not distilled: the genetic-algorithm portfolio solver (GASP) internals, spreadsheet Solver walkthrough, matrix/statistical-table appendices. Read the source if needed.

## Contents
1. What diversification can and cannot do
2. Levels of diversification
3. Balanced (equal) risk
4. Portfolio model types
5. Why classic mean-variance fails for trading returns
6. Objective function
7. Volatility stabilization, switching costs, exposure caps

## 1. Limits of diversification
- Systematic (diversifiable) vs market risk (shocks, catastrophic; not diversifiable). In stress, correlations go to 1 (2008: gold and the euro went to -0.6 vs the S&P, i.e. everything liquidated at once). Rolling/short-window correlation shows this; one long-period average hides it.
- The three defenses against shock risk: be out of the market as much as possible; cap portfolio leverage; use genuinely uncorrelated strategies. Statistics that behave in normal times (correlation, VaR) go to extremes in shocks.
- Financial markets (rates, FX, indices) share fundamental links and react predictably to the same data (strong GDP: bonds down, dollar up, stocks up unless rate-sensitive). Weak dollar lifts oil, gold, grains. Equity sectors all respond to the same macro conditions. Diversify across groups: fixed income, currencies, equity indices, energy, metals, grains, livestock, softs.

## 2. Levels
Choose a broad market set with one approach, several strategies on one product, or many systems on many markets. Risk falls fast with the first few uncorrelated assets then flattens (diminishing returns; ideal case approaches a floor around half of single-asset risk).
Strategies that are functionally different (less correlated): trend following, countertrend/mean reversion, spreads (pairs, intercommodity, arbitrage), fundamental/value, carry. MA, ARIMA and point-and-figure are the SAME trade (all trend): do not count them as diversification. Different strategies may hold opposite positions in one market, which reduces risk.

## 3. Balanced risk
Three ways: equal dollars, equal annualized standard deviation, equal ATR. Equal dollars is rarely used (low-priced volatile names dominate). ATR is best when H/L/C are available; use annualized stdev of closes otherwise. Example: BAC (low price) had twice the volatility of MSFT/AAPL, so equal-dollar overweights it. Allocation proportional to 1/volatility (vol 4% vs 1% -> 20%/80%). Make total invested value match capital after rescaling.

## 4. Portfolio model types (Narang)
- Equal-dollar: assumes forecasting winners is unreliable; concentrates risk.
- Equal-risk: volatility or drawdown based; gives each trade an equal chance to matter.
- Alpha-driven: rank assets by expected alpha and give the top larger allocations (rank-based to avoid distortion, but chases past winners).
- Decision tree: map each asset to strategy and risk level; dynamic if desired.
- Mean-variance optimization (Markowitz): volatility + correlation -> optimal allocation.

## 5. Why classic mean-variance breaks for TRADING returns
- Use the daily returns of the TRADING in each market, not price returns: two rising stocks look positively correlated in price, but a system long one and short the other has negative correlation in its returns.
- Standard deviation distortion: a system in the market 50% of days has half the stdev of a passive hold (zero-return days), so the optimizer sizes it up; on days when both are in, risk is higher than intended. Same issue corrupts covariance with intermittent returns. Fix: size by risk while in the market, or optimize on a drawdown-based risk measure.

## 6. Objective function
Information ratio = annualized return / annualized risk, but choose the risk measure deliberately:
- Annualized volatility (stdev x sqrt(252) or sqrt(12)); daily-to-annual scaling can be inaccurate.
- Residuals of a linear fit to the equity curve: penalizes big gains as well as losses and forces a straight line.
- Semivariance of daily drawdowns (preferred): only non-new-high days count; no penalty on profit patterns; no annualizing. Kaufman's GASP objective: OF = AROR / stdev(drawdown from high equity). (metrics.py computes the drawdown series; use that.)
- Add constraints (max weight per asset/group) to prevent concentration and to constrain diversification. A genetic algorithm can search allocations when Solver fails (non-smooth objective); verify the global maximum with several seeds.

## 7. Volatility stabilization and exposure cap
- A fixed ratio of target vol / long-run vol is hindsight-dependent. Use rolling annualized volatility (e.g. 10-day) and scale positions by a LAGGED volatility factor VF = target vol / rolling vol. In Kaufman's 17-year mixed portfolio, raw vol ranged 1.5%-25.5% (8.5% avg); stabilizing improved the information ratio from 1.27 to 1.38 and gave a more uniform risk path (realized 13.7% vs 12% target, because the factor is lagged and vol trended up).
- Stabilization only sees historic vol; keep a forward-looking control (VaR, leverage cap) as well.
- Switching costs: each change in VF changes positions. Use a longer volatility window and/or a threshold (e.g. no resize unless vol moves 20%). Test the combination.
- Exposure cap (UCITS-style example: total exposure <= 2.5x equity; commodities <= 20% of equity). Exposure = face value (shares x price; contracts x big-point value; short rates adjusted). Apply the cap LAST, after all other scalings: if exposure E exceeds cap C, scale ALL positions (including new ones) by C/E to preserve balance. Expected to cost little information ratio since high leverage coincides with low volatility and no direction.
