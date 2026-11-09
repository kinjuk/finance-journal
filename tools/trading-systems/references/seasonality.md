# Seasonality and calendar patterns (Kaufman Ch. 10, distilled)

Not distilled in detail: link-relatives arithmetic, the full detrending worked examples, the seasonal calendar tables, key-date studies. Code: `seasonal_table()` in scripts/indicators.py.

## Contents
1. When seasonality is real
2. Data traps
3. Calculation methods
4. Seasonal filters and trades
5. Stock-market calendar effects
6. Common-sense limits

## 1. When seasonality is real
- Real seasonality needs a recurring physical or behavioral cause: harvest forces selling (limited storage, minimum 3-month rental), carry costs make deferred contracts higher within a crop year (backwardation in crude/copper is temporary demand overwhelming normal carry), construction/housing drives copper, summer travel drives airlines, winter drives heating oil, tax and holiday behavior drives equities.
- Seasonality sets: position bias through the year, changes in risk (seasonal volatility), direction, profit. It is easier to find than cycles/economic trends because it repeats every calendar year.
- If a pattern cannot be explained by fundamentals, avoid it. Financial markets (bonds, yen) have no forced calendar action; participants can hedge or wait. Restrict seasonality work to markets driven by weather, nature, or consumer calendar behavior (grains, softs, livestock, energy, metals with housing links, some equity sectors).
- Seasonality drifts: Brazil soybeans, Asian demand, on-farm storage and cattle imports have shifted grain/livestock patterns. The "best day" in 1975 is not the best day now.

## 2. Data traps
- Use monthly data (weekly/daily is noisier and too specific). Use month-end (last) prices for tradable results; monthly averages smear the signal.
- Cash/spot gives the textbook seasonal pattern; back-adjusted continuous futures can give a distorted or out-of-phase one (wheat: cash low May-June, median low July-Aug; futures spiked down in July with averages out of phase). Futures are what you trade, but for the underlying pattern, cash is safer. Compare both.
- Back-adjusted futures cannot be indexed or used for percentage returns (negative/changed prices). Index only cash or stocks: set first value 100, then chain by percentage change.
- Price changes at high price levels swamp earlier years: use percentage (indexed) changes. Southwest Airlines in dollars looked flat (+-$0.50) but in percent showed +-6% with a clear April-July peak and November (Thanksgiving) bump; August, September, January lows.

## 3. Calculation methods
1. Month x year table of monthly changes (dollar or %); compute AVERAGE, MEDIAN, % up months, and seasonal volatility (stdev by month).
2. Adjusted seasonal = monthly average (or median) / average of all monthly averages (ratio to the yearly mean). Medians resist one or two extreme years.
3. Detrend first: remove the long-run trend before measuring the pattern, or a rising market makes later months look seasonally strong.
4. Link relatives method (chain month-over-month ratios) is another route; results from all methods are usually similar (one says September low, another October; both flag the same pair of months).
5. Seasonal volatility chart confirms risk by month.
6. Group "years with similar characteristics" (drought, good-weather, freeze years): a few special-event years distort the average; separate normal years from event years and study each.

## 4. Seasonal filters and trades
- A seasonal filter marks the periods when only longs or only shorts are allowed. Select periods from detrended data using medians. Entries should be averaged in (e.g. 25% per week through the month), not fired on one date.
- Heating oil 1984-2011 monthly % example: averages exceeded medians in many months (extreme months distort). The statistical longs (end-Feb to end-Mar; end-May to end-Aug; end-Oct to end-Dec) and shorts (end-Mar to end-May; end-Aug to end-Oct): May-Aug (inventory build) and Oct-Dec (winter stocking) have a reason; Feb-Mar is statistically fine but risky (a late cold spell: +40% Mar-Apr 1982, +20% in 1983). The 1990 Gulf War rally conformed to the Aug-Sep pattern by coincidence. Understand the fundamentals before trading the numbers.
- Soybeans: classic long April 1 to June 1 (planting/crop development), short Sept 1 to Nov 1 (harvest); post-harvest rally, tax selling and Brazilian maturity feed the February break.
- Use overbought/oversold timing inside the seasonal window; averaging in is always safe.
- Test the seasonal rule like any system: out-of-sample, costs, many markets, and count how many years it worked (a 20-year sample has only 20 observations per month).

## 5. Stock-market calendar effects
- S&P 1982-2000 vs 2000-2010: earlier low volatility and clear summer decline; recent decade more volatile. October-November strength persisted (return from summer, year-end tax moves); "buy in May and go away" no longer reliable. Cash Dow shows a similar pattern (peak end-April, October rally). Patterns change; only significant ones survive.
- Holiday effect (Merrill 1966; Fosback; Kaeppel; Freeburg): day before holidays up 67.9% of days vs 50.8% day after (1897-1964); Thanksgiving-to-New-Year up 74%; July 4-Labor Day 69%; before Christmas 74%. Buy the close 3 days before an exchange holiday, sell 2 days later (Kaeppel); Fosback bought 2 days before and sold the day before: +880% 1928-1975, 70% winners, vs buy-and-hold -41% (all gains came from a few days a year). Still profitable later (also Treasury bond futures and corporates) but less so. Base rate: ~54% of all days up 1897-1964.
- Month-end effect: buy the last (or second-to-last) trading day of the month, exit on the 4th trading day of the new month (liquidation then reset); confirmed by several authors, still viable for S&P and bonds, less profitable post-1975. Day-of-month patterns are in Ch. 15.
- Hirsch strategy: buy Nov 1, sell Apr 30 (six months), avoiding summer doldrums.
- Warning: these were found and confirmed on pre-1975 data with fewer participants; discount published edges, and check recent-decade performance and costs.

## 6. Common-sense limits
- Do not be too specific: expect corn's seasonal high "usually July, sometimes June or August" and the harvest low in September (possibly October/November). Study the big picture first, then how the pattern develops each year; scale in rather than pick a day.
- Confirm seasonal trades with trend/momentum timing; do not let a seasonal bias override a strong contrary trend and risk stop.
