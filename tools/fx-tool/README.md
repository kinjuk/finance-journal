# FX Interest Arbitrage Calculator

Compares net yield when switching currencies (for example EUR to USD) on the interest gap, such as 2% ECB against 4% Fed, after broker conversion costs. Shows whether the yield advantage survives the fee and the spot rates you assume out and back. A carry trade aid.

**Live app:** https://fxtool.streamlit.app/

Python port of the Excel version (`FX Arbitrage Tool.xlsx`) in this repo. Rates are entered by hand; the tool doesn't pull live data.

## How it works

Route A keeps the capital in A and earns A's interest. Route B converts at the outbound spot rate less the broker fee, earns B's interest over the holding period, then converts back at the return spot rate. The net advantage is Route B minus Route A, both in A.

```
net FX rate        = spot out x (1 - fee)
converted capital  = capital x net FX rate
B yield            = converted capital x (B rate x days / 365)
final B value      = converted capital + B yield
back in A          = final B value / spot back
A yield            = capital x (A rate x days / 365)
final A value      = capital + A yield
net advantage      = back in A - final A value
```

Inputs: A and B interest rates, outbound and return A/B spot rates, broker fee, holding period in days, and initial capital in A. Rates and the fee are entered as percentages.

## Assumptions and limits

- Interest is simple, not compounded.
- The broker fee is charged once, on the outbound conversion, as in the Excel. An optional switch also applies it on the way back. On the default inputs that moves the net advantage from 12.98 to 7.82.
- Both spot rates are fixed inputs. The tool doesn't model the exchange-rate risk between the two conversions, the bid/ask spread or taxes. In practice that risk can erase the interest gap, so read the result as a best case.
- Educational tool. Not financial advice.

## Run locally

```
pip install -r requirements.txt
streamlit run app.py
```

`app.py` is the interface. `fx_arbitrage.py` holds the calculation.
