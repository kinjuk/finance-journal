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
Calculates whether it's worth converting for yield advantages (as in 2% ECB vs 4% Fed). Carry Trade aid.  
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
  
### ▸ Portfolio Optimization in Python
Step-by-step implementation of Modern Portfolio Theory in Python.  
Includes data download, return calculation, standard deviation, covariance matrix, optimizer (scipy) for Sharpe-maximization. 
Default universe is SPY, BND, GLD, QQQ and VTI.

### ▸ Portfolio Efficiency Comparison Tool  
Excel-based tool to evaluate and compare portfolio strategies using Sharpe, Sortino, and other risk-adjusted metrics.  
Identify the most efficient portfolio construction approach across different assets and optimizations.  

### ▸ Valuation Models (Excel)
Develop multiple fair value estimation models, including DCF, Dividend Discount, etc.
Each model outputs intrinsic value per share.
Models are applied to certain equities which gives dated valuation snapshots and will be stored accordingly in the "market-analysis" repository.  
Contextual factors such as macro, market sentiment, pertinent news, technical/charting observations, and general analytical notes are documented inside the spreadsheet to provide aditional and/or necessary assumptions and information.



---

## 🗓️ Scheduled / To Come

### ▸ Portfolio Efficiency Comparison Tool  
Excel-based tool to evaluate and compare portfolio strategies using Sharpe, Sortino, and other risk-adjusted metrics.  
Identify the most efficient portfolio construction approach across different assets and optimizations.  
  
### ▸ IBKR API Integration (TWS + Python)
Setup of the Interactive Brokers API through TWS using Python for data access, strategy testing, and automated paper trading.
Intended as a long-term replacement for current demo backtesting methods, providing a more reliable and algorithm-driven framework once fully implemented.
