# Portfolio Optimization Tool

A standalone Python script that automates Modern Portfolio Theory (MPT) to find the maximum Sharpe/Sortino Ratio portfolio. It downloads historical data, calculates risk and return metrics, runs a bounded mathematical optimization, and outputs the final allocation summaries and charts.

## Key Features

* **Automated Data Fetching:** Uses `yfinance` to download historical daily closing prices.
* **Continuous Return Modeling:** Calculates daily returns via natural log (`np.log(prices / prices.shift(1))`) for accurate time-aggregation.
* **Risk-Adjusted Maximization:** Optimizes asset weights to maximize the Sharpe Ratio against a designated risk-free rate hurdle using `scipy.optimize.minimize`.
* **Built-in Constraints:** Enforces strict minimum and maximum allocation bounds per asset while ensuring total weights sum to exactly 100%.
* **Automated Artifact Generation:** Saves all foundational matrices, computed expected returns, raw historical prices, final portfolio summaries, and visual allocation pie charts to a structured local directory.

## Default Pipeline Parameters

* **Default Universe:** SPY, BND, GLD, QQQ, VTI
* **Default Window:** 2015-01-01 to 2025-10-23
* **Annualization Factor:** 252 trading days
* **Risk-Free Rate:** 4.0%
* **Asset Allocation Bounds:** Minimum 5%, Maximum 40%
