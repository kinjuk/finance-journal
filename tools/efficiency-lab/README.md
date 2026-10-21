# Efficiency Lab
Enter a portfolio (tickers + %), set goal/horizon/risk, get a 0-100 diagnostic score, rule-based and optimizer what-if suggestions, and comparisons vs benchmarks, famous model portfolios and 13F investors.

    pip install -r requirements.txt
    streamlit run app.py

## 13F investors
Download a quarterly zip from the SEC "Form 13F Data Sets" page, upload it in the sidebar (13F investor data → Process).
The app extracts the tracked investors (edit `INVESTORS` in `engine.py`), maps CUSIPs to tickers via OpenFIGI, and writes
`data/investors_13f.csv` + `data/cusip_map.csv`. Download both and commit them so they persist on Streamlit Cloud.
If mapping stops (OpenFIGI rate limit), press Process again: it resumes.

## Data problems (crypto, mutual funds)
"Skip assets with data problems" (sidebar, on by default) drops assets with <1 year of data and renormalises weights.
