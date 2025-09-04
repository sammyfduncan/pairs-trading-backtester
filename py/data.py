import yfinance
import pandas
import numpy

#Acquires relevant data and prepares it into a DataFrame. 

def fetch_data(user_tickers: tuple):

    #first get our tickers
    ticker1, ticker2 = user_tickers[0], user_tickers[1]

    #download data from yfinance
    #data var is a DataFrame
    #period initially set to 5y
    data = yfinance.download(
        tickers=[ticker1, ticker2],
        period='5y'
    )

    #isolate closing price data
    price_data = data['Close'].copy()
    
    #rename tickers to generic name for consistency
    col_names = { price_data.columns[0]: 'asset1',
                  price_data.columns[1]: 'asset2'}

    price_data.rename(col_names, inplace=True)

    #remove any missing entries in the data
    price_data.dropna(inplace=True)

    #return clean DataFrame
    return price_data


def get_stock_choice() -> tuple:
    
    ticker1: str = input(
        "Enter the first stock/ticker symbol:\n"
        ).upper()

    ticker2: str = input(
        "Enter the second stock/ticker symbol:\n"
        ).upper()
    
    return (ticker1, ticker2)




