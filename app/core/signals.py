import pandas as pd
import numpy as np
#Adds trading signals to the DataFrame. 

#Takes analysed df and adds new cols with Z-score and signals
def create_signals(
        price_data: pd.DataFrame,
        z_window: int,
        z_threshold: float
        ) -> pd.DataFrame:
    

    #calculate Z-score:
    #find rolling mean/std deviation of spread col
    data_series = price_data['Spread'].rolling(window=z_window)
    mean = data_series.mean()
    std_dev = data_series.std()

    #z-score formula
    zscore = (price_data['Spread'] - mean) / std_dev

    #add it to a new col
    price_data = price_data.assign(ZScore=zscore)


    #create position signals
    #placeholders: -1 == short, 1 == long, 0 == flat 
    price_data['position'] = np.where(
        zscore > z_threshold,
        -1, #value if above true
        np.where(
            zscore < -z_threshold,
            1, #value if above true
            0 #value if false
        )
    )
    
    return price_data
