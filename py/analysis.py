from statsmodels.tsa.stattools import coint
import numpy, pandas


#Mathematically checks for cointegration between given pairs
#If proven, calculates spread

def calculate_spread(price_data: pandas.DataFrame):

    #first, check for cointegration using statsmodels
    tmp = coint(
        price_data['asset1'],
        price_data['asset2'])
    
    #tuple index 1 represents p-value 
    p_value = tmp[1]
    
    #if cointegrated, proceed, else halt
    #initial value set to 0,05
    if p_value < 0.05:
        pass
    else:
        print('Pair is not cointegrated.')
        return None


    #calculate hedge ratio by performing linear regression
    tmp = numpy.polyfit(
        price_data['asset2'],
        price_data['asset1'],
        deg=1
    )

    #slope (hedge ratio) is first value returned from polyfit
    hedge_ratio = tmp[0]

    #create new time series representing spread
    #formula:
    spread = price_data['asset1'] - (hedge_ratio * price_data['asset2'])
    #assign to a new col
    price_data = price_data.assign(Spread=spread)
    
    return price_data
