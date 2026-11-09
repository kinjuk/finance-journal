# Behavioral techniques (Kaufman Ch. 14, distilled)

Not distilled: Elliott Wave/Fibonacci geometry (golden rectangle/spiral, pentagon, Gann time-price squares), DeMark alternate arcs, financial astrology (planetary/lunar cycles, Gann/Bradley), most Bullish Consensus figures. The book presents astrology and Fibonacci geometry as interesting but not validated; do not treat them as evidence-based rules. Code: `volatility_ratio`, `cot_index` in scripts/indicators.py.

## Contents
1. News and surprise
2. Event trading (post-shock)
3. Commitment of Traders (COT)
4. Contrary opinion and sentiment
5. Fibonacci and other folklore

## 1. News
- News is the largest single driver of free-market prices, but it is hard to rank objectively (bullish +, bearish -, weights), subject to bias, and impossible to ignore once seen. A systematic trader holding a technical position would do best to avoid news exposure; as an input, news only has value if quantified.
- Price just before a scheduled report is the best measure of expectations. The market always discounts its best guess, so the SURPRISE (actual vs expected) moves price; if price rallied into a bad report and the report is neutral, price drops to remove the wrong expectation. Use price changes between releases to judge whether an event is already discounted.

## 2. Event trading
- Two kinds: (a) scheduled reports/earnings/analyst calls (modest moves; typically traded against the reaction), (b) unexpected price shocks (largest moves, biggest risk, out of proportion to normal trading risk).
- Do NOT position ahead of an event (50% odds, very high risk); study patterns AFTER the first reaction. Post-event drift exists because no one knows the correct price immediately (efficient-market "instant" repricing is rejected by the author): underreaction (or structural change) = continuation over the next days; overreaction/short-lived event = reversal. Size of reaction matters: small surprises tend to continue; very large surprises may be treated as errors or over-anticipated (CPI example: 0-0.2 no reaction if expected; 0.2-0.4 clear reaction; > 0.4 shock, may reverse).
- Candidate events need enough volatility for a profitable follow-up, a favorable historical probability, or must hedge another position.
- Measure the surprise: volatility ratio = true range_t / (average true range over previous n days, lagged m days); n = 60, m = 30 (the lag keeps one shock from contaminating the next). Ratio > 3.0 = news-driven shock. Use true range (shocks happen overnight; use pit-session data where available).
- Treasury volatility is greatest on the report day and lowest the day after; weekly cyclic volatility between monthly releases.
- Warwick rules: buy on the close if price closes in the upper 20% of the event-day range AND the market has a historic continuation pattern; hold a pre-set number of days from the lag pattern; use a stop-loss. (Mirror for shorts.) Larson (corn, older): 81% of price change occurs on the event day; typical 8% reversal over the next 4 days; net 27% in the original direction over 45 days.
- Trend link: if trend following works in a market, normal shocks are in the trend direction. Shock survival matters more than shock prediction (testing.md, pitfalls.md).

## 3. Commitment of Traders (COT)
- CFTC report (positions as of Tuesday, released Friday since 2000; earlier monthly/biweekly): open interest split into commercial (hedgers), large speculators (non-commercial), small traders (nonreportable); reporting thresholds by market (e.g. 500 contracts 30-year bond, 300 S&P). 2010 reclassification separates swap dealers, giving "true commercials."
- Jiler: compile normal position patterns by season; look for when one group's share is unusually large. Commercial position changes are large-scale (commercials' trend-direction sets 67% of the time per one study).
- COT Index (Briese) = 100 x (NL_t - lowest NL over n)/(highest NL over n - lowest NL over n), NL = net long of a group; n = 1.5-4 years (Ruggiero used 1 year for plotting). Commercials reach bullish extremes (index > 80) just before up-moves and bearish extremes before drops; small traders are out of phase with commercials and turn bullish as price peaks; funds turn bullish/bearish around the middle of the move as commercials exit. Short signal: commercial index > 80 while the other two < 20 (buy is the reverse). Holding time ~3-6 months.
- Cautions: a "qualified hedger" can also take speculative positions; commercial positions are a slow filter, not a timer; Tuesday data is 3 days stale.

## 4. Contrary opinion
- Contrarian = between fundamentalist and technician: opposes unified crowd opinion because when everyone is positioned, nobody is left to push price further (then a blow-off and reversal). Sentiment is a FILTER and risk guide, not a timing signal.
- Opinion measures: Consumer Confidence, Bullish Consensus (poll of advisory letters weighted by circulation; neutral ~55% because of the novice bullish bias; normal range 30-80%; 90% in an advance or 20% in a decline = overbought/oversold, look for an exit, do not reverse until price confirms, e.g. with a moving average; a 10% change within two weeks is significant), Market Sentiment Index, COT-based sentiment. Hadady's arithmetic: with 80% bullish, the average bull holds only 1/4 as many contracts as the average bear, so a decline cascades.
- Practical rules: within the normal range trade WITH the trend; use extremes to avoid late entries and to tighten exits; good moment to fade is when general news moves price further than seems reasonable in the crowd's direction; specific news that fails to move price at an extreme consensus signals an exhausted trend (Schabacker: follow the crowd when fundamentals are really improving, leave it when action rests on rumor, prospects, publicity).
- Weakness: timeliness (a 60-70 letter poll is stale on arrival) and subjective thresholds. "Works 100% of the time" requires an accurate consensus.

## 5. Fibonacci and folklore
- Fibonacci ratios (0.382, 0.618, 1.618) appear in nature and Elliott's wave counts; the book notes they have become part of price analysis (retracement levels, targets, circles/arcs for time-price). Application is subjective and complex (wave counting). Treat as widely watched levels (self-fulfilling support/resistance), not as validated edges; test any rule before use (foundations.md, testing.md).
- Financial astrology, Gann, lunar cycles are discussed historically; no systematic evidence is given in the book. Do not use as signals without independent testing.
