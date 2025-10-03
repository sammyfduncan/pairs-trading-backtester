import pandas as pd
import numpy as np

#Backtesting engine
#iterates through data and 'executes' hypothetical trades

def run_backtest(
        price_data: pd.DataFrame,
        hedge_ratio: float,
        starting_capital,
        trading_fees
        ) -> pd.Series:
    
    #calculate number of shares to hold for each asset based on the signal
    price_data['asset1_holdings'] = (10000 / price_data['asset1']) * price_data['position']
    price_data['asset2_holdings'] = -((10000 / price_data['asset1']) * price_data['position']) * hedge_ratio

    #calculate market value of the portfolio for each day
    price_data['portfolio_value'] = (price_data['asset1_holdings'] * price_data['asset1']) + \
                                  (price_data['asset2_holdings'] * price_data['asset2'])

    #calculate daily profit and loss of the portfolio
    price_data['pnl'] = price_data['portfolio_value'].diff()

    #calculate the cost of trading 
    #trade occurs when the holdings change from the previous day 
    price_data['asset1_trades'] = price_data['asset1_holdings'].diff()
    price_data['asset2_trades'] = price_data['asset2_holdings'].diff()

    price_data['trading_costs'] = (price_data['asset1_trades'].abs() * price_data['asset1'] * trading_fees) + \
                                  (price_data['asset2_trades'].abs() * price_data['asset2'] * trading_fees)

    #calculate the final equity curve
    price_data['net_pnl'] = price_data['pnl'] - price_data['trading_costs']
    equity_curve = starting_capital + price_data['net_pnl'].cumsum()
    equity_curve.iloc[0] = starting_capital

    return equity_curve
