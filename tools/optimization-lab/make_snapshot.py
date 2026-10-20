"""Run once on your own machine: downloads prices to data/prices_fallback.csv."""
import datetime as dt
import engine as E

tickers = ["SPY", "BND", "GLD", "QQQ", "VTI"]
p = E.load_prices(tickers, "2010-01-01", str(dt.date.today()))
p.to_csv("data/prices_fallback.csv")
print(f"Saved {p.shape[0]} rows, {p.shape[1]} tickers -> data/prices_fallback.csv")
