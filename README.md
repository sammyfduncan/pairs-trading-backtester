### Pairs Trading Backtester

A python based application to backtest and optimise a statistical arbitrage pairs trading strategy, implemented with libraries such as Pandas, NumPy, yfinance and Tkinter.

Users can test the historical performance of a mean reversion strategy on any pair of equities to find the optimal trading parameters and generate a performance report. 

**Features:**

- Statistical validation of a relationship between two assets through the use of an automated Engle-Granger cointegration test
- Can quickly run a single backtest using default parameters to identify a strategy's equity curve
- More advanced parameter optimisation mode where a range of Z-Score lookback windows and entry/exit thresholds are analysed to find the parameters with the highest Sharpe Ratio
- Interactive portfolio equity curve display with Matplotlib

