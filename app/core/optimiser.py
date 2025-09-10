import numpy as np
import pandas as pd
from .pipeline import run_pipeline
#Allows backtester to loop through different parameter sets

#runs datasets through the pipeline to test parameter combinations
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

    #analyse all results and return the most optimal
    #for now, set to test for sharpe ratio
    optimal_params = analyse_results(
        results_list=results_list,
        optimise_for='sharpe_ratio'
    )

    return optimal_params



#Analyses list of backtest results to find best performing params
#Arg optimise_test: the metric to optimise for
def analyse_results(
        results_list: list,
        optimise_for: str
) -> pd.Series | pd.DataFrame:
    if not results_list:
        print("No backtest was run")
        return None
    
    #convert list of dicts into pandas Df
    results_df = pd.DataFrame(results_list)

    #find row w/ max value for chosen metric
    optimal_run_index = results_df[optimise_for].idxmax()
    optimal_run = results_df.loc[optimal_run_index]

    return optimal_run

