# Risk, leverage, position sizing, stops, ruin (Kaufman Ch. 23, distilled)

Ch. 23 is now fully covered except the binomial/chi-square tables (see section 11 for the usable rules). Code: `var_historical`, `var_variance_covariance`, `adx`, `commodity_selection_index`, `optimal_f`, `kelly_fraction`, `prob_losing_streak` in scripts/indicators.py and scripts/metrics.py.

## Contents
1. Choosing between systems
2. Return/risk measures (formulas; script: scripts/metrics.py)
3. Leverage and target volatility
4. Position sizing
5. Stops and profit targets
6. Probability of ruin
7. Value at Risk (VaR)
8. Ranking markets for selection
9. Entering, averaging in, pyramiding
10. Equity-curve trading and reserves
11. Optimal f, Kelly, and 'is the model broken?'

## 1. Choosing between systems
Prefer: larger profits (room for execution error); upward equity surges over downward; shorter time to recovery; less time in market (avoids shocks). ALWAYS compare against a benchmark (e.g. 60% S&P / 40% Treasury). Real trading results show bigger equity swings than hypothetical ones; hypothetical is always optimistic. Monthly-return ratios look better than daily because they are smoothed; compare like with like.

## 2. Measures
- Sharpe = (E - I) / sigma (annualized return, risk-free, annualized vol). Information ratio = same without I (use I whenever interest income on idle capital is embedded in returns).
  Weakness: cannot distinguish consecutive losses from alternating losses, or profit surges from loss surges.
- Treynor = (AROR - I) / beta vs benchmark.
- Average Maximum Retracement (Schwager) = mean of (prior peak equity - current equity) over days not at new highs. Semivariance-like; fixes std dev symmetry bias.
- Max drawdown / Calmar = AROR / max peak-to-valley drawdown. Practical and honest, but the historic max DD is understated by overfit or shock-avoidance; the future brings larger drawdowns. Rule of thumb from the book: with monthly sigma 10% a 15% monthly loss has ~2.5% chance, i.e. likely within ~40 months.
- Sortino = (AROR - MAR) / stdev of the non-zero drawdown excursions (peak equity - equity). MAR can be the risk-free rate.
- Ulcer Index = sqrt(mean(D_i^2)), D = drawdown from highest equity to date (0 on new highs). Rises with anxiety; penalizes depth and duration.
- Also track: time to recovery, % time in market, stability of returns.
Use scripts/metrics.py `report()` to compute all of these from a returns series.

## 3. Leverage and target volatility
- Leverage magnifies both ways; futures margin is ~5-10% so exposure, not margin, is the real risk. Margin is not volatility-adjusted and changes slowly. Capital far above margin means effective leverage is much lower (e.g. $50k on 1 gold contract ~3:1, not 10:1).
- Targeting volatility (standard CTA practice):
  1. Record daily P/L of the strategy at fixed size.
  2. Compute annualized stdev of that P/L (dollars).
  3. Choose target annualized volatility (typically ~15%; aggressive).
  4. Required capital = annualized stdev($) / target vol. If actual capital is larger, positions can be scaled up; if smaller, scale all positions down by the ratio.
  Check: stdev of resulting returns should land at the target.
- Sanity check on target: with 15% vol, 2-2.5 sigma losses (~37%) happen; with a hard max-drawdown limit of 50% that is the edge. If you can only accept 10% max loss, the target vol is ~3% (a fifth).
- Reserves: unused equity needed to keep trading at target vol through losses. Define a maximum-loss liquidation level in advance (often 50%, as low as 10%).
- Scaling to personal risk: halve leverage to halve both risk and expected return. Never choose leverage from the best backtest.

## 4. Position sizing
- Equal-dollar sizing gives unequal risk (low-priced volatile stocks dominate). Three stock methods compared: (1) $ / price; (2) $ / (price x 100 x annualized vol); (3) $ / (ATR x 252-based). They give wildly different allocations; ATR/true-range is considered the better risk measure, but TEST each across many instruments and compare average information ratio.
- When using methods 2/3, pool total money and rescale so total exposure equals available capital.
- Volatility-based sizing equalizes each trade's chance to matter, cuts portfolio vol swing (6% to 25% unmanaged in one 3-year span), and reduced BAC test volatility by ~27%. Size shrinks in volatile periods (e.g. 6000 -> 1000 shares); for a rigorous test define capital as the maximum ever needed.
- Equal risk per trade is the conservative default unless you can rank trades by quality.

## 5. Stops and profit targets
- Entry is the point of greatest uncertainty. Style matters: trend systems already take small losses (stop may add nothing); breakout loss = size of range; mean-reversion NEEDS to hold losers (high win %), tight stops cut win rate and break the system. Test; do not assume stops help.
- Trailing stop types: fixed % from high close; volatility-based (ATR, annualized vol; adapts but can widen); % of open profit (only after a trigger profit; use closer of the volatility and profit stops); standard-deviation stop (Kase Dev-stop). Volatility-adaptive and trailing beat fixed-dollar and initial stops in the book's tests.
- Kaufman's test: 30-year bonds 2000-2011, MA 10-100 days x SD-stop factor 2-10 (40-day): nearly every stop version beat no-stop, i.e. robust. Caveat: one market, one period, trending market (equity indices are noisier).
- Noise: for random prices, (frequency of stop hits) x (distance) is constant, so tight stops just trade many small losses. Real data: filtering noise leaves larger, more meaningful moves.
- Stops fail when needed most (gaps/shocks fill at the worst price), like correlation in a crisis. Proximity risk: clustered stops of trend followers. Large funds may take ~3 days to enter.
- Stops on closing prices avoid noise exits; profit-taking is the opposite (take the intraday spike).

## 6. Probability of ruin
- Equal win/loss (gambling): R = ((1 - A)/(1 + A))^c, A = P - (1 - P), c = capital in units. 60% win rate, c=1 -> R=33%, c=2 -> 11%.
- Trading (unequal win/loss): Kaufman/Vince approximation, implemented in scripts/metrics.py `risk_of_ruin()`:
  Z = pW*avgWin% - pL*avgLoss%; A = sqrt((pW*avgWin%)^2 + (pL*avgLoss%)^2); P = 0.5*(1 + Z/A); R = ((1-P)/P)^(MaxRisk/A).
  Book example: $10k, avg win $400, avg loss $200, 40%/60%, max loss 25% -> R < 1%. Halve capital -> 7.9% / 28.1% (ruin rises faster than capital falls). Cut avg win to $325 and max risk to 15% -> 38.3%.
- Lesson: small edge + small capital + tight loss cap = high ruin probability; capitalization is part of the strategy.


## 7. Value at Risk (VaR)
- VaR = loss you do not expect to exceed over a horizon at a confidence level, using historical risk; a daily positional limit, e.g. a bank with a 0.5%-of-commitments daily loss rule must cut positions the same day if VaR exceeds it. Inputs: position sizes, volatilities, cross-correlations, horizon, confidence level (1.65 sd = 95%, 2.33 = 99%).
- Variance-covariance (1 day): VaR = sqrt(s1^2 + s2^2 + 2 r12 s1 s2) where s_i = (position value x daily stdev x 1.65). Example: EURUSD EUR 1m (value $1.25m, sd 0.565% -> $11,650) + Eurobund (sd 0.605% -> $12,475), correlation -0.27 -> by the formula VaR = $14,590, below the $24,125 plain sum because of offsetting positions. NOTE: the book prints $17,068, which does not match its own formula (that number is what you get with the correlation term dropped, i.e. rho = 0); trust the formula. Horizon P days: scale by sqrt(P). Annualized vol s = sqrt(252) x stdev(daily % changes).
- Generalized: probability of loss L over T years: N[(ln(1+L) - mu T)/(sigma sqrt(T))]; VaR = -(exp(mu T - Z sigma sqrt(T)) - 1) x W.
- Historical (simplest, recommended): apply today's positions to the last k = 252 days of returns, R_i = sum w_j r_ji (convert to one currency), take mean and stdev of R, VaR = R_mean - 2.33 s (99%); VaR is a negative number. Monte Carlo is the third method.
- VaR fails when needed most (extreme correlated moves: 2008); stress-test with price shocks and simulated 2-3 sd moves across all sectors with correlation ~1. Real return distributions have kurtosis up to ~25 (normal = 3); there is no simple fix; treat extremes as exceptions with a crisis plan (pitfalls.md). Hindenburg Omen type signals are folklore, not tested rules.

## 8. Ranking markets for selection
- Match the ranking to the system: if 20-day r^2 ranks trend strength, trade the top markets with regression-slope trend following (period <= 20); low correlation favors mean reversion. Candidate measures over 5/10/20/40 days: correlation coefficient (only > 0.25), net moves over n, 2n, 4n, regression slope in $/day, ADX (> 0.20), average absolute price change (higher volatility = more profit and more risk). Smooth the last 3 days if erratic.
- Wilder's Directional Movement: PDM = H_t - H_(t-1), MDM = L_(t-1) - L_t (the book prints the sign convention loosely; only the larger positive outside-day move counts, the other is zero; inside day = 0); TR = max(H-L, H-C_prev, C_prev-L). 14-day sums by average-off: X14_t = X14_(t-1) - X14_(t-1)/14 + X_t (or 0.071 constant). PDI = PDM14/TR14, MDI = MDM14/TR14, DX = 100 x |PDI - MDI|/(PDI + MDI); ADX = ADX_(t-1) + 0.133 (DX - ADX_(t-1)); ADXR = (ADX_t + ADX_(t-14))/2. Ruggiero's reading: ADX crossing above 25 = trending; below 20 = consolidating; falling through 45 from higher = consolidating; the distance ADX vs ADXR gauges the extent of the trend.
- Commodity Selection Index: CSI = ADXR x ATR14 x K, K = 100 x (V / sqrt(M)) x 1/(150 + C); V = value of a 1-cent move, M = margin, C = commission (the extraction lost the radical on M; Wilder's original uses the square root, so verify against the source before relying on absolute values). For stocks V = 1 and M = share value. K is constant per market. Rank markets and choose the highest CSI or allocate in proportion.
- Kaufman's strategy selection: efficiency ratio ER (65-day average) vs profit factor of a 65-day MA system across many markets 1990-2011: profit factor rises with ER (less noise). Use ER to decide trend vs mean reversion by market (foundations.md); a long window compresses the ER range, which is fine.

## 9. Entering, averaging in, pyramiding
- Entry choices on a signal: all at once; average in; wait for a better price.
- Averaging in (80-day MA, 30-year bonds, e-mini S&P, gold, 1990-2011; 5 contracts, spaced 1-5 days apart over 5-21 days): results improved with spacing; best around 2 days in bonds (trending), kept improving in the noisy S&P (negative to positive), stabilized after ~2 days in gold. Cost-benefit: if the trend reverses before the full position is on, the loss is smaller; if price runs, the average entry is worse. Spacing must scale with the trend speed/holding period (a 10-day MA cannot take 21 days to enter). Averaging in removes single-entry uncertainty.
- Waiting for a better price (or a timing oscillator): helps average entry but misses some of the biggest moves; fallback: enter at the close of day 5 if no better price came (timeframes.md first-oversold logic).
- Compounding (pyramiding): add when the trade is confirmed (sustained base, expected further profit, clear risk level) rather than "averaging down." Shapes: pyramid (smaller adds), equal adds (inverted pyramid, maximum leverage, fragile and top-heavy), reflecting pyramid (add then remove). The largest position sits at the worst price, so losses land on a bigger base when the market reverses; never lever up with all available funds. Adding on new high profits (60-day MA, AAPL/AMZN/TY/ES): highest total profit was the plain single unit for Apple; additions raise leverage but not necessarily profit factor; averaging down (adds on new losses) gives better entry prices but may miss the move and fights the trend-following premise.
- Reserve adequate funds for the full intended size before building it.

## 10. Equity trends and reserves
- Growing size with equity at the top of a trend cycle means losses hit a larger base: a 100% gain then 50% loss cycle twice a year nets zero ($10,000 stays $10,000). Holding size constant while profits accumulate as reserves, then re-splitting equity into margin and reserve (e.g. 40/60) after the drawdown stabilizes, enters the next profit phase with a larger base (gradual growth). Rule: raise exposure after a drawdown has stabilized, not at the peak.
- Trading the equity curve (exit when a moving average of cumulative P&L turns down; 10- and 60-day average on an 80-day MA system): inconsistent: better for S&P and gold, much worse for bonds (the most trending market), no switching costs included, poor expectation on a diversified portfolio. Do not adopt without testing.

## 11. Optimal f, Kelly, and "is the model broken?"
- Gain needed to recover a loss = 1/(1 - loss) - 1 (50% loss needs 100%).
- Kelly: G(f) = P ln(1 + B f) + (1 - P) ln(1 - f), B = avg win/avg loss. Equivalent f = (p (PLR + 1) - 1)/PLR. Vince optimal f = the fraction of the largest historical loss that maximizes the geometric mean of per-trade growth: maximize prod(1 + f x (-R_i)/largest loss)^(1/n) over f in 0.01..1.0. Example p = 0.5, PLR = 2 -> f = 25%; after three consecutive losses equity is down 57.8% (not 75%) because each bet is a fraction of current equity.
- Caveats (A. Elder): optimal f changes with every trade and is estimated from history (largest loss will be exceeded); betting MORE than optimal leads to eventual ruin, less than optimal lowers risk arithmetically but profit geometrically. Practical stance: use a fraction of optimal f (half or less), and size by volatility (section 3).
- Comparing expected vs actual: if a trend system expects ~33% winners with a 4:1 win/loss ratio and the first 10 trades all lose, use the binomial: probability of l losses in n trades with loss probability p = C(n,l) p^l (1-p)^(n-l); ten straight losses at p = 0.67 is 1.8% (0.67^10), so it is unusual but possible within the profile; use the Chapter 21 drawdown test (testing.md) before declaring the system failed. Probability of a run of n same-outcome events ~ (1/2)^(n+2) for a fair coin.
