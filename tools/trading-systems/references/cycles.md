# Cycle analysis (Kaufman Ch. 11, distilled)

Not distilled: trigonometric curve fitting and Fourier/spectral worked examples, Hilbert transform detail, MESA math (Ehlers' books cover it). Code: `triangular_ma`, `cycle_oscillator`, `cci` in scripts/indicators.py.

## Contents
1. Cycle components and when to believe a cycle
2. Isolating the cycle
3. Spectral methods (summary)
4. Cycle-based indicators and trading
5. Phasing (Hurst)
6. Cautions

## 1. Components and belief
- Price = trend + seasonality + cycle + noise (noise = everything unexplained). To see one component, remove the others: first differences remove trend; subtract a 1-year MA (or the value 12 months/252 days ago) to remove seasonality; what remains is cycle plus noise.
- Cycles can be sums of subcycles (harmonics: 1/2, 1/4... of the larger length); peaks/valleys are strongest when subcycles synchronize.
- Common reference: the 28-day lunar cycle = ~20 business days (4 weeks), the most widely watched period. Elections: Appel's election-year cycle (+10% election year, +4.5% year after, -1.25% two years before, +20% year before) is an example, treat as unverified.
- Before analyzing a market, confirm a dominant cycle exists AND know why (inventory holding, livestock breeding/feeding time, mining open/close lags, interest-rate policy, income expansion). Without a cause, assume spurious. Cattle example: 9-11 month cycle (1980-85), later peaks consistently 12 months apart (valleys less consistent). Cycle peaks vary by about one month, so use cycles as a long-term bias, not a precise timer.
- Long-term cycles are fundamental; short-term cycles are behavioral (see Ch. 15, patterns).

## 2. Isolating the cycle
- Simplest: subtract a 20-day MA from price, or use 20-day differences p_t - p_(t-20), to remove the trend.
- Oscillators (RSI, stochastic) show a cycle only if their period is <= half the cycle (<= 10 days for a 20-day cycle).
- Two-EMA detrend (Ehlers/Johnson): longer EMA = half the dominant cycle, shorter = half the longer; difference (MACD-like) removes trend with reduced lag.
- Triangular weighting: weights smallest at ends, largest in the middle (center weight 2.0; period P=10 drops the oldest value; weights 0.4,0.8,1.2,1.6,2.0,1.6,1.2,0.8,0.4); take the difference of two triangular averages (one half the length of the other); e.g. 63 days (a quarter, assuming earnings-related cycles). Very smooth and anticipates direction changes but acts like momentum: uneven spacing and varying amplitude.

## 3. Spectral methods (summary)
- Trig curve fitting and Fourier analysis need a computer; Fourier needs >= 256 points and >= 16 consistent cycles of 16 bars, which excludes short-term trading.
- MESA (Maximum Entropy Spectral Analysis, Ehlers) finds cycles in small data sets by making data look more stationary. Useful cycles exist only ~20% of the time; knowing when none exists is itself valuable (stay out of cycle trades then).
- Phase angle of a clean cycle rises steadily 0-360 degrees (sawtooth); when the sawtooth turns erratic, the cycle is breaking down. Ehlers bars by tick count; trend exists if smoothed price has not crossed the instantaneous trendline within the last half dominant cycle.

## 4. Cycle indicators and trading
- Cycle Channel Index (Lambert's CCI): x_t = (H+L+C)/3; CCI = (x_t - SMA_N(x)) / (0.015 x mean deviation_N). N < 1/4 cycle. Use a simple MA (fixed window matches cycle phase), not an EMA (residual old data). Scaling puts 70-80% of values within +-100: > +100 = cyclic turn up, < -100 = turn down. Choose N as short as possible while keeping the mean deviation a stable noise estimate.
- Short Cycle Indicator (Lorca-Susino): fast (8) and slow (20) EMA, squared convergence term scaled by the slow-period lowest high / highest low (a stochastic form); expanding volatility conditions trigger sells. Intraday, multi-time-frame. Complex and lightly validated here; treat as an idea, not a rule.

## 5. Hurst phasing (simplified procedure)
Idea: a centered moving average sits at t - n/2; "phasing" plots it that far back so its tops/bottoms align with price's, and measures oscillation about the trend-cycle line.
1. Choose full span F = average distance between price tops; half span H = F/2. Plot each MA at t - span/2 (phased).
2. Record crossings of the two phased averages, regress the crossing points for the trend line YT.
3. Project the half-span from its extreme since the last crossing to its latest value (straight line Yc); intersect with YT for the projected crossing; D = distance from the extreme to the crossing; price objective = D beyond the crossing (equidistant on the other side).
4. Update daily until the actual crossing, then fix D.
5. Rules: long when the half-span MA turns up (cover shorts regardless of objective), short when it turns down; exit at the price objective, set 10% of the full cycle height closer for error.

## 6. Cautions
- Cycles drift in length and amplitude; peak-to-valley spacing is not even. Treat cycle signals as timing within a trend/seasonal bias.
- Always demand a causal story and out-of-sample persistence (testing.md). Fourier/MESA on short noisy data finds cycles in random series.
