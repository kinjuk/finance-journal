# penman-valuation

A Claude skill for accounting-based equity valuation, following the framework in Stephen Penman's *Financial Statement Analysis and Security Valuation* (5th ed.).

It walks a valuation end to end: reformulate the statements (operating vs financing), analyze profitability (RNOA, margin, turnover, leverage), test accounting quality, build pro forma forecasts, value with residual operating income / abnormal operating income growth / DCF, and reverse-engineer what the market price implies.

## Contents

- `SKILL.md` - principles, workflow, output rules and pre-presentation checks (the file Claude reads).
- `references/` - formulas, reformulation, analysis and forecasting, accounting quality, valuation models, risk and credit.
- `scripts/valuation_engine.py` - ReOI / AOIG / DCF with a consistency check, implied-growth solver, sensitivity grid.

## Engine

```
python scripts/valuation_engine.py value input.json
python scripts/valuation_engine.py implied-growth input.json   # needs "price" and "shares"
python scripts/valuation_engine.py sensitivity input.json
```

Input fields are documented at the top of the script. For assets whose GAAP depreciation is not economic (REITs, net lease), pass `terminal_ops_value`; see `references/valuation-models.md` section 9.

## Notes

- The skill contains the method distilled in original wording. It does not reproduce text from the book.
- Analysis tool, not personalised investment advice. Banks, insurers and early-stage companies need adaptation.
