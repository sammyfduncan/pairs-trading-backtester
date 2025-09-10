from .data import fetch_data
from .analysis import calculate_spread
from .signals import create_signals
from .backtester import run_backtest
from .report import create_report

#Run_pipeline executes entire backtest
def run_pipeline(
        tickers: tuple,
        time_period: str,
        initial_capital: float,
        trading_fees: float,
        z_window: int,
        z_threshold: float
) -> tuple:
    #fetch data
    price_data = fetch_data(tickers, time_period)
    if price_data is None:
        print("Failed to fetch data.")
        return (None, None)
    
    #check for cointegration and find spread
    processed_data, hedge_ratio = calculate_spread(price_data)
    if processed_data is None:
        print("Pair is not cointegrated.")
        return (None, None)
    
    #create signals 
    signals_data = create_signals(processed_data, z_window, z_threshold)

    #run backtest
    equity_curve = run_backtest(
        price_data=signals_data,
        hedge_ratio=hedge_ratio,
        starting_capital=initial_capital,
        trading_fees=trading_fees
    )

    #create performance report
    performance_data = create_report(equity_curve)
    
    #return output tuple
    return performance_data


