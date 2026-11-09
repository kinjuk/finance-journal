# Adaptive techniques (Kaufman Ch. 17, distilled)

Code: `kama`, `parabolic_sar`, `mcginley`, `adaptive_stochastic`, `trend_adjusted_oscillator`, `variable_ma` in scripts/indicators.py. (Known caveat from the author: adaptation "may work better than a static period but is far from the final solution.")

## Contents
1. Premise and caveat
2. KAMA
3. Making momentum adaptive
4. McGinley dynamic, Parabolic SAR
5. Trend-adjusted oscillator
6. Adaptive intraday breakout (Meyers)
7. Adaptive process (periodic retest) and variable-speed MA
8. When to use adaptive methods

## 1. Premise
- Use a slower trend when the market is noisy/sideways/low-volatility and a faster one when moves are clean. Identifying a sideways market is hard (price can be unchanged over 5 days yet swing violently). Adaptation improves basic trend calculations but does not solve everything.
- Replacing fixed values ($500 stop, 50-point breakout) with volatility-based ones is the simplest adaptation (also see risk-sizing.md); fully adaptive methods let core parameters vary with price level, volatility or pattern.

## 2. KAMA (Kaufman's Adaptive Moving Average)
- KAMA_t = KAMA_(t-1) + sc_t x (p_t - KAMA_(t-1)); sc_t = [ER_t x (fastest - slowest) + slowest]^2; fastest = 2/(fast period + 1), slowest = 2/(slow period + 1); nominal periods 2 and 30.
- ER_t (efficiency ratio) = |p_t - p_(t-n)| / sum |p_i - p_(i-1)| over n (typically 10). ER = 1: all moves one direction (fast); ER -> 0: noisy (slow). Squaring makes the slow end very unresponsive (30x30 = a 900-period trend), freezing the line in noise, while a clean run can reach a ~4-period equivalent speed. It is an exponential smoother, not a moving average.
- Trade as any trendline (direction or price penetration); see trend.md for signal rules. Same ER measure as the noise test in foundations.md.

## 3. Adaptive momentum
- Convert any bounded indicator M to a smoothing constant: 0..1: sc = M; -1..+1: sc = |M|; 0..100: sc = M/100; -100..+100: sc = |M/100| (0 = less trend, 1 = more trend). Adaptive RSI is more sensitive than KAMA; square sc to slow it (0.75 -> 0.56).
- Adaptive stochastic: look-back per = int(slowend - ER x (slowend - fastend)) (ER from the same period, e.g. 10); raw = 100 x (close - lowest(low, per))/(highest(high, per) - lowest(low, per)); K-slow = 3-day average of raw.

## 4. McGinley Dynamic and Parabolic SAR
- McGinley: MD_t = MD_(t-1) + (p_t - MD_(t-1)) / (k x n x (p_t/MD_(t-1))^4)? NOTE: the book prints the denominator as k x n x (p_t / MD_(t-1)) with k = 0.60 and n the MA period; (the common published form raises the ratio to the 4th power). Implement the book's form and verify against a reference before trusting it.
- Parabolic Time/Price (Wilder): always in the market; stop-and-reverse (SAR) trails price faster as the trade advances. SAR_t = SAR_(t-1) + AF_t x (extreme - SAR_(t-1)) where extreme = highest high since entry (long) or lowest low (short); AF starts at 0.02 and increases by 0.02 on each new extreme up to 0.20 (equivalent to a 99-day average accelerating to ~9 days). Long: SAR may never exceed today's or yesterday's low; short: never below today's or yesterday's high; reverse on penetration. Starting SAR = lowest low (long) / highest high (short) of the prior move. Idea: time is the enemy; a trade must keep making profit. Weak point: AF always restarts at 0.02 even when the market is fast. Works well in short consistent trends, whipsaws in ranges.

## 5. Trend-adjusted oscillator (TAO, Wall)
- Problem: oscillators cluster in the lower half in downtrends and upper half in uptrends, giving false countertrend signals. Fix: O_t = average over n of (close - low)/(high - low) (as % scale), MAO_t = n-day average of O; TAO_t = midpoint - (MAO_t - O_t) with midpoint 50 (or 0 for +-100 scales). Re-centers the oscillator; gold example: at the May 2011 peak TAO was ~50 (neutral), not overbought. Cost: loses some extreme readings; takes weeks to re-adjust.

## 6. Adaptive intraday breakout (Meyers)
- Idea: expected n-bar range scales with sqrt(n) (price-volatility relationship). HR_t = H_t - L_(t-n); LR_t = L_t - H_(t-n) (single bars n ago, not extremes); normalize NHR = HR/(n^a)/ATR(n), NLR likewise; HRmax = highest(NHR, n), LRmax = highest(NLR, n). Buy when HRmax > threshold_high and LRmax < threshold_low; sell on the reverse; flat 5 minutes before the close. Four optimized variables (n <= 25, a, two thresholds): QQQ n=6, a=0.75, thresholds 0.50 and 1.05, ~1 trade/day. High overfitting risk: demand a long, consistent test (testing.md).

## 7. Adaptive PROCESS and variable-speed MA
- Process version: retest on recent data periodically (fixed window, or restart after a regime change/price shock). The faster you react, the less data you have, so decisions are less dependable (see walk-forward, testing.md).
- Variable-length MA (Arrington): choose min/max period (e.g. 5 and 30); compute mean and stdev s of price changes over a fixed window (>= 10 days, ideally the max period); define thresholds in stdevs (low volatility inside mean +- 0.25s -> longest period; high volatility outside +- 1.75s -> shortest); n_t = (max - min) x (|change_t|/s - 0.25)/(1.75 - 0.25) + min, clipped to [min, max]. (As printed, the formula uses the day's change over s; larger moves shorten the period.)

## 8. When to use
- Adaptive features conflict with the "simple fixed rule over a long test" ideal and are only supported by the improvement in the whole-period performance profile; at extreme volatility there are few observations so the sliding scale is unproven there. Prefer adaptation tied to a clear premise (noise measure ER, volatility) over adding free parameters, and count each adaptive parameter in the overfitting tally.
