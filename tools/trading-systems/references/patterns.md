# Pattern recognition (Kaufman Ch. 15, distilled)

Not distilled: the numeric probability tables for weekday, weekend, gap and reversal studies (the book gives them per market; re-run them yourself), Merrill's 104-year NYSE two-month box patterns, per-market day-of-month charts, Aronson's full descriptor sets. Code: `pivot_levels`, `demark_projection`, `weekday_pattern_counts` in scripts/indicators.py.

## Contents
1. What pattern studies are and how to treat them
2. Projecting next-day high/low
3. Time-of-day patterns
4. Opening gaps
5. Weekday, weekend, day-of-month, reversal studies
6. Computer-based pattern recognition and AI

## 1. Treat patterns as hypotheses
- Most trading systems are pattern recognition (charts, MAs). Older patterns are market lore ("up on Monday, down on Tuesday", "locals even up on Fridays", watch key reversals), not facts, until tested by computer.
- Brute-force approach: tally all 2-day (4), 3-day (8), 4-day (16) ... sequences of up/down closes and look for a follow-through tendency. Longer sequences have more combinations and fewer observations: expect false paths. Every pattern found by search counts toward your test tally (testing.md). Patterns are a source of ideas and of false paths.
- Always require a plausible behavioral reason, enough cases per cell (a line with 3 cases means nothing), robustness across markets and eras, and costs.

## 2. Projecting tomorrow's range
- Statisticians: best forecast of tomorrow's price is today's price; no reliable method for projecting the high and low. Traders still use these levels as guides.
- Pivot levels: P = (H+L+C)/3; R1 = 2P - L; S1 = 2P - H; R2 = (P - S1) + R1; S2 = P - (R1 - S1). Example H/L/C 12.50/11.50/11.75 projects a downward bias because the close was low in the range. Alternative: yesterday's close +- half the 14-day average range.
- DeMark projections bias by the open vs the prior close: if close < open: high = (H + C + 2L)/2 - L, low = (H + C + 2L)/2 - H; if close > open: high = (2H + L + C)/2 - L, low = (2H + L + C)/2 - H; if equal: high = (H + L + 2C)/2 - L, low = (H + L + 2C)/2 - H. The pivot method matches DeMark's neutral case when the open equals the prior close (Swiss franc example: 6583 vs 6550/6625/6575).
- Use as entry/exit reference with a stop, never as a standalone edge until tested.

## 3. Time of day
- Classic volume pattern (stocks and futures): highest at the open, next at the close, lowest midday; unchanged by growth in participants and HFT. Causes: orders accumulated overnight execute at the open, positions evened up before the close (locals avoid overnight margin), institutions need heavy-volume times (VWAP algorithms), lunch/coffee breaks thin liquidity and can cause temporary reversals.
- Day-trader implications: opening minutes are for assessment; stock opens gap to align with futures traded overnight, so there is little profit in the first seconds; floor traders sell strong opens and buy weak ones then must even up, reinforcing the opening direction later; a strong open with no downward reaction absorbs local selling and tends to hold. Overnight session moves are not considered decisive for next-day direction; closing prices are viewed as "correct value."
- (See volume.md for intraday volume shape and bar time-stamping.)

## 4. Opening gaps
- A gap implies higher volatility for the day. Study design: bucket gaps in 25 bp increments (>2.5% in the top row); for each bucket count closes that continued in the gap direction, closed between the open and prior close, or reversed; range outcomes (crossed prior close, reversed but not crossing, continued only); and whether the next open continued. Always show both counts and percentages and ignore thin buckets.
- Gap frequency differs by instrument: a stock (ABX) gaps > 1% often; e-mini S&P almost never because Globex trades 6 PM to 4:15 PM so the "gap" is the 15-minute break and the overnight move is already priced. Use the right session definition (pit vs electronic) for any gap test.
- Idea: strong open + stronger close allows buying a pullback after the open; strong open + weak close allows shorting near the open. Entry timing refined by intraday patterns.

## 5. Weekday, weekend, month-day, reversal studies
- Weekday patterns: encode each day's close-to-close direction relative to the Friday-to-Monday move as X (same) or O (reversed), e.g. XOXXO; compare probabilities per market. Tuesday reversal after a strong Monday is lore; verify per market. Trend filter (20/50/200-day MA direction at Friday-Monday) raised the probabilities of the patterns (EURUSD: Tuesday reverses then Thursday reverses went from 55% to 61% with the 200-day filter); results are not best in all cases (S&P not as clear as EURUSD); choose combinations that improve across trend settings, a more robust solution. Test entry at the next open vs the prior close.
- Weekend patterns: Friday liquidation by short-term traders, Monday resetting, weekend news build-up; relate Monday's open/close to the prior week's move.
- Day-of-month (extends Ch. 10): recent decade shows buying in the last few days of the month across markets and selling in the first days, with a bounce on day 1; gold, crude and soybeans shifted by era (gold: lower month-end 1975-2000, higher 2001-11, partly a trend artifact). Buying about four days before month-end and exiting at the end of day 1 captures "free exposure"; averages hide losing months; sustained contraction would weaken it.
- Reversal patterns (leading indicator/filter): (1) intraday trend continuation (higher high and higher close than before; check open/close next day), (2) reversal day (higher high, lower close; most traders expect follow-through) and (3) outside reversal. Check whether follow-through actually exists per market before use.

## 6. Computer-based recognition and AI
- Descriptor/class approach (Aronson): define the trade you want (e.g. move >= 3% within 20 days with no loss > 0.5%), mark the 5 days before every qualifying move as buy days (or sell days), then search indicator combinations (MA direction, RSI/contrary opinion, volume direction, 10-day momentum) for values that occur mostly on those days. Poor signals still occur at those values: the set condition is necessary, not sufficient.
- Heuristic/AI (expert systems, neural nets, genetic algorithms): knowledge base + inference engine; learns what worked in recurring situations but cannot handle new ones and can keep elaborating pattern combinations that already produced inconsistent results = overfitting at a sophisticated level. Use out-of-sample discipline (testing.md); see Ch. 20/24 for GA use.
