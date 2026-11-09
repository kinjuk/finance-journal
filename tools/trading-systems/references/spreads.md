# Spreads, arbitrage, pairs and market neutral (Kaufman Ch. 13, distilled)

Not distilled: the full interest-rate-parity tables, bond/yield-curve arbitrage detail, intermarket ratio studies (gold/silver, crack/crush), per-market carry tables, spread-order mechanics beyond the notes below. Code: `stress_indicator`, `atr_pair_sizes`, `spread_risk_ratio` in scripts/indicators.py.

## Contents
1. Why spreads reduce (and sometimes raise) risk
2. Futures carry, convenience yield, structural change
3. Arbitrage
4. Pairs trading procedure
5. Market neutral strategies
6. Carry trade
7. Spread risks

## 1. Risk reduction
- Spread variance = Var(A) + Var(B) - 2 Cov(A,B) (for a long-A/short-B difference). The more closely related the legs, the larger the covariance and the lower the spread's volatility. Check in a sheet: stdev of daily changes of A, B and of the spread; the stronger the relationship, the smaller the spread's stdev relative to the legs. If the spread is MORE volatile than one leg (legs moving apart, or margin leverage on the low-margin spread), it is not a spread trade anymore.
- Futures spreads get lower margin, so leverage partly restores the risk; stock spreads need full financing of both legs.

## 2. Futures spread dynamics
- Intramarket spread = two delivery months of one market. Nearby contracts react faster and bigger to news; deferreds slower, except policy aimed at long rates.
- Precious metals: pure carry (successive months higher by the interest cost of holding metal): higher metal price or interest rate widens the spread, lower narrows it; industrial use (gold/platinum in electronics) altered patterns. Industrial metals (copper) usually in carry but can backwardate for long (silver first inverted in 1997). Currencies: forward rates follow interest-rate parity; a weakening economy discounts deferreds; central banks resist fast appreciation (yen).
- Carry charges persist even in inverted (backwardated) markets; extreme near-term demand temporarily overwhelms them.
- Convenience yield: F_(t,T) = S_t + (S_t x r x (T - t)/365) + CY, so CY = F - S - interest cost (gold example: F=1400, S=1350, r=5%, no storage cost gives CY return of ~1.2% for six months). Lower rates push more of the difference into CY.
- Spread relationships change structurally: more South American/Asian supply altered grain, orange juice, edible-oil seasonality; larger storage reduces harvest selling; electronics and Chinese/Indian demand shifted gold/silver/platinum ratios (gold/silver "normal" 33:1 was never stable); consumer tastes (red meat, high-fructose corn syrup, ethanol demand for corn); index futures arbitrage forces stock relationships apart (Russell vs S&P). Never treat a historical ratio as an anchor without checking for structural change.

## 3. Arbitrage
- True arbitrage = two highly correlated legs with theoretically no trading risk; profits are small, liquidity limited, risk grows with time in the trade; large institutions dominate (and the fast end is high-frequency).
- Spatial arbitrage (same asset, different venues) requires the gap to exceed bid-ask costs, credit lines, and simultaneous execution.

## 4. Pairs trading (statistical / relative value arbitrage)
- Choose pairs by: (1) correlation of 0.5-0.7 (moves together most days but not always; lower is riskier, higher leaves too little profit to cover costs), or (2) cointegration (shared long-term trend; deviations are the trade; better measure; Engle-Granger two-step, Johansen, Phillips-Ouliaris; needs statistical software; identifies more pairs than correlation). Practical filter: same or related business, similar charts, same reaction in crises.
- Mean-reversion strategy: hold only a few days; longer holding fights each leg's own trend.
- Method 1: difference of two 14-day stochastics > T (e.g. 50): short the high one, long the low one; exit when the difference returns to zero.
- Method 2: stress indicator: D_t = Stochastic1 - Stochastic2 (raw stochastics); Stress = (D_t - min D over n)/(max D over n - min D over n) x 100; enter when Stress > 95 (short leg 1, long leg 2) or < 5 (the reverse).
- Position sizing: equalize risk, not shares: buy/sell (investment / (ATR-in-dollars)) per leg (e.g. $1000 with ATR $0.25 -> 4,000 shares; $25 stock with ATR $1 -> 1,000 shares). Re-adjust only if volatilities move > 20%.
- Stock vs commodity pairs (Barrick vs gold): legs can be traded without short-sale restrictions on the futures side; give up diversification for convenience; expect divergences on company-specific news (earnings).
- Pairs with extreme price ratio ($100 vs $2) cause liquidity and event risk in the cheap leg (a 10% move in a leveraged cheap leg can be fatal).
- Volatility dispersion (options): relative value of index implied volatility vs component basket.

## 5. Market neutral
- Classic: mean-reversion arbitrage applied to an industry group or correlated set (correlation 0.5-0.7 again; cointegration may select better). Long strongest/weakest and short the other via self-ranking: by returns, information ratio, a long-term trend system, or fundamentals ratings. Many names let lower-correlation members add profit while diversification offsets risk.
- Equal ATR-based risk per leg or per basket; rebalance only when volatility differs > 20%.
- Index funds and program arbitrage have raised stock correlations, reducing market neutral opportunities. Stock-market noise is high, so mean reversion with short holding beats trend following here.
- Use conditional/spread orders so both legs fill at an acceptable differential (the opportunity is short-lived); leg-in risk otherwise.

## 6. Carry trade
- Idea: money flows to the currency with the highest real yield; borrow low-rate (yen), hold high-rate (dollar/AUD/BRL). Executed in forwards/futures where the interest differential is ALREADY discounted in the forward price, so it is not literally "capturing carry"; it relies on forward bias (high-yield currencies tend to strengthen/not depreciate enough). Risk: sudden reversal (yen strengthening) can exceed years of carry; diversify across currencies, favor exchange-traded major futures (EUR, GBP, JPY, CHF, AUD, CAD, maybe MXN) to avoid counterparty risk; screen for real rate = nominal minus inflation and economic stability.

## 7. Spread risks (futures)
- Events (Fed, data) affect legs unequally; volatile nearby spreads may not normalize before expiry; short squeezes and delivery problems distort expiring spreads; stock legs with illiquid names; spreads can be riskier than an outright when legs diverge. Test spreads with realistic transaction costs on both legs.
