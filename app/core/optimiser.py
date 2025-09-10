import numpy as np
from .pipeline import run_pipeline
#Allows backtester to loop through different parameter sets

def run_optimiser(
    tickers: str,
    time_period: str,
    initial_capital: float,
    trading_fees: float
) -> list:
    
    #define parameter ranges to test using numpy,
    #testing in windows from 30 to 120 days with intervals of 15
    window_range = np.arange(30, 121, 15)

    #test z score thresholds from 1.5 to 3.0 with intervals of 0.25
    threshold_range = np.arange(1.5, 3.1, 0.25)

    #init variables
    results_list = []
    total_runs = len(window_range) * len(threshold_range)
    nr_runs = 0


    #create nested loops to iterate through each param set
    for w in window_range:
        for t in threshold_range:
            nr_runs += 1
            print(f"Running backtest {nr_runs}/{total_runs}\n")
            print(f"Window:{w}\nThreshold:{t:.2f}")

            #call pipeline w/ curent param set
            kpm_dict, equity_curve = run_pipeline(
                tickers=tickers,
                time_period=time_period,
                initial_capital=initial_capital,
                trading_fees=trading_fees,
                z_window=w,
                z_threshold=t
            )

            #if successful, store results
            if kpm_dict:
                kpm_dict['z_window'] = w
                kpm_dict['z_threshold'] = t
                results_list.append(kpm_dict)

