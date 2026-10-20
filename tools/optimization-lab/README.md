# Optimization Lab
Streamlit dashboard: Sharpe / Sortino / Min-vol optimizers, efficient frontier, constraint diagnostics, backtest, projection.

Live app: https://opt-lab.streamlit.app/

## Run
    pip install -r requirements.txt
    streamlit run app.py

## Deploy (free)
Push to GitHub → share.streamlit.io → New app → select repo, main file `app.py`.

## Rate-limit fallback
yfinance gets throttled on shared hosts. Run `python make_snapshot.py` once locally, then commit `data/prices_fallback.csv`.

## Layout
- `engine.py` – estimation, optimizers, frontier (no UI imports; testable)
- `app.py` – dashboard

## Caveats
All results are in-sample historical estimates. Estimator "Legacy log-mean" reproduces the original script (Sharpe 0.784); the default arithmetic estimator is consistent with the covariance and will give different numbers.
