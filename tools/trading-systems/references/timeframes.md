# Multiple time frames (Kaufman Ch. 19, distilled)

Not distilled: Pring's full set of ROC interpretation examples, Krausz's Fibonacci/Gann geometry (see behavioral.md for the status of that material). Code: `elder_ray`, `kst`, `force_index`, `stochastic` in scripts/indicators.py.

## Contents
1. Why combine frames
2. Tuning trend + timing indicator
3. Elder's Triple Screen
4. Krausz's laws
5. Pring's ROC / KST

## 1. Why combine
- One frame fails: very short = noise obscures direction and invites pattern chasing; weekly alone = clear direction but high risk and poor entries. Use each frame for one purpose: low-frequency data for direction, high-frequency for timing. Floor traders have always done this.
- Tune the pair TOGETHER. A timing oscillator that is a loser on its own is fine if it improves the combined profit and risk (the profit comes from the trend component).

## 2. Trend + timing indicator
- Rule: the timing oscillator's period must be much shorter than the trend period. If trades last ~1 month (23 days), the oscillator should hit an extreme within the first 3-5 days (10-20% of the holding period), i.e. an extreme about every 5 days: use fewer than 5 days to compute it (e.g. 3-day raw stochastic). Take ONLY the first overbought/oversold reading after a new trend signal.
- Linda Raschke "First Cross"-type entries. Euro example (60-day MA + 3-day stochastic): trend alone made $2,075; waiting for the first oversold reading after the upturn entered at 1.2810 (vs 1.2986) and made $6,200; the next entry was worse (1.3736 vs 1.3600) because price moved steadily. Entering on a pullback improves price and % winners and reduces slippage (countertrend orders), but NOT every entry is better; a 14-day stochastic had too few swings and delayed entries.
- Compare combined vs trend-only on risk-adjusted terms over a long sample (testing.md).

## 3. Elder's Triple Screen
- Time frames relate by about a factor of 5 (weekly - daily - hourly; for a 10-minute chart: 1 hour - 10 minutes - 2 minutes).
- Screen 1 (major move, weekly): trend direction = slope of the weekly MACD histogram (or a ~13-week exponential smooth): up if above last week's value, down if below.
- Screen 2 (intermediate, daily): an oscillator to pick the entry window against the major move. (a) Force Index 2-day EMA (= force_index(close, volume, 2)): in an uptrend, buy when it dips below zero without a new multiweek low (stochastic version: buy below 30). (b) Elder-Ray: Bull Power = High - EMA13, Bear Power = Low - EMA13. Buy when the Screen 1 trend is up and Bear Power is negative but rising (never positive); optional: last bull-power peak higher than the prior peak, bear power rising from a bullish divergence. Mirror for sells.
- Screen 3 (timing, hourly): buy stop above the previous day's high (hourly bar high exceeding the previous day's highest hourly high); sell on the reverse.
- Stop: below the low of the entry day or prior day (lower), move to break-even as soon as there is room, then protect 50% of the highest profit; consider exits when the stochastic or Force Index exceeds the 70% level.

## 4. Krausz's laws
- Premise: a robust trend system shows a smooth pattern across calculation periods: a 100-day trend vs 50-day gives larger profit per trade, higher reliability, and proportionally fewer trades; the pattern reverses for shorter periods (limited by noise, slippage, commissions). Plot return per trade vs average holding period; continuity is the robustness check (also testing.md).
- Three frames of similar ratio (e.g. 10 min, 50 min, daily); the shortest is traded, the two longer provide context. Six rules: each frame has its own structure; higher frames overrule lower; lower-frame prices respect higher-frame "energy points" (support/resistance); higher-frame levels are validated by lower-frame action; the next frame's trend defines the tradable trend; chaos in one frame can be order in another.
- Practical gain: patterns appear sooner on the lower frame. Support seen on hourly, daily and weekly at the same price is stronger. The Gann/Fibonacci layer is unvalidated (see behavioral.md).

## 5. Pring's ROC and KST
- Three ROC lines (e.g. 6, 12, 24): the strongest moves occur when all three rise together; a peak in the 24-period ROC while shorter ones rise = minor sell-off; shorter ones peaking while the 24 rises = mild; a major sell-off needs all three to peak then decline. Direction of the trade from a trendline of about half the longest ROC period.
- KST = 4 x avg(ROC24, 9) + 3 x avg(ROC18, 9) + 2 x avg(ROC12, 6) + 1 x avg(ROC6, 6) (the 18-period smoothing weight is not specified in the source; 9 assumed). Very smooth, little lag; trade in the direction of the moving-average trendline, timed when KST crosses its ROC line after the first turn of the trendline; apply divergence/trendlines to KST. Works best on monthly/weekly data, usable on daily as a filter. Always combine with a trendline.
