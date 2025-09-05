import yfinance as yf 
import pandas as pd
import numpy as np

#Acquires relevant data and prepares it into a DataFrame. 

def fetch_data(
        user_tickers: tuple,
        time_period: str
        ) -> pd.DataFrame:

    #first get our tickers
    ticker1, ticker2 = user_tickers[0], user_tickers[1]

    #download data from yfinance
    #data var is a DataFrame
    #period initially set to 5y
    data = yf.download(
        tickers=[ticker1, ticker2],
        period=time_period
    )

    #isolate closing price data
    price_data = data['Close'].copy()
    
    #check tickers found
    if len(price_data.columns) != 2:
        return None

    #rename tickers to generic name for consistency
    col_names = { price_data.columns[0]: 'asset1',
                  price_data.columns[1]: 'asset2'}

    price_data.rename(columns=col_names, inplace=True)

    #remove any missing entries in the data
    price_data.dropna(inplace=True)

    #return clean DataFrame
    return price_data




