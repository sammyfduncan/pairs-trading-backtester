import pandas as pd
import numpy as np

#Backtesting engine
#iterates through data and 'executes' hypothetical trades

def run_backtest(
        price_data: pd.DataFrame,
        hedge_ratio: float,
        starting_capital: str,
        trading_fees: str
        ) -> pd.Series:
    
    #define starting conditions of portfolio
    initial_capital = starting_capital
    cash = initial_capital
    position = 0 #flat
    #stores value of portfolio at end of each day
    equity_list = []

    asset1_shares = 0
    asset2_shares = 0

    #transaction cost 
    cost_pct = trading_fees


    #simulation loop
    for index, row in price_data.iterrows():

        #record daily PnL
        market_value = (
            asset1_shares * row['asset1'] +
            (asset2_shares * row['asset2'])
        )

        total_equity = cash + market_value
        equity_list.append(total_equity)
        
        #check signal
        target_pos = row['position']

        #execute trades
        #initially amount to invest set to 10k
        if position == 0 and target_pos == 1:
            #signal for opening long pos

            #determine how many shares to trade
            nr_asset1_shares =  10000 / row['asset1']
            nr_asset2_shares = nr_asset1_shares * hedge_ratio

            #update share holdings
            asset1_shares = nr_asset1_shares
            asset2_shares = -nr_asset2_shares
    
            #update cash 
            cash -= (asset1_shares * row['asset1'])
            cash += (nr_asset2_shares * row['asset2'])

            #include trading fees
            buy_cost = ((asset1_shares * row['asset1']) * cost_pct)
            sell_cost = ((nr_asset2_shares * row['asset2']) * cost_pct)
            cash -= (buy_cost + sell_cost)

            #update state 
            position = 1
        
        elif position == 0 and target_pos == -1:
            #signal for opening short pos, reverse of above

            nr_asset2_shares = 10000 / row['asset2']
            nr_asset1_shares = nr_asset2_shares * hedge_ratio

            asset1_shares = -nr_asset1_shares
            asset2_shares = nr_asset2_shares

            cash -= (asset2_shares * row['asset2'])
            cash += (nr_asset1_shares * row['asset1'])
            
            buy_cost = ((asset2_shares * row['asset2']) * cost_pct)
            sell_cost = ((nr_asset1_shares * row['asset1']) * cost_pct)
            cash -= (buy_cost + sell_cost)
            #short position
            position = -1

        elif position == 1 and target_pos != 1:
            #close long position

            #liquidate holdings, update vars
            cash += (asset1_shares * row['asset1'])
            cash += (asset2_shares * row['asset2'])

            #account for fees
            sell_cost = ((asset1_shares * row['asset1']) * cost_pct)
            buy_back_cost = ((abs(asset2_shares) * row['asset2']) * cost_pct)
            cash -= (sell_cost + buy_back_cost)

            #reset share holdings
            asset1_shares = 0
            asset2_shares = 0
            position = 0

        elif position == -1 and target_pos != -1:
            #closes short position

            cash += (asset1_shares * row['asset1'])
            cash += (asset2_shares * row['asset2'])

            sell_cost = ((asset2_shares * row['asset2']) * cost_pct)
            buy_back_cost = ((abs(asset1_shares) * row['asset1']) * cost_pct)
            cash -= (sell_cost + buy_back_cost)

            asset1_shares = 0
            asset2_shares = 0
            position = 0
    
    #convert equity list into series curve
    equity_curve = pd.Series(data=equity_list, index=price_data.index)

    return equity_curve
