# Formula sheet

Notation: r = required return (rho = 1 + r). Subscript F = firm/operations, E = equity, D = net debt (after tax). t = year. Balances are end-of-year unless "beginning". All income is after tax.

## Contents
1. Accounting identities
2. Free cash flow
3. Profitability and its drivers
4. Valuation models
5. Simple valuations
6. Multiples
7. Cost of capital
8. Reverse engineering

## 1. Accounting identities
- CSE = NOA - NFO, where NOA = operating assets - operating liabilities, NFO = financial obligations - financial assets (negative NFO = net financial assets).
- Clean surplus: CSE_t = CSE_{t-1} + comprehensive income_t - net dividends_t (net dividends = dividends + buybacks - share issues).
- Comprehensive income (CI) = operating income (OI) - net financial expense (NFE), after minority interest and preferred claims.
- Tax on OI = reported tax + (net interest expense x tax rate). After-tax NFE = net interest x (1 - tax rate), plus after-tax unrealized financial gains/losses with sign.

## 2. Free cash flow
- FCF = C - I = OI - change in NOA.
- FCF = net dividends + net payments to debt holders = NFE - change in NFO + d.
- Treasurer's rule: change in NFO = NFE - FCF + d. Surplus FCF over interest and dividends buys down debt or builds financial assets; a deficit borrows.
- From a reported cash flow statement: C = reported CFO + after-tax net interest paid; I = reported investing cash flow - net investment in interest-bearing instruments.
- Dividend/ownership-side identity: d = FCF - NFE + change in NFO.

## 3. Profitability and its drivers
- RNOA = OI / average NOA. NBC = NFE / average NFO. FLEV = NFO / CSE.
- ROCE = RNOA + FLEV x (RNOA - NBC). (RNOA - NBC) is the operating spread.
- RNOA = PM x ATO, PM = OI / sales, ATO = sales / average NOA.
- PM = sales PM + other-items PM. Sales PM = 1 - sum of expense ratios (each expense / sales).
- 1/ATO = sum of asset ratios (each operating asset or liability / sales), liabilities negative.
- Operating liability leverage: OLLEV = operating liabilities / NOA. RNOA = ROOA + OLLEV x (ROOA - short-term borrowing rate after tax), where ROOA = (OI + implicit after-tax interest on operating liabilities) / operating assets.
- Growth of CSE = ROCE + net investment rate (net share transactions / beginning CSE).
- Core vs unusual: OI = core OI from sales + core other OI + unusual items. RNOA = core RNOA + unusual items / NOA.
- Change in core RNOA is explained by: change in core sales PM at prior ATO, change in ATO at the new margin, change in other core income, change in unusual items.
- Operating leverage: contribution margin ratio = (sales - variable costs)/sales; % change in core OI = OLEV x % change in core sales, with OLEV = contribution margin / core OI.
- Payout: dividend payout = d / CI; retention = 1 - payout; total payout adds buybacks.

## 4. Valuation models (all equivalent if forecasts articulate)
- DDM: V_E = PV of expected dividends (+ terminal price).
- DCF: V_ops = sum over t of FCF_t / rho_F^t + CV/rho_F^T. V_E = V_ops - NFO_0.
- Residual operating income: ReOI_t = OI_t - r_F x NOA_{t-1}.
  V_ops = NOA_0 + sum ReOI_t/rho_F^t + CV; V_E = V_ops - NFO_0.
  CV (growth g after T) = ReOI_{T+1} / (r_F - g) discounted by rho_F^T. No-growth case: g = 0.
- Residual earnings (equity): RE_t = CI_t - r_E x CSE_{t-1}; V_E = CSE_0 + sum RE_t/rho_E^t + CV. Use only when leverage and r_E are stable; operating version is cleaner.
- Abnormal operating income growth (AOIG): cum-dividend OI_t = OI_t + r_F x FCF_{t-1}; AOIG_t = cum-div OI_t - rho_F x OI_{t-1} = ReOI_t - ReOI_{t-1}.
  V_ops = (1/r_F) x [OI_1 + AOIG_2/rho_F + AOIG_3/rho_F^2 + ...]; V_E = V_ops - NFO_0.
- Equity version: AEG_t = CI_t + r_E x d_{t-1} - rho_E x CI_{t-1}; V_E = (1/r_E)[CI_1 + AEG_2/rho_E + ...].
- Two-stage AOIG in multiplier form: V_ops = OI_1/r_F x (G_2 - G_long)/(rho_F - G_long), G_2 = cum-div OI_2 / OI_1 (gross), G_long = 1 + long-run growth. Needs G_2 > G_long.

## 5. Simple valuations (from current statements)
- No-growth: OI_1 = current core OI; V_ops = core OI / r_F.
- Growth at current RNOA: ReOI_1 = (core RNOA_0 - r_F) x NOA_0; V_ops = NOA_0 + (core RNOA_0 - r_F) x NOA_0 / (r_F - g), g = growth in NOA (or sales if ATO is stable).
- Fade growth toward long run: g = 0.7 x current growth in ReOI + 0.3 x long-run (GDP-like) growth.

## 6. Multiples
- Enterprise (unlevered) P/B = V_ops / NOA_0 = (market equity + net debt) / (book equity + net debt).
- Levered P/B = V_E / CSE_0. Levered P/B = unlevered P/B + FLEV x (unlevered P/B - 1).
- Normal forward P/E = 1 / r_E; normal trailing P/E = (1 + r_E) / r_E. Deviations from normal require expected abnormal earnings growth.
- PEG = forward P/E / one-year-ahead percentage earnings growth. Ignores dividends and cum-dividend adjustment; treat as a screen only.
- Unlevered P/sales, P/ebit, P/ebitda = (market equity + net debt) / metric.

## 7. Cost of capital
- r_F is a weighted average: rho_F = (V_E/V_ops) x rho_E + (V_D/V_ops) x rho_D, with rho_D after tax = 1 + nominal borrowing rate x (1 - tax rate), V_ops = V_E + V_D.
- Equivalent: r_E = r_F + (V_D/V_E) x (r_F - r_D). Leverage raises r_E; it does not add value by itself.
- Estimate r_E with CAPM or a ranged assumption; always sensitivity-test.

## 8. Reverse engineering
- Given price P, solve for the growth g (or required return) that makes V_E = P holding other forecasts fixed. The engine does this by bisection.
- Implied expected return: the discount rate that equates forecast payoffs to the price. Compare to the required return: the gap is the claimed mispricing, or the forecast error.
- Split: V = value supported by book and near-term forecasts + value of speculative growth.
