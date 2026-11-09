# Practical considerations (Kaufman Ch. 22, distilled)

## Contents
1. Data and computer use
2. Development discipline (vertical vs integrated, transparency)
3. Diagnosing a system that "should work but doesn't"
4. Extreme events / price shocks
5. Martingales, selective trading, trade-offs, signal similarity (see bottom)

## 1. Data and computer use
- Computers do not find systems; brute-force/neural/genetic search over everything = overfit. Reason the idea out first.
- Data checks (daily): outliers >4% from prior bar (or preset), gaps of >4 days with no data, open/close outside high-low. Intraday: tick-frequency gaps, large spikes that reverse in seconds. Plot the series: decimal-shift errors show up visually. Combining vendors can mix scales (135.50 vs 13550).
- Dilemma: systems built on clean data can fire many false signals live on dirty data (seen in open-outcry energy). Fix: develop on the dirty data so the system is insensitive to bad prints.
- Use standard tools first (MA, RSI, breakout, stochastic). Trend profit comes from prices trending, not the exact formula; trend SPEED matters more than method. Use third-party/spreadsheet tools to analyze saved optimization output (average, variance, robustness).
- Use as much history as possible; old data is only invalid after a real structural change. If old years were low-volatility, a strategy should at least not lose in them.
- Paper trade before real money: write expectations first (trade frequency, holding period, % winners, avg win/loss). Assume worst price of the 5 minutes after an intraday signal, or worst of the closing range for on-close orders. Then start small.
- Four outcomes of a diligent project: profitable / not profitable / cannot be implemented / too slow or costly. Build slowly; stop when performance deteriorates after adding a feature.

## 2. Development discipline
- Vertical (stack tested building blocks; primary rule must work alone) vs integrated (interdependent parameters tested together, e.g. trend speed + volatility filter). If vertical shows the filter does not help but an integrated solution looks great, test it: the feature is real only if the PERCENTAGE of profitable parameter combinations with the feature exceeds the percentage without it (robustness measure from Ch. 21).
- Prefer transparent systems (a trader could verify a signal on a chart). Complex, non-transparent systems can be wrong undetected and are hard to debug.

## 3. Diagnosing disappointing results
- Rules misprogrammed: ambiguous rules interpreted badly (e.g. "volume confirmation" coded as today > yesterday; should be > 10-day average).
- Parameter range simply does not work: negative results are information. Example: medium trends (15-70d) have highly variable holding periods; fix by combining long trend (fundamental direction) with medium trend (timing within it), then understand WHY.
- Works in some markets only: markets in the same sector should behave alike (two autos, two telecoms); be concerned if similar markets differ. Fixed income has the longest trends; equity indices the most noise.
- Hidden assumptions / selected data; test other markets and filter high/low volatility and high-correlation periods.
- Ignoring a few large losses (Long-Term Capital): removing historic worst events to lever up. Same events do not repeat, different ones of equal size do. History shows too little risk; correlations are rising. Accept big losses as likely but rare.
- Misjudging volatility: a constant NASDAQ contract count from 1996 to 2000 is ~6x the risk (600 to 4,000). Size and stops must scale with volatility; check the test did.
- Evolving market: more participants means more short-term noise; trend systems enter/exit later and show decaying profit over long tests.
- Simple systems (long-term trend, dual MA crossover) would have exited equities after 2000 and before 2008's worst; being proactive costs small opportunities but avoids big losses.

## 4. Extreme events
- Price shocks (unexpected events or surprise data) cause the biggest gap between backtest and live. Diversification fails in shocks: correlations go to 1 as money is liquidated; unrelated markets (soybeans, cocoa) move in sympathy.
- Backtests treat shocks as ordinary days, and parameter selection benefits from lucky shocks. Never assume an open position lands on the right side of more than ~50% of shocks (likely fewer).
- Four shock cases (1991 Gorbachev, 1992 UK election, 1990-91 Gulf War, 9/11): shocks do NOT always hurt trend followers; prices tend to reverse AFTER the shock is absorbed (sentiment flips); volatility always increases afterward. Implication: if a shock gives a windfall, reduce/exit given the higher risk; if capitalized to survive, a crisis-management plan can recover part of the loss in the second phase.

## 4b. Crisis management (continued)
- Full reserves for worst case usually push expected return below bond yields, so a tactical plan is needed. Kaufman's plan after a shock: (1) windfall profit -> exit; (2) large loss -> hold for the expected reversal (most of the damage is already done by the time you can exit; reversals typically came within days, 13 days to new highs after Gorbachev; UK 1992 took 3 weeks; 2012 orange juice reversed in 4 days); (3) with adequate reserves, add on peak volume or once volatility subsides.
- Trend systems disconnect in a crash: in Oct 1987 the 50/100/200-day MAs all turned down on the day of the lowest price, so a trend sell signal would sell the bottom; MAs then lagged the recovery by months (50d turned up late Dec, 100d in March, 200d in August 1988). Consider crisis rules (liquidate shorts, hold longs) instead of following the signal mechanically.

## 5. Martingales and the theory of runs
- Martingale (double after each loss) wins small amounts often; fails on one long run or at table/margin/capital limit. Capital needed = initial bet x 2^(longest run); a 1-in-256 expectation of an 8-run means bet = capital/128. Anti-martingale (double winners, stop at a goal) wins big only if the long run arrives early; expected break-even otherwise.
- Test whether markets behave like a fair coin before using either: Kaufman ran runs-of-up/down-days analysis on 15 futures (2000-2011); price runs are longer than a random series. Conclusion: neither is a free lunch; position scaling must come from risk control, not from betting systems. Anti-martingale-style scaling WITH trend (add to winners with capped risk) is the defensible version.

## 6. Selective trading and filters
- Overriding a system is usually the intuitive urge to hold losers; keep losses small and follow the plan. Override only for a documented crisis rule or for a genuine market/system disconnect.
- "Remove the losing trades" via multiple indicators, cross-market or seasonal confirmation: a combination will always look great in testing; that is overfitting. Simple, with larger risk than you want, is usually best. Do not bolt black-box systems onto yours (duplicated techniques, hidden risk, correlated).

## 7. System trade-offs
- You cannot have large profits, high win rate and small losses at once. Choose among frequency of wins, size of wins vs losses, and number of opportunities. Transaction costs make "tiny losses" strategies fail; "risk-free" arbitrage is not risk free.
- Trend following: many small losses, few large wins ("conservation of capital"); 30-35% winners normal, 40-45% is a ceiling for smoothing methods. Longer trends capture more of the fat tail but carry more lag risk. Judge by the aggregate of losing sequences, not single-trade risk.
- Mean reversion: positions set before the reversal (timing risk); profits capped by goal, so they must be frequent (high win %), and therefore losses cannot be tightly limited. Methods that wait for a turn have a trend element.
- Combining trend and range (the Commodex idea) is possible but must be tested as an integrated system.

## 8. Trading limits and signal similarity
- Limit moves and disconnected markets break stop/exit assumptions (act like price shocks).
- Trend systems with different parameters are positively correlated because they harvest the same trends; correlation falls as the percentage gap in period widens (10 vs 20 days lowers it more than 50 vs 60). Lukac/Brorsen/Irvin: 12 popular trend techniques over 12 futures markets (1978-84) showed similar performance. ISAM: long-term returns of trend systems converge; variation shows year to year.
- Diversifying across periods helps less than it appears. All systems are in the same trade at the best AND worst times (correlated drawdown and shock risk). Control with the sizing and portfolio methods.
