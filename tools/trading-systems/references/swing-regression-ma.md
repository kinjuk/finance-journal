# Swing charts, point-and-figure, regression, moving averages (Kaufman Ch. 5-7, distilled)

N-day breakout is in trend.md. Code for everything below: scripts/indicators.py.

## Contents
1. Swing charts (Ch. 5)
2. Point-and-figure (Ch. 5)
3. Time-series components and regression (Ch. 6)
4. Regression trading signals (Ch. 6)
5. Moving averages and smoothing (Ch. 7)
6. Choosing calculation periods

## 1. Swing charts
- Swing = sustained move of a pre-set size (the swing filter: cents/dollars or % of price). Event-driven (no time axis): nothing happens until a reversal exceeds the filter.
- Filter rules (8-step method): in an upswing extend the column on any higher high and ignore lows; if high is not higher, check swing_high - low >= filter -> start a new column down; mirror for downswings. Inside days ignored; outside day: pick one rule (continue the current direction) and apply it consistently. The 2-day Eng method needs only two bars to flip; require 3+ bars for lower sensitivity.
- Filter sizing: scale to the market's volatility (e.g. ~4% of price; 75 cents on an $18 stock), not a fixed value across markets (Dunnigan's lesson). A swing system signals when price exceeds the last swing high/low by the filter. Used as the building block for channels, trendlines and pattern recognition (Ch. 4).

## 2. Point-and-figure (P&F)
- Rules: simple, defined; ignores reversals below a minimum; no time factor (event-driven). Box size = minimum price move; reversal = number of boxes (standard 3-box); X columns = up, O columns = down; the swing chart is its time-less sibling.
- Rationale (De Villiers 1933): last price reflects all known information; informed intentions reveal themselves in later action. Signals: buy when an X column exceeds the prior X column top; sell when an O column falls below the prior O column bottom; compound formations (double/triple tops and bottoms, catapults) are the same breakouts with more confirmation.
- 45-degree trendlines from the first blank top or bottom box define the major trend; filter trades to the trendline direction.
- Thiel & Davis (1970, first futures P&F study): 3-box reversal, simple buy/sell formations, 799 signals, 53% profitable, avg net $311 over ~50 days. A decent historical benchmark, pre-costs and pre-modern markets.

## 3. Components of a time series; regression basics
- Price = trend + cycle + seasonal + random. Long trends tie to economic factors (rates, inflation, dollar); short trends (days/weeks) are investor behavior reacting to news flow. Cycles are slow because capacity decisions are slow; seasonality is a calendar-fixed cycle (crops, power demand, refinery shifts). Everything unexplained is random (ARIMA/Box-Jenkins later extracts shorter structure).
- Regression: Y = a + bX (a intercept, b slope). Explains the past relationship of two series; it does NOT forecast unless conditions remain the same (corn vs soybeans r2 = 0.83; Barrick vs gold only r2 = 0.26). Least squares always returns an answer; check validity.
- Correlation r (Pearson): +1/-1 perfect, 0 none. If r2 < ~0.20 the regression has no practical value. For arbitrage/pairs, cointegration matters more than correlation (Ch. 13).
- Curve fitting: curvilinear and exponential fit best statistically but extrapolate to absurd prices; the log fit fit worst yet gave the most realistic forecast. Common sense beats a better r2 when extrapolating. Re-estimate on a rolling window when macro factors change; consider multivariate regression for causal variables. Log scale makes returns and volatility look uniform.

## 4. Regression trading signals
- Forecast rule: n-day linear regression on closes gives F(t+1); buy when C(t+1) > F(t+1), sell short when < F(t+1). Many signals (line passes through the center of prices), so add confidence bands: 90% = 1.65 x stdev of residuals, 95% = 1.96 (use 2.0). Buy above F + 2R, sell below F - 2R, where R = stdev of residuals.
- Regression reacts to a direction change sooner than a moving average (which has a built-in lag that absorbs small reversals); bands set how much move is needed.
- Slope rule: buy when the n-day regression slope is positive, sell when negative (or when slope turns up/down). Slope needs no bands because long periods smooth. Competitive with other trend methods (see trend.md comparison). Performance improves as the calculation period lengthens.
- Slope alone can mislead: same slope in a smooth or a noisy rise. Add R (correlation of price vs sequential integers, signed): positive and high = consistent uptrend; negative = downtrend. Use R to rank trend quality; combine with slope.
- Chande Forecast Oscillator: 5-day regression residual as % of price: %F = 100 x (y - yhat)/y; buy when its 3-day average crosses above zero (the regression line), sell short when below. Assumes residuals trend.
- Market strength / ranking: index each series to 100 on the same date (essential when mixing futures and stocks), compute a rolling regression slope over the same period, and rank. Basis of market-neutral long-strong/short-weak (or the reverse) in Ch. 13. Strength rotates: each of four pharma stocks took turns strongest and weakest over a year.

## 5. Moving averages and smoothing
- Autoregressive trend-following measures current direction only (no confidence level); lag is the price paid for ignoring noise. Reducing lag costs noise rejection.
- Simple MA: MA_t = MA_(t-1) + (p_t - p_(t-n))/n. Each point matters 1/n. Drop-off effect = (p_t - p_(t-n))/n: an old large value leaving causes an abrupt jump; fixed-window methods (SMA, regression, weighted) share it; exponential smoothing minimizes it.
- Choose n by purpose: a 63-day MA = a quarter; 252 = a year (ignores seasonality); the stock market's 200-day is a benchmark but too slow for timing. A cycle the same length as the MA is cancelled; to see a monthly cycle use < half its length, to remove it use exactly its length; avoid MAs equal to an existing seasonal/cyclic period unless you intend to remove it.
- Match horizon to need: a buyer purchasing weekly wants a 5-day, not 6-month, average.
- Geometric MA: G_t = exp(average(ln p)); equals arithmetic for small ranges (56.20, 58.30, 57.15: 57.2166 vs 57.1871); matters only for long, wide-range histories (10 and 1000: 505 vs 100). Accumulative average depends on start date and loses sensitivity; reset accumulative average restarts at events or crop years.
- Exponential smoothing (EMA): E_t = E_(t-1) + a(p_t - E_(t-1)); start E_1 = p_1. Weights a, a^2... on past prices (front-loaded, memory never fully drops). Hutson conversion: a = 2/(n+1) for an n-day SMA equivalent, but it ignores lag, so the EMA is slower: 10% smoothing is slower than a 10-day MA, 5% slower than a 20-day. In a steady rise the 5-day SMA settles at a constant lag; the 20% EMA approaches that lag (0.95 of it in the book's 1-to-15 example) but never fully reaches it, and it changes direction one period after the SMA (4 prices after the peak vs 3). The SMA has no memory of earlier moves; the EMA does.
- Parameter spacing: equally spaced smoothing constants put half of the tests at <= 3-day equivalents (more sensitivity at the fast end). Equally spaced days gives very different constants. Kaufman: equally spaced smoothing constants is the BETTER test distribution; the constant-to-days relation is close to logarithmic, matching the percentage-step rule in testing.md.
- Lag correction: apply the same smoothing to the forecast error e_t = p_t - E_t to get ERR_t = ERR_(t-1) + a(e_t - ERR_(t-1)); adjusted trend EE_t = E_t + ERR_t; accept only if the error actually shrinks (more lead, more noise).
- Leads/lags in plotting: plotting MA_t ahead by k turns it into a k-day forecast; lagging a 10-day MA by 5 centers it on the data (phasing for cycles).

## 6. Choosing periods (cross-reference)
Test period lists as percentage steps (testing.md); make sure signals progress cleanly across adjacent periods (trend.md signal progression); measure noise first with the efficiency ratio (foundations.md).
