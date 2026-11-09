# Volume, open interest and breadth (Kaufman Ch. 12, distilled)

Not distilled: Bolton-Tremblay, McClellan and other breadth oscillators in detail, Accumulation/Distribution variants, the intraday U-shape charts by market. Code: `obv`, `filtered_obv`, `force_index`, `volume_oscillator`, `volume_spike`, `market_facilitation`, `ad_index` in scripts/indicators.py.

## Contents
1. Futures volume and open-interest data issues
2. Standard interpretation tables
3. Volume indicators (formulas)
4. Breadth indicators
5. Systematic use: spikes, integrated model, filters
6. Intraday volume and tick volume

## 1. Data issues (futures)
- Futures volume and open interest are posted a day late (intraday estimates exist). Spread trades (calendar rolls) are NOT in reported volume, unlike stock volume which counts both sides.
- Per-contract volume rises as a contract goes deferred -> nearby and falls near delivery: use it only to choose which month to trade (best liquidity), and TOTAL volume (all months) for analysis so month-switching does not look like trend in participation. Rates shift abruptly the last day of the month before delivery (margin hikes); currencies trade the nearby until 1-2 days before it comes off the board.
- Stocks: aggregate sector volume smooths news-driven rotation among peers. Low-priced or thin stocks have small dollar volume; use accumulated sector volume.
- Tick volume = number of price changes in an interval: a good practical proxy for volume and often the only real-time one; two trades in 5 minutes = illiquid.

## 2. Standard interpretation (confirmation logic)
- Price up + volume up = confirms rise; price down + volume up = confirms drop; price up + volume down = weak rally; price down + volume down = weak pullback. Volume tends to lead price; falling volume warns of change. Weekly data adds consistency. 1-week returns with falling volume tend to reverse the next week (folklore; test it).
- Open interest: rises when new buyer meets new seller; falls when old meets old; unchanged when new meets old. Volume/OI: rising/rising = trend confirmation; volume up/OI down = liquidation (at extremes); volume down/OI up = slow accumulation; both down = congestion. With price: rising price + rising volume + rising OI = new buyers; falling/falling/falling = longs forced out, downtrend ends when all sellers liquidated. Rules of thumb: OI grows in trends; volume may fall while OI builds in accumulation; rising price with falling volume and OI = pending reversal. "No one knows" who the position-holders are.
- Breadth (stocks): rising breadth + rising price confirms; divergence warns. Match breadth to what you trade (75% of Dow stocks up while small caps lag). Equal-weighted simple counts preferred (Appel).

## 3. Volume indicators
- Average volume (50 days typical; match the price average length); normalized volume = 100 x V_t / average_N(V).
- Volume momentum V_t - V_(t-n) and % change are erratic: smooth.
- On-Balance Volume (Granville): OBV_t = OBV_(t-1) + sign(close_t - close_(t-1)) x Volume_t; use a moving-average trend (up to ~100 periods) and trade OBV crossing its trend; OBV direction vs price: sideways price + rising OBV = accumulation (bottom), falling OBV = distribution (top); both up = clear uptrend.
- Force Index (Elder) = (Close_t - Close_(t-1)) x Volume_t, smoothed: 2-day EMA (a = 0.667) for timing (buy when low, sell when high); 13-day EMA (a = 0.1428) as trend: long above zero, short below, holding until the opposite zero cross.
- Volume oscillator: (a) difference of short and long volume averages (14 vs 34 days), or (b) ratio of the 14-day to 34-day volume sums.
- Volume-weighted MACD (VWMACD): MACD of volume-weighted EMAs (12/26); trade like MACD; small timing improvement.
- Elastic volume-weighted MA (Fries): eVWMA_t = ((OS - V_t) x eVWMA_(t-1) + V_t x C_t)/OS, OS = shares outstanding (use slightly more than max daily volume); more responsive when volume is high; behaves like a 0.10 EMA but tracks price closer.
- Market Facilitation Index (Williams) = (H - L)/Volume (tick volume): rising MFI + rising volume = confirmation; both falling = false direction, skip; volume down/MFI up = poor entry timing; volume up/MFI down = possible new trend/end of old.

## 4. Breadth indicators
- Advance-Decline: oscillator = Advances - Declines; index accumulates it (unchanged issues ignored).
- Sibbett Demand Index: sum of up volume / sum of down volume over n = 10 (Merrill suggests 5); like RSI.
- New highs/new lows (52-week) add another confirmation series. Breadth data: advancing/declining counts and up/down volume.

## 5. Systematic use
- Most systematic approaches smooth the accumulated series (OBV, A/D index) with a long average and trade trend changes of that series to confirm price; single-day oscillator values are too noisy to trade alone. High volume confirms a new direction; EXTREME volume more often marks a reversal; a volume peak should precede a trend change; declining volume signals equilibrium, not direction.
- Volume spike: volume >= T x average volume (T ~ 2 or more over 1-3+ months). Spikes cluster around unstable periods and mark the END of a significant price move (post-2000 tech-bubble cluster: -50% in weeks). Build the average with a 5-day lag so the 2-3 day run-up does not dampen the spike: V_t > T x mean(V over n days ending t-5). Crude oil spikes often coincide with price reversals; low volume suggests continuation. No comprehensive tests; treat as an observation to test.
- Integrated probability model: 1-day-ahead forecasts via regression slope for price Pf = P + slope(close, n); volume, open interest and OBV likewise. Forecast index = w1*Pf + (1-w1)*(w2*Vf + w3*Of + w4*OBVf), weights sum to 1, tested over a grid; a useless input should get weight ~0. Choose n by minimizing stdev of forecast error. Then trend-follow the index instead of price. Count these weight tests in your overfitting tally (testing.md).
- Filtering low volume: threshold = average(V,n) - k x stdev(V,n); skip days below it (k=1 removes ~16% of days, k=2 ~32% per the book's normal approximation); for OBV leave it unchanged on those days. Price-filtered OBV: ignore days when |price change| < f x stdev of changes (f = 0.10-0.25) because tiny moves could as easily have gone the other way.

## 6. Intraday volume
- Intraday volume has a U shape (high at open and close, low at midday lunch) in older US data; Europe/US overlap changed shapes per market (DAX, NASDAQ, 30-year bonds differ). Light-volume periods (e.g. pound in US afternoon) give unreliable price moves.
- Bar time stamps: CQG stamps bars at the START of the interval (5-minute bars 10:10:00-10:14:59); the last bar of the session may contain only 1 minute; merge it with the previous bar. Check the vendor convention before testing intraday rules.
