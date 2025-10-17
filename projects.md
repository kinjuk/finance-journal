# Projects 📚

A log of on-going and upcoming projects.  
Helps me stay focused and mostly avoid idea loss.

---

## 🔄 On-going / Finished

### ▸ Momentum Strategy Research (MACD & RSI)  
Exploring momentum-based systems using MACD and RSI crossovers.  
Extending to assets like Gold, Bitcoin, and sector stocks to evaluate where these signals are most effective and where they fail.

### ▸ Finance-Journal Organization  
Sorting course notes, key concepts, essays and misc tools.  

### ▸ FX Interest Rate Arbitrage Calculator (Excel)  
Tool to compare net yields when switching between currencies (EUR → USD) based on central bank rates vs broker conversion costs and current FX rate.  
Calculates whether it's worth converting for yield advantages (as in 2% ECB vs 4% Fed).  
Add spot rate out and spot rate back.  
Add implied 1y forward spot rate (assuming normal market conditions where forward is expected above spot / backwardation scenarios excluded).  

### ▸ Beta (β) Calculator (Excel)  
Spreadsheet tool to calculate a stock’s beta relative to a benchmark index. Calculates 3y, 5y, and 10y betas using daily closing price data.
Implementing either Google Finance formulas as direct ticker reference in the sheet or imported CSV files fetched separately via Python (yfinance). "Easy vs Accurate" dilemma. 
Beta is calculated through slope function. A covariance method might be added in paralel to crosscheck the data.  
Tool currently functions throught pulled data from yfinance but google finance data is also shown side by side for comparison's sake.

### ▸ Order Types Flow & Trade Flow Notes  
Comprehensive overview of how trades progress through the market and how each order type shapes the execution flow.

### ▸ Demo Portfolio Log Book 
This repository is designed to exhaustively document and analyze every trading strategy deemed worth testing.  
Each idea is executed either manually, via API, or another method and recorded in detail, capturing positions, prices, timing, and outcomes.  
Over time, the accumulated data and statistics will reveal what works, what needs refinement, and what is unprofitable, while also highlighting good vs. bad instincts and decision-making patterns.  
Log Book + Notes will be available in due time.  

### ▸ Portfolio Optimization in Excel  
Step-by-step implementation of modern portfolio theory using Excel.  
Includes expected return, standard deviation, covariance matrix, and solver-based optimization.  
Dafault template built using SPY, BND, GLD, QQQ and VTI.
  
---

## 🗓️ Scheduled / To Come

### ▸ Portfolio Optimization in Python
Step-by-step implementation of Modern Portfolio Theory in Python.
Includes data download, return calculation, covariance matrix, optimizer (scipy most likely) for mean-variance or Sharpe-maximization, and reusable outputs (weights, expected return, volatility).  
Default universe is SPY, BND, GLD, QQQ and VTI.

### ▸ Portfolio Efficiency Comparison Tool  
Excel-based tool to evaluate and compare portfolio strategies using Sharpe, Sortino, and other risk-adjusted metrics.  
Identify the most efficient portfolio construction approach across different assets and optimizations.
