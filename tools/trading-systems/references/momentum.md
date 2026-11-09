# Momentum and oscillators (Kaufman Ch. 9, distilled)

Not distilled: Williams %R/other minor oscillators, double-smoothed variants beyond TSI, the full Directional Parabolic details (see Ch. 17/23), per-market figures. Code: scripts/indicators.py (momentum, rsi, cmo, macd, stochastic, tsi).

## Contents
1. Momentum definition and properties
2. Trading extremes (mean reversion) vs high momentum (trend)
3. Oscillator formulas
4. RSI variants and evidence
5. Double-smoothed momentum (TSI)
6. Velocity and acceleration
7. Divergence
8. Hybrids and practical rules

## 1. Momentum
- Momentum M(n)_t = p_t - p_(t-n) (change over n days). Always state n. Speed = M/n (5-day change 100 -> speed 20; 10-day -> 10). Many sources call this ROC. "Oscillator" in the book = momentum normalized to +-1 or 0-100.
- Momentum is NOT volatility: gold 1200 -> 1250 -> 1200 over 5 days has zero momentum, high volatility. Range scales with price level, so fixed thresholds drift; normalize.
- Smoothing/lead: momentum has no moving-average lag. Fast momentum peaks BEFORE price (leads), slow momentum peaks with price. In a perfectly smooth cycle momentum would be a perfect leading indicator; real prices are irregular so it is not. Flat price slope at constant $1/day makes momentum plateau.
- Normalize: divide by the max possible over the same window (e.g. n-day range) so the value self-adjusts to price and volatility (Amazon $34 with a $3.79 10-day range vs $191 with a $16.63 range: a $2 move and an $8.77 move are both 0.52).

## 2. How to trade momentum
- Mean reversion (fading extremes): enter against the move when the oscillator is at an extreme; exit when momentum returns to ~zero (momentum cannot swing extreme to extreme on command; extremes revert to neutral). Taking profit short of zero (5-10% beyond) raises win rate and lowers average win; target past zero raises size. Fails when a sustained trend outlasts the calculation window (price still higher when momentum hits zero). ALL momentum entries against price are high risk; fast calculation periods flip between overbought/oversold unstably.
- High-momentum trading: trade in the direction of the move when momentum exceeds a high threshold, instead of anticipating a reversal (professionals' approach; fast, full-time execution).
- Best use: timing tool inside a conservative trend strategy. Tune the period so extremes occur often enough. Example: trend trades held ~20 days, willing to wait 2 days for entry -> build a 3-period oscillator on daily bars (or 10-period on hourly); it should give 1-2 oversold signals per 2-day wait; buy dips, not rallies. Non-extreme values carry little information.
- Rule of thumb for stops: mean-reversion without stop only if testing shows it holds (see risk-sizing.md); momentum fades have occasional very large losses.

## 3. Oscillator formulas
- Normalized oscillator = momentum / max over the same rolling window.
- RSI (Wilder) = 100 - 100/(1+RS), RS = AU/AD (sum of up changes / sum of down changes over n=14; down as positives). Update with average-off: AU_t = AU_(t-1) - AU_(t-1)/n + max(p_t - p_(t-1), 0); AD likewise with downward moves. Thresholds 30/70 (n=14 = half a one-month cycle).
- Net momentum oscillator (Chande CMO) = 100 x (Su - Sd)/(Su + Sd); more extremes than RSI because less smoothing.
- MACD (Appel): fast EMA minus slow EMA (12/26 default; book example 20/40 with a = 2/(n+1): 0.0476, 0.0243), signal = 9-day EMA of MACD (a = 0.10), histogram = MACD - signal; above zero confirms uptrend. Smoother than same-period momentum, peaks near the same place, leads the moving averages in turns. Also an RSI of the MA spread (5-day RSI of 10-week minus 40-week MA on e-mini S&P).
- Stochastic (Lane): %K = 100 x (C - L_n)/R_n with L_n = lowest low and R_n = highest high minus lowest low over n days; %D = 3-day average of %K; %D-slow = 3-day average of %D. Uses high/low/close, no built-in lag; premise: closes resist penetrating prior highs/lows, and near turns the close settles toward the day's low despite new highs.

## 4. RSI variants and evidence
- Wilder's 14-day RSI: >14-day sustained move pins the RSI near an extreme and then it goes sideways. Aan study: average 14-day RSI tops and bottoms cluster ~72 and ~32; 50% of values between 32 and 72 (~0.675 sigma), so 30/70 are NOT selective. Use ~1.5 sigma-equivalent bands (about 80/20 on 10 days) for fewer, higher-quality trades. Too many trades -> longer period and wider bands.
- Smoother RSI: replace each 1-day change with an n-day change (2-day RSI = p_t - p_(t-2)).
- RSI(2) (Stokes, MarketSci): buy next close when 2-day RSI crosses below 10, sell short when above 90, exit one day later. S&P 1970-98: 90+ kept going up (trend behavior); after ~1998 it is a mean-reverting indicator, both longs and shorts profitable 2000-08. Scaling in by RSI depth (buy 50% at 14, add at 8) tested. WARNING: a regime flip in the same indicator, and 1-day trades are cost-sensitive; verify net per share/contract after costs. Waiting for RSI to cross 50 to exit does not work (it can sit on one side for long).
- Quick-move variant: act when RSI_t - RSI_(t-k) exceeds a threshold; exit near zero or after n days.

## 5. Double-smoothed momentum (Blau TSI)
- TSI(r,s) = 100 x EMA(EMA(c_t - c_(t-1), r), s) / EMA(EMA(|c_t - c_(t-1)|, r), s). First differences are smoothed twice (a = 2/(n+1)), giving a smooth index with surprisingly little lag; denominator uses absolute values so |TSI| <= 100.

## 6. Velocity and acceleration
- Velocity = slope = momentum / n (average); instantaneous velocity needs the derivative (a limit of shorter intervals; use short momentum or regression slope as the practical proxy). Acceleration = change in velocity (change in slope): positive velocity with falling acceleration warns of exhaustion; use as an early exit or filter, noisy at short horizons.

## 7. Divergence
- Bearish: price makes a higher high while the oscillator makes a lower high (bullish mirror at lows). Failure swing = unsuccessful test of a recent RSI extreme.
- Longer-span divergences (months) forecast larger reversals than hourly ones. Best when the oscillator started from an extreme and is still well away from its midpoint (50 or 0) when the signal fires, so a correction can occur before neutral.
- Procedure: find the swing highs (or lows) in price, connect; find the matching peaks in MACD, connect; opposite slopes = divergence. MACD rules: sell when the MACD line crosses below its signal after the second (divergent) peak; exit at MACD = 0 or a formation-based objective; optionally wait for the MACD to recross the signal.
- General rules: enter when the divergence is identified unless the correction target is already reached; neutral momentum is the normal profit target. Waiting for a very clear divergence is often too late; anticipation entries (earlier) trade more risk.
- Divergence uses subjective peak selection: code the swing definition explicitly before testing (swing_chart or pivot_points in indicators.py).

## 8. Hybrids and practical rules
- Directional Parabolic System (Wilder): ADX direction filters Parabolic SAR trades (only longs when ADX up, only shorts when down; no trade if they conflict); in a position use the parabolic stop (DPS); ADX exceeding +DM/-DM and reversing closes the position (leading exit only; the reversal needs the parabolic penetration). Oscillator exits give better prices than trend exits when right, but give back when the trend resumes. (Directional Movement is detailed in Ch. 23; Parabolic in Ch. 17.)
- Final caution from the book: momentum indicators are most useful as timing within another strategy; small calculation periods are unstable; contrary entries carry high risk.
