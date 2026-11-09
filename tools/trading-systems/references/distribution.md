# Price distribution systems (Kaufman Ch. 18, distilled)

Not distilled: the exact moving-skewness recursion (garbled in the extraction; use `rolling_moments` as a standard-moment substitute), Market Profile letter/TPO construction details and CTI participant tables, Bollinger-band chart walk-throughs. Code: `bollinger`, `jackson_zones`, `rolling_moments`, `kurtosis_skew_signals`, `value_area` in scripts/indicators.py.

## Contents
1. Measuring distribution
2. Zones
3. Long-term price distributions (what to correct before reading them)
4. Skewness and kurtosis as trend signals
5. Market Profile
6. Daily distribution as support/resistance

## 1. Measuring distribution
- Standard deviation is the most useful measure but breaks down with small samples and skew (annualized 20-day crude volatility hit 140% at end-2008; cannot exceed 100% on a downward move, but stdev reflected the upside). Frequency distribution (percent from each end) adapts to skew.
- Bollinger bands: 20-day SMA +- 2 stdevs of PRICES (not returns). Wider bands = fewer, more reliable signals with larger losses when wrong. Penetration is read either as confirmation of direction or as the setup for mean reversion. Main use: volatility description (narrow = low); compare 21- vs 65-day bands (monthly vs quarterly volatility). Lag: a rolling n-day stdev reflects today's volatility only 1/n, so bands widen slowly after shocks.

## 2. Zones
- Gould: divide the last 3 years' price range into five 20% zones; selling in the lowest zone and buying in the highest zone carry the greatest risk/least opportunity. Re-zone after structural moves.
- Jackson daily zones (floor traders) from yesterday's H, L, C: Average = (H+L+C)/3; High1 = 2 x Average - Low; High2 = Average + High1 - Low1; Low1 = 2 x Average - High; Low2 = Average - (High1 - Low1) (written in the text as Average + Low1 - High1... verify). Zones 1-6 from strongly down to strong up. S&P frequency by zone (20%, 44%, 83%, 79%, 42%, 20% as printed) shows the equity upward bias; these are era- and market-specific, so compute your own.
- Use: treat zones 3-5 as noise; sell the top of zone 4 / buy the bottom of zone 3 and exit near the average; stops in zone 5/2.

## 3. Long-term distributions: correct first
- Commodity prices cluster at low levels with a long right tail (supply responds to price). Remove factors that shift the level before reading the distribution: deflate by PPI/CPI and the US dollar index when prices are quoted in dollars (wheat: nominal 170% of 1985, real <90; nominal histogram had a left tail, dollar-adjusted had the classic right-tail shape). Structural changes (euro vs deutschemark, live vs lean hogs, gold/oil investment demand) break comparability: abnormal distributions mean the market is in an unusual period; short-term that is both opportunity and risk.
- Use MEDIAN, not mean (wheat mean 362.75 vs median 341.50; the position of the mean in the sorted list vs the median shows skew). Skew measure: SK = 3 x (mean - median)/stdev.
- A skewed price distribution makes stdev bands misleading (3 stdev to the left may be off the chart). Trend-following returns are strongly positively skewed (fat-tail wins, small losses), so stdev understates the upside; use drawdown-based measures (risk-sizing.md).
- Potential for big moves is greatest when: (1) a broad, erratic formation, no established range; (2) right-skewed, mode at the base, current price at the high end of the tail (unusual upside move underway); (3) left-skewed, mode in the upper half, price in the lower tail (a peak and decline). Prices near the long-term median/mode tend to move less.

## 4. Skewness and kurtosis signals
- Moving skewness (McNicholl) as a leading trend indicator: smooth closes (double-smoothed, a=0.1) to get a mean M; deviations DEV = close - M; moving stdev of DEV (b = 0.05); moving skewness G (c = 0.333). Largest spikes marked the start of the 2009 S&P uptrend; smaller spikes = minor turns. (Use `rolling_moments` for a rolling-window version.)
- Kurtosis (excess = kurtosis - 3): falling = orderly move/persistence (trade with the trend); rising = excessive move (fade). Skew sign gives direction of the tail.
- Trend rule: buy when excess kurtosis crosses BELOW 0, skew > 0 and ATR > minimum; sell when kurtosis crosses below 0, skew < 0, ATR > minimum.
- Mean-reversion rule: buy when excess kurtosis crosses ABOVE 0, skew < 0 and ATR > minimum; sell when kurtosis crosses above 0 (per the book, "below 0" printed for the sell: this is likely a typo for above), skew > 0 and ATR > minimum.
- Intraday version: 40-bar kurtosis (30-minute), 15-bar skew, 10-day ATR; stops 5 points beyond the 10-bar low/high (scale to market). Three variables only: kurtosis period, skew period, minimum volatility. Improvements: maximum volatility (mean reversion did better in high vol; trend entries should avoid high vol), exit when kurtosis moves the wrong way (cross zero or trend of kurtosis). Daily data is less noisy than 30-minute.

## 5. Market Profile (Steidlmayer)
- Time-at-price frequency distribution (TPO letters per 30-minute period) rather than volume; value area = range holding ~70% of the day's TPOs (or 2 stdevs per Jones: 42.5% each side of the center row); it is where buyers and sellers agree on fair value. Trading inside the prior value area = balance; above = buyer-initiated/seller-reactive; below = seller-initiated.
- CTI categories (CBOT): 1 locals, 2 commercial clearing members, 3 other members/commercials, 4 public; 1+2 are >65% of volume (locals small, short-term, contrarian, even up at the close). Participant data arrives after the close.
- Trends step through new value areas: a "price trend" (failed probe, within one TPO) vs a "value trend" (accepted: volume builds a new value area over longer periods). Trends retrace to the old consolidation area, widening the value area. Early trend warning: price leaves the value area or TPOs concentrate on one side. Advantage: usable on any market anytime (TPO count, not volume); disadvantage: interpretation is subjective and the objective rules are still developing.

## 6. Daily distribution as support/resistance
- Build the histogram of closes over the last ~6 months (50 bins min-max); the central cluster = middle 60% (20% off each end) or ~1.5 stdev (about 86%). Prices leaving the cluster signal a breakout earlier than a new n-day high/low (EuroStoxx 2011: 2735 matched the lows and flagged the break). One market, short period: a hypothesis, not a rule; test with out-of-sample (testing.md).
