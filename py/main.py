from data import get_stock_choice, fetch_data
from analysis import calculate_spread
from signals import create_signals
from backtester import run_backtest
from report import create_report
import matplotlib.pyplot as plt

#data.py
user_tickers = get_stock_choice()
price_data = fetch_data(user_tickers)

#analysis.py
processed_data, hedge_ratio = calculate_spread(price_data)

if processed_data is not None:
    #add signals to DataFrame
    signals_data = create_signals(processed_data)
    
    #run backtester
    equity_curve = run_backtest(signals_data, hedge_ratio)

    #plot and calculate KPMs
    create_report(equity_curve)
    plt.show()

