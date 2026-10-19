# Portfolio Optimization Tool (Sharpe Ratio)

An automated Python script that implements **Modern Portfolio Theory (MPT)** to find the optimal risk-adjusted asset allocation. The tool downloads historical price data via `yfinance` and utilizes numerical optimization (`scipy.optimize`) to maximize the **Sharpe Ratio** under customizable constraints.

## 🚀 Key Features

* **Automated Data Pipeline:** Downloads historical adjusted closing prices directly from [Yahoo Finance](https://finance.yahoo.com/).
* **Mathematical Optimization:** Employs the Sequential Least Squares Programming (`SLSQP`) algorithm to find the absolute highest Sharpe Ratio.
* **Risk Management Bounds:** Implements mandatory minimum and maximum weight floors/ceilings per asset to avoid over-concentration or total exclusion.
* **Visual Output:** Generates a publication-quality portfolio allocation pie chart and archives all underlying mathematical metrics to CSV files.

---

## 🛠️ Mathematical Implementation

### 1. Log Returns & Expected Returns
Rather than simple arithmetic returns, the tool uses **natural log returns** for historical asset scaling to ensure time-additive consistency:

$$	ext{Log Return} = \ln\left(rac{P_t}{P_{t-1}}
ight)$$

The annual expected return ($\mu$) for each asset is calculated by scaling the mean log return over the specified trading days ($252$):

$$\mu = e^{(\overline{	ext{Log Return}} 	imes 252)} - 1$$

### 2. Risk Metrics & Co-movements
The covariance matrix ($\Sigma$) and individual standard deviations ($\sigma$) are annualized using daily percentage changes:

$$\Sigma_{	ext{annual}} = \Sigma_{	ext{daily}} 	imes 252$$
$$\sigma_{	ext{annual}} = \sigma_{	ext{daily}} 	imes \sqrt{252}$$

### 3. Optimization Objective
The system minimizes the negative Sharpe Ratio, which mathematically maximizes the portfolio's excess return per unit of volatility relative to the risk-free rate ($R_f$):

$$\max w^T \mu - R_f \over \sqrt{w^T \Sigma w}$$

$$	ext{Subject to: } \sum w_i = 1 \quad 	ext{and} \quad w_{\min} \le w_i \le w_{\max}$$

---

## 📦 Directory Structure & Generated Artifacts

Upon running, the script creates a `results/` folder saving the following structured outputs:

```text
results/
├── allocation_pie.png              # High-DPI pie chart of optimal asset weights
├── portfolio_summary.csv           # Annual Return, Volatility, Sharpe Ratio, and Rf
├── optimal_weights.csv             # Final percentage allocations per ticker
├── annual_expected_returns.csv     # Individual asset calculated annual returns
├── annual_std_individual.csv       # Individual asset annualized volatilities
├── annual_cov_matrix.csv           # Final covariance matrix used in calculations
└── prices.csv                      # Cleaned and forward-filled historical price matrix
```

---

## 📋 Default Configuration Template

The pre-configured script executes the optimization with the following parameters:
* **Assets / Tickers:** `["SPY", "BND", "GLD", "QQQ", "VTI"]`
* **Historical Window:** `2015-01-01` to `2025-10-23`
* **Risk-Free Rate Hurdles ($R_f$):** `4.00%` (`0.04`)
* **Allocation Constraints:** Minimum `5.00%` and Maximum `40.00%` per individual asset.
