import tkinter as tk 
from tkinter import ttk
from .control_frame import ControlFrame
from .plot_frame import PlotFrame
from app.core.pipeline import run_pipeline
from app.core.optimiser import run_optimiser
import matplotlib.pyplot as plt


#App class representing main window

class Application(ttk.Frame):

    def __init__(self, master):
        #call parent constructor
        super().__init__(master)
        self.master.title("Pairs Trading Backtester")
        #create component frames
        self.control_frame = ControlFrame(
            self,
            run_callback=self.handle_run_backtest,
            optimise_callback=self.handle_run_optimisation
            )

        self.plot_frame = PlotFrame(self)

        self.control_frame.pack(
            side="top", fill="x", expand=False,
            padx=10, pady=5)
        
        self.plot_frame.pack(
            side="top", fill="both", expand=True
        )

        #make visible
        self.pack(fill="both", expand=True)

    def handle_run_backtest(self):
        #hide run button
        self.control_frame.show_button(False)
        
        #get user inputs
        input_tickers = self.control_frame.get_tickers()
        backtest_params = self.control_frame.get_backtest_params()
        time_period = backtest_params[0]
        starting_capital = backtest_params[1]
        trading_fees = backtest_params[2]

        #default if user doesn't enter anything
        default_capital = 100000.0
        default_fees = 0.001
        default_period = '10y'

        default_z_window = 60
        default_z_threshold = 2.0

        try:
            if starting_capital.strip():
                initial_capital = float(starting_capital)
            else:
                initial_capital = default_capital
        except ValueError:
            print(f"Invalid capital input {starting_capital}")
            initial_capital = default_capital
    
        try:
            if trading_fees.strip():
                initial_fees = int(float(trading_fees))
            else:
                initial_fees = default_fees
        except ValueError:
            print(f"Invalid fee input {trading_fees}")
            initial_fees = default_fees
    
        if time_period:
            initial_period = time_period
        else:
            initial_period = default_period

        #call pipeliine function
        performance_data = run_pipeline(
            tickers=input_tickers,
            time_period=initial_period,
            initial_capital=initial_capital,
            trading_fees=initial_fees,
            z_window=default_z_window,
            z_threshold=default_z_threshold
        )

        kpm_dict = performance_data[0]
        equity_curve = performance_data[1]

        if kpm_dict and equity_curve is not None:
            #format dict into a str
            report_str = (
                f"Total Return: {kpm_dict['total_return']:.2f}% | "
                f"Sharpe Ratio: {kpm_dict['sharpe_ratio']:.2f} | "
                f"Max Drawdown: {kpm_dict['max_drawdown']:.2f}%"
            )
            #call plot function passing above data as tuple
            self.plot_frame.plot_graph((report_str, equity_curve))

        #show button
        self.control_frame.show_button(True)

    #handles calls to optimisation function
    def handle_run_optimisation(self):
        #disable buttons
        self.control_frame.show_button(False)

        #get user inputs
        input_tickers = self.control_frame.get_tickers()
        backtest_params = self.control_frame.get_backtest_params()
        time_period = backtest_params[0]
        starting_capital = backtest_params[1]
        trading_fees = backtest_params[2]

        #default
        default_capital = 100000.0
        default_fees = 0.001
        default_period = '10y'

        try:
            if starting_capital.strip():
                initial_capital = float(starting_capital)
            else:
                initial_capital = default_capital
        except ValueError:
            print(f"Invalid capital input {starting_capital}")
            initial_capital = default_capital
    
        try:
            if trading_fees.strip():
                initial_fees = int(float(trading_fees))
            else:
                initial_fees = default_fees
        except ValueError:
            print(f"Invalid fee input {trading_fees}")
            initial_fees = default_fees
    
        if time_period:
            initial_period = time_period
        else:
            initial_period = default_period


        #call optimisation engine
        optimal_params = run_optimiser(
            tickers=input_tickers,
            time_period=initial_period,
            initial_capital=initial_capital,
            trading_fees=initial_fees
        )

        #if result was found, run pipeline again with it
        if optimal_params is not None:
            optimal_window = int(optimal_params['z_window'])
            optimal_threshold = optimal_params['z-threshold']

        #rerun backtest w/ optimal params to get equity curve
        kpm_dict, equity_curve = run_pipeline(
            tickers=input_tickers,
            time_period=initial_period,
            initial_capital=initial_capital,
            trading_fees=initial_fees,
            z_window=optimal_window,
            z_threshold=optimal_threshold
        )

        if kpm_dict and equity_curve is not None:
            report_str = (
                f"Optimal Window: {optimal_window}, Threshold: {optimal_threshold:.2f} | "
                f"Sharpe: {kpm_dict['sharpe_ratio']:.2f} | "
                f"Return: {kpm_dict['total_return']:.2f}%"
            )
            #plot graph
            self.plot_frame.plot_graph((report_str, equity_curve))

        self.control_frame.show_button(True)




