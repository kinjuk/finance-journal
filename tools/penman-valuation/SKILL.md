---
name: penman-valuation
description: Value a company or stock with accounting-based fundamental analysis (Penman's framework) - reformulate the financial statements into operating vs financing, decompose profitability (RNOA, margin, turnover, leverage), test accounting quality, build pro forma forecasts, value with residual operating income / abnormal earnings growth / DCF, reverse-engineer what a market price implies, and run sensitivities. Use this skill whenever the user wants intrinsic value, a buy/sell/overpriced view, a valuation model or spreadsheet, financial statement analysis, ROCE/RNOA/net operating assets, residual earnings, abnormal earnings growth, a justified P/B or P/E, a check on earnings quality or manipulation, or a credit/risk read from the statements - even if they never say "Penman" or "fundamental analysis".
---

# Accounting-based valuation (Penman framework)

Purpose: turn a set of financial statements into a defensible intrinsic value, and show exactly which assumptions the value rests on. The framework's edge is discipline: value what the statements support, price the speculation separately, and challenge the market price instead of trusting it.

## Principles (why the steps below exist)

1. **Anchor on what is known, price the speculation separately.** Book value plus near-term forecasts is hard information; long-run growth is soft. Keep them apart so the user can see how much of a price is speculation.
2. **Reformulate before analyzing.** GAAP/IFRS statements mix operating and financing activity. Profitability, growth and value drivers only become visible after splitting them (net operating assets vs net financial obligations; operating income vs financing expense).
3. **Value = book value + PV of residual operating income** (equivalently abnormal earnings growth, or DCF). The three must agree when the forecasts articulate. A mismatch means an arithmetic or consistency error, never a "modelling difference".
4. **Accounting quality caps forecast quality.** Forecasts anchor on reported numbers, so test those numbers before leaning on them.
5. **Reverse-engineer the price.** Ask what growth/profitability the market price implies, then judge whether that is plausible. This is usually more useful than a point estimate.
6. **Never invent inputs.** Real statements, price, share count and required return are needed. If missing, ask, or fetch from filings with search/fetch tools. State every assumption you make.

## Workflow

Run only the stages the request needs. A "quick take" may be stages 1, 4 (simple), 5, 6. A full valuation is all of them.

**0. Scope.** Pin down: company, statements available (years, currency, US GAAP vs IFRS), price date, share count, whether the user wants a quick or full valuation, and the output form (chat / Excel / report). Ask at most one clarifying question; otherwise state assumptions and proceed.

**1. Reformulate the statements** -> read `references/reformulation.md`. Produce reformulated balance sheet (NOA, NFO, CSE), income statement (operating income after tax, net financial expense, comprehensive income), cash flow (free cash flow), and equity statement. Run the articulation checks at the end of that file before moving on.

**2. Analyze profitability and growth** -> read `references/analysis-and-forecasting.md` (analysis half). Compute RNOA, PM, ATO, FLEV, spread, ROCE; separate core from unusual items; decompose change in RNOA; look at operating leverage and sustainable growth. Compare against the firm's own history and peers if available.

**3. Test accounting quality** -> read `references/accounting-quality.md`. Identify policy (conservative/liberal/neutral), run the diagnostics that fit the business, normalize operating income where needed. Quality findings change the numbers you forecast from, so do this before step 4.

**4. Forecast** -> `references/analysis-and-forecasting.md` (forecasting half).
- *Simple* (mature, stable firms): forecast from current core RNOA and NOA growth, optionally fade toward long-run growth.
- *Full* (everything else): sales -> margin -> operating income; asset turnover -> NOA; then financing, dividends, equity. The template there has the exact steps.
- Forecast operating drivers, not the valuation. Assume fade: high RNOA and high growth decay toward norms unless there is a specific, durable competitive reason.

**5. Value** -> `references/valuation-models.md` and `references/formulas.md`. Use `scripts/valuation_engine.py` for the arithmetic and the three-way consistency check (ReOI vs AOIG vs DCF). Value operations, subtract net financial obligations, adjust for minority interest and option overhang, divide by diluted shares. Cost of capital for operations must be consistent with the leverage in the valuation (see formulas).

**6. Challenge the price** -> reverse-engineer implied growth (engine: `implied-growth`) and implied required return. Run sensitivity on the 2-3 inputs that matter most (usually required return, terminal growth, long-run RNOA/margin). Split the price into "supported by statements and near-term forecasts" vs "speculative growth".

**7. Risk / credit (only if asked)** -> `references/risk-and-return.md`.

## Output

Lead with the conclusion: intrinsic value per share vs price, and the verdict that follows. Then the 2-3 assumptions the verdict hinges on, then supporting numbers. No hedging filler; if the answer depends on one input, say which and give both outcomes.

- **Chat:** compact tables for reformulated statements and the valuation; show formulas used for any non-obvious number.
- **Excel:** use the xlsx skill. Layout: Inputs sheet (all assumptions, colour-coded), Reformulated statements, Analysis (ratios and decomposition), Pro forma, Valuation (live formulas for ReOI, AOIG and DCF side by side with a check cell that must be ~0), Reverse engineering, Sensitivity. No hard-coded numbers in formula cells.
- **Written report:** use the docs/docx guidance available in the session. Structure: verdict, business and strategy, reformulated results, quality findings, forecasts and valuation, what the price implies, sensitivities, risks.

End valuation outputs with one line noting this is analysis, not personalised investment advice.

## Checks before you present numbers

- Reformulated CSE from the balance sheet equals CSE rolled forward (beginning + comprehensive income - net dividends). Free cash flow computed from operations equals the sum of financing flows.
- ReOI, AOIG and DCF values agree (the engine reports the gap).
- Beginning-of-period balances drive residual income, not ending balances.
- Operating income is after tax, with tax reallocated between operations and financing. Mixed pre/post-tax inputs are the most common silent error.
- Terminal growth is at or below long-run nominal growth of the economy the cash flows are in; justify anything higher explicitly.
- Required return is a rough estimate. Show how the value moves for +/-1 point before calling anything cheap or expensive.
- Units and currency consistent; shares are diluted; minority interest, preferred stock and option overhang are handled, not ignored.
- Depreciation test: the default terminal assumes GAAP depreciation is reinvested 1:1 forever. For real estate, net-lease and other assets whose value does not decay like their book value, that destroys value spuriously (a worked REIT case came out at ~$15 vs a $59 price). Forecast replacement spend explicitly, pass `terminal_ops_value` to the engine, and show value across the share of GAAP depreciation that is truly economic. See `references/valuation-models.md` section 9.
- Valuation of a firm with negative or tiny book, deep losses, or mostly speculative prospects: say the framework gives little anchor and what you did instead.

## When this skill is not enough

Banks, insurers and other financial institutions need a different operating/financing split (their "financing" is the business); say so and adapt rather than forcing the industrial template. Start-ups with no earnings history: the anchor is thin, lean on scenario analysis and reverse engineering.
