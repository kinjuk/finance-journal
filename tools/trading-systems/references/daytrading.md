# Day trading and short-term systems (Kaufman Ch. 16, distilled)

Not distilled: the full cost/volatility tables (Table 16.1), later intraday pattern programs (key-level strategies, midday support/resistance variants beyond the outline, intraday volume tests), Crabel's complete pattern list. Code: `opening_range_breakout`, `intraday_shock_signals` in scripts/indicators.py.

## Contents
1. Nature of day trading
2. Transaction costs (the binding constraint)
3. What works at short horizons
4. Intraday support/resistance and patterns
5. Opening range breakout
6. Intraday price shocks

## 1. Nature
- A day trade is opened and closed within the same session; the chapter extends to systems held ~24 hours. Peak popularity coincided with the early-2000 stock top; the opening-range breakout was the strategy of the day, then faded.
- Intraday prices respond to noise (reports, fund orders, upgrades, news flow), not fundamentals. Day trading is focused on patterns, noise and volatility. It demands discipline: shorter response time magnifies bad habits.
- Evolution: directional breakouts (1990s) -> pairs/market neutral (early 2000s) -> high-frequency mean reversion/market making (now). Competition has pushed margins to ~1 cent per share net in NASDAQ names; individual edges survive mainly in spreads of different deliveries/related products, sector baskets, formula spreads (energy crack, soybean crush), and in longer holds (up to a few days) with larger risk.

## 2. Transaction costs
- Costs = commissions + slippage (execution price minus intended price). They can turn expected profit into loss. Fees fell from 1% of share value / $50 per futures contract (early 1970s) to ~$7-10 per stock order (any size) and $3-15 per futures contract, so for a position trader costs are incidental but for the day trader they dominate.
- Improve by: lower commissions, careful opportunity selection (prefer higher-volatility markets so costs are a smaller fraction of range), better execution. Volatility measured with true range includes the overnight gap; strict day traders should use high-low range.
- S&P e-mini: open-to-close range is only ~1/2 of the full-day range, so enter-open/exit-close forfeits half the opportunity; entering at better than the open is a worthy goal.
- Trend (directional) trades have higher slippage than mean reversion because they buy strength and sell weakness. E-mini S&P ($50/point): expect >= 0.5 point ($25) slippage per entry and exit, more in fast markets. Book example: daily range $931, $10/side fees, $100 slippage leaves $821; capturing 1/4-1/2 of range is enough ONLY if many trades are winners; typical trend trading wins ~1/3 of trades with winners ~2x losers, which nets to roughly the transaction costs lost (per the book's arithmetic). Always apply real costs per trade before accepting a short-term system (testing.md).

## 3. What works at short horizons
- Traditional trend-following methods are not used for holds under ~3 days and likely do not apply under ~20 days. Fundamental/policy analysis is irrelevant for intraday; trading the REACTION after an economic-report jump is a valid day-trade idea (react, do not anticipate; see behavioral.md event trading).
- Short-term movement is mostly noise, so: (1) directional entries should wait for a pullback; (2) mean reversion is the preferred strategy. Classic triangles/flags on intraday data are random-looking and weak bases.
- Key levels for floor traders: today's open, today's high/low, yesterday's close and high/low, less important last week's high/low, memorable older support/resistance, contract high/low. A price satisfying more than one level has more confidence.
- Point-and-figure for day trading: minimum box (1-tick/min move) with 3-box reversal, charts continued across days; signals have NO lag (they occur concurrently with the breakout); on an outside day plot the reversal (brings the stop closer); stops advance only on P&F reversals; mostly used for countertrend support/resistance; trend-direction entries fit short overnight holds where the move is larger. Still pays directional slippage.
- Moving averages are poorly suited intraday (built-in lag; unevenly spaced time, noise > trend; open-to-close span ~50% of daily range leaves little time to enter and still profit).

## 4. Intraday support/resistance and 1-3 day patterns
- 1-3 day holds: in trends Monday continues the trend, Tuesday/Wednesday fade as new buyers/sellers tire (profit taking), Thursday resumes, Friday afternoon shows minor reversal for weekend risk reduction; in sideways markets Friday and Monday directions differ from the prior week and each other (see patterns.md).
- Support/resistance: the prior high is expected to attract professional selling and breakout stop orders; the 1-3 day range narrows as levels become obvious (like a short-timeframe triangle).
- Midday S/R strategy (TSM Midday Support and Resistance, 15-30 min bars): morning = open to 12:00; record morning high/low and highest/lowest close; afternoon: if flat or short and a bar closes in the lower 25% of the morning range, cover/go long (mirror in the upper 25%); new lows/highs after midday imply continuation. Rationale: midday volume and volatility lows are reversal windows.

## 5. Opening range breakout (Crabel)
- Entry: buy when price rises X above the day's open, reverse short at X below the open (X = fixed ticks, or volatility-based); all trades exit at the close. Variants: pivot at prior close; hold overnight; require an inside-day (or low-volatility) prior day (Crabel: significant improvement).
- Crabel table (% of days with the breakout level reached/profitable-type frequency, any day vs after an inside day): bonds open+16 ticks 60% vs 76%; S&P +160 pts 68% vs 61%, -80/-160 pts 49% vs 48/45%; soybeans -10c 63% vs 76%; cattle -50 pts 63% vs 73% (inside day usually raises the odds, except S&P). Illustrates asymmetry by market and that the filter helps most where noise is low.
- Updated test (to Feb 2011): crude oil 5-minute bars, breakouts $0.05-$1.00/bbl, Mar 2009-Feb 2011: profitable at every breakout size before costs; profit per contract approached ~$100 as the breakout widened; small breakouts give profit per trade too small to survive costs; holding overnight raised per-trade profit but lowered profit factor; trading only after inside days with overnight holds cut the trade count sharply. Judge robustness by profits across the WHOLE breakout range, not the best size (testing.md).
- Intraday N-bar breakouts (10 bars) in the 1990s produced shockingly large risk when prices whipsawed intraday and held overnight.

## 6. Intraday price shocks
- Shock = an intraday bar at least 3x the average bar size (or volume 2x the average for the same time bar). Spikes cluster at the open (daily open spike in gold; stocks too) and around reports. Average choices matter (last n bars vs same-time bars over n days); compare to the 100-day average-off volatility of the same bar.
- Reaction strategy (premise: abnormal moves are mostly noise and tend to reverse): at the day's open, if true range > 3x the prior bar's average and the close is in the top 20% of range -> sell short the next bar's open; close in bottom 20% -> buy; otherwise intrabar: if the bar's volatility is 2x the average for that bar and the close is in the top/bottom 20% of its range, fade it. No stop for the next 2 bars (let volatility play out), then stop beyond the extreme of the entry bar or the following two bars; exit at the close. Profitable for gold (20-minute bars, since 2000) and 30-year bonds (factor 2.5) in the book. Possible refinements: volume filter; exit when volume falls back to average (floor traders "listen to the noise" and exit when it fades).
