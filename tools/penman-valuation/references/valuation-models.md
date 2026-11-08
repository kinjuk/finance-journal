# Valuation models and how to use them

## Contents
1. Choosing the model
2. Equivalence and the consistency check
3. Residual operating income valuation in practice
4. Abnormal operating income growth in practice
5. DCF, and why it is the weakest anchor
6. Multiples (P/B, P/E, enterprise multiples)
7. Reverse engineering and active investing
8. Pitfalls
9. Asset-heavy firms where GAAP depreciation is not economic

## 1. Choosing the model
- Default: residual operating income (ReOI). It anchors value on book (NOA) and values only what is added beyond the required return, so less of the value sits in the long-run terminal.
- Cross-check with AOIG when the user thinks in earnings and earnings growth (common with analyst forecasts), or when you want to avoid forecasting FCF.
- DCF is for communication and as a check; it puts almost all value in the terminal when near-term FCF is depressed by investment.
- DDM only for mature payers; dividends are a policy choice, and the model hides value drivers.

## 2. Equivalence and consistency
With articulating forecasts, ReOI, AOIG and DCF give identical value. Build the pro forma once (OI and NOA by year, plus terminal assumption), compute all three, and display the gap. Gap should be rounding-sized. If not, the usual causes: terminal assumption inconsistent across methods (ReOI growing at g implies NOA growing at g and FCF_{T+1} = OI_{T+1} - g x NOA_T), beginning vs ending balances, pre/post-tax mix, or a missing year.

## 3. Residual operating income valuation
1. Reformulate; get NOA_0, NFO_0, minority interest, shares.
2. Forecast OI_t and NOA_t for T years.
3. ReOI_t = OI_t - r_F x NOA_{t-1}; PV at r_F.
4. Continuing value: ReOI_{T+1}/(r_F - g) with a justified g (long-run nominal growth or lower; zero if competitive advantage is expected to be fully competed away).
5. V_ops = NOA_0 + PV(ReOI) + PV(CV). V_E = V_ops - NFO_0 - minority interest - option overhang. Per share = V_E / shares.
6. Split the value: book value, PV of explicit ReOI, PV of continuing value. A large CV share means most of the value is speculation.

## 4. AOIG valuation
AOIG_t = ReOI_t - ReOI_{t-1} (the change in residual income). V_ops = (1/r_F)[OI_1 + sum AOIG_t/rho^{t-1}] with terminal AOIG growth g. Use when you have OI forecasts and want to see how much of the value is "capitalized next-year earnings" vs growth premium. Capitalizing forward earnings alone is the no-growth value; the extra is the price of growth.

## 5. DCF
V_ops = sum FCF_t/rho^t + CV; CV = FCF_{T+1}/(r_F - g). Use only after confirming FCF is consistent with growth (a firm growing at g must keep investing g x NOA). Terminal value dominating the total is the warning sign. Equity = V_ops - NFO_0 (and other claims).

## 6. Multiples
- P/B: levered P/B = V_E/CSE_0. A P/B above 1 requires expected positive residual income; below 1 requires expected negative. Enterprise P/B = (market equity + net debt)/(book equity + net debt) is the cleaner cross-firm comparison because it strips leverage.
- P/E: normal forward P/E = 1/r_E; above that requires abnormal earnings growth. PEG is a rough screen; it ignores dividends and risk.
- EV/sales, EV/ebit, EV/ebitda: only comparable across firms with similar margins, capital intensity and growth; treat as a sanity check, never a valuation by themselves.
- Method of comparables: multiples of "similar" firms only transfer when drivers (growth, RNOA, risk, accounting policy) are similar; otherwise explain the multiple with the drivers instead of copying it.

## 7. Reverse engineering and active investing
- Start from price. Compute the value supported by statements and near-term forecasts; the remainder is the value of speculative growth. Ask what growth rate, or what long-run RNOA, the market is paying for.
- Solve for implied g (and/or implied r_F) given the pro forma. Present: "At $P the market assumes X% perpetual growth in residual income / an expected return of Y%."
- Judge the implied assumption against history, industry fade, and sustainable growth. Too aggressive -> overpriced; conservative -> candidate for buying, subject to accounting quality.
- Index-level reverse engineering works the same way with aggregated statements.
- Fundamental investors protect against paying too much for growth: they pay for what is supported, treat growth beyond that as an option, and require a margin of safety proportional to the speculation.

## 8. Pitfalls
- Using market leverage for the book-based formulas (or vice versa) without being explicit.
- Applying an equity cost of capital to operating cash flows.
- Treating a point estimate as the answer; always show the range from required return +/- 1 and terminal growth +/- 1.
- Growth assumed above the economy's growth forever.
- Ignoring option overhang, minority interest, preferred stock, pensions or leases that change claims on operations.
- Starting from unadjusted earnings of a firm with poor accounting quality.

## 9. Asset-heavy firms where GAAP depreciation is not economic (REITs, net lease, infrastructure)
Symptom: GAAP RNOA sits near or below the cost of capital while pre-depreciation return is above it, and a standard ReOI valuation lands far from any sensible price.
1. Reformulate normally. Check RNOA before depreciation (OI after tax + D&A over average NOA) as well as after.
2. Make replacement spend explicit: phi = share of GAAP D&A that must actually be spent (or lost in value) to sustain cash flows. Land and tenant-maintained buildings push phi down; short leases, obsolescence and re-leasing costs push it up. It is a judgment: never present one value without the phi range.
3. Forecast FCF = EBITDA (after tax) - growth investment - phi x D&A; derive NOA by clean surplus (NOA + investment + replacement - D&A - impairments). Terminal: V_ops(T) = (EBITDA_{T+1} - phi x D&A_{T+1}) / (r - g). Pass it as `terminal_ops_value`.
4. Treat recurring "one-off" impairments net of gains as a core cost.
5. Deduct noncontrolling interests (consolidated funds and JVs mean NOA is 100% of assets you own part of), and flag unsettled forward equity.
6. Test whether external growth creates value: compare the unlevered after-tax yield on new investment with r_F and with (r_F - g). Growth funded at a yield below r_F adds AFFO/share but not value.
7. Cross-check with a dividend or AFFO-yield reverse engineering: price implies r_E = yield + growth.
Banks and insurers still need their own adaptation.
