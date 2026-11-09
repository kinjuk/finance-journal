# Trend systems (Kaufman Ch. 8, plus N-day breakout from Ch. 5)

## Contents
1. Why trend systems work
2. Signal definitions
3. Which trend method? (comparison)
4. Test standards for trend studies
5. Two and three trends
6. Choosing trend speed
7. Early exits and macro trends

## 1. Why trend systems work
- Long trends capture fundamentally driven moves (interest-rate policy is slow and persistent; it feeds FX, trade balance, mortgages, equities). Prices have a FAT TAIL: more long directional runs than random (fewer runs of 1-2, more runs >6). These few long runs produce the exceptional profits a trend system needs.
- Money flow sustains trends (noise short term, persistence long term).
- Trend systems earn only when markets trend; no technique rescues sideways markets and no method is always best. Most trend methods have similar returns over time; they differ in RISK PROFILE and TRADE FREQUENCY. A trend exists "if you can profit from it using a trending strategy."
- Tolerance for interim reversals determines whether the fat tail is captured.

## 2. Signal definitions (specify exactly; ambiguity corrupts tests)
- Price-penetration: buy when price crosses/closes above the trendline; sell short below. Using the CLOSE reduces whipsaws; (H+L)/2 or (H+L+C)/3 versions can only be computed after the session.
- Trendline-direction: buy when the trendline value rises vs prior bar; sell when it falls. More stable (ignores price crossing back and forth) but lags more.
- Always state: signal price (close vs intraday), order type, and execution assumption.

## 3. Which method? (Kaufman's six-system comparison)
Systems: momentum, moving average, exponential, N-day breakout, linear-regression slope, swing. Net conclusion: differences in profit are small; differences in profile are large.
- Moving average: many trades, many small losses, few big wins ("conservation of capital"); loses sooner, holds biggest winners longer.
- N-day breakout: higher % winners and much larger profit per trade but takes very large risk and holds very long (a 100-day breakout is investing).
- Regression slope: in between.
- "There is no best system, only trade-offs": pick the underlying method to fit your risk tolerance (win rate vs loss size vs holding time).
- Fast systems (calc periods giving >200 trades in 20 years in the euro test) did worse than slower; fewer trades gave higher profit factors. Profit factor < 1 = loss.

## 4. Standards for fair trend tests
1. Same long test period for all (20 years, bull/bear/sideways). 2. Start all tests on the same date (the one with the longest wind-up, e.g. 160 days). 3. Speeds from a few to ~100 trades per year; below 2-3 or above 100 per year is not tradable. 4. Realistic costs (too low = fantasy, too high = false rejection). 5. Judge by profit factor / information ratio (returns vs risk), also net profit, trade count, % winners, avg trade. 6. Have expectations: fast vs slow and breakout vs MA each have distinct profiles; use them to catch bad results (the engineer's 10-ft bridge over a 100-ft river).

## 5. Two and three trends
- Rationale for two: slow trend = fundamental direction; fast trend = timing and shorter holding. Trade the fast signal ONLY in the direction of the slow trend. Eurodollar 60d + 20d with $40 round-turn cost: 60d alone held ~31 days; 20d alone made $62/trade; combined $92/trade, same holding as 20d, slightly lower total profit than slow alone, in market ~50% of time (lower shock risk).
- Do not accept a combination found by computer if each trend is unprofitable alone, unless a large share of combinations are profitable or each trend has a stated purpose. A 38/40 pair is pointless; periods should differ by a meaningful percentage (roughly 2x).
- Three trends: long = direction, middle = shorten holding, third (fast, ~3 days or <= fastest MA) = entry timing/confirmation. Modified 3-crossover filter: do not enter long (short) unless the slope of the confirming fast MA is up (down). Effect: fewer trades, more profit per trade, similar total profit. Eurobund 1990-2011: 20-40-80 beat 40, 80 and 40-80 but with fewer trades (one trending market; do not generalize).
- 4-9-18 crossover (1970s): slightly faster than 5-10-20 and each about double the previous (constant % spacing). Fast trends do worse in recent years than in the 1970s.
- Appel: sum of three ROC (momentum) indicators on S&P, buy when composite crosses above 4%.

## 6. Choosing trend speed (without a brute-force search)
- Match the horizon: a hedger needing one signal per month needs ~10 days, not 3. A 3-day average gives 5-10 signals a month from 2-day moves.
- Common sense: a computer favoring a 3-day over a 20-day should be distrusted (execution costs and fast-market slippage).
- Seasonal markets: a trend lasting 6 months cannot be caught by a 6-month average; use a period below ~1/4 of the trend length. A "best" period of 6 months or more means the test failed to capture the seasonal move.
- Method differences in net return are small; frequency, per-trade size and per-trade risk differ.
- Chart method: mark the swings you want (IBM 2000-02: 8 tops/bottoms in 22 months, avg swing ~3 months); calculation period ~ 1/4 of the average swing (16 days). That gave 36 trades, 20 winners, +$114/share without optimization (no costs). Worst-retracement method: period = length of the move to ignore (42 days for a 2-month move) avoided the correction but lost money overall; accept frequent small losses rather than tuning them away.
- Signal progression: compare adjacent trend speeds. Healthy turn: changes progress cleanly short-to-long. If the 20-day flips but 19 and 21 do not, the signal is unreliable (drop-off effect). Erratic short-period flips are normal below ~10 days.

## 7. Early exits, macro trends
- A 200-day trend lags ~100 days; for a falling-yield move of 2% the trendline can lag ~1%.
- Macro trends rest on policy; if policy clearly changes (central bank shifts), exit before the trendline turns, since a slow trend can take ~6 months to signal. Decisions are clear only afterward (2010 hints of change; 2011 was a record year for trends), so treat as a discretionary overlay with a rule, not a prediction.
- Projected crossover: an N-day moving average crosses the next price at the (N-1)-day average of the last N-1 prices; use to anticipate signals and place orders in advance.

## 8. Event-driven trends (Ch. 5: N-day breakout; swing charts and P&F are in swing-regression-ma.md)
- N-day breakout: buy when today's high exceeds the high of the past N days; sell/reverse when the low breaks the N-day low. More conservative: require the CLOSE beyond the N-day extreme (confirmation, later entry). Always in the market (reverses).
- Event-driven vs time-driven: breakout reacts to an event (new high/low) not elapsed time. For N < 5 it is effectively trend continuation, not an event. Risk = distance from entry to the opposite N-day extreme, so large N = much greater risk per trade (and higher profit per trade, higher % winners).
- Donchian 4-week rule (1971): long when price exceeds the highs of the previous four full calendar weeks, short below the four-week low; futures rolled on the last day of the month before expiry. Historic benchmark of simple rules that kept working.
