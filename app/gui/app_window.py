import tkinter as tk 
from tkinter import ttk
from .control_frame import ControlFrame
from .plot_frame import PlotFrame
from app.core.data import fetch_data
from app.core.analysis import calculate_spread
from app.core.signals import create_signals
from app.core.backtester import run_backtest
from app.core.report import create_report
import matplotlib.pyplot as plt


#App class representing main window

class Application(ttk.Frame):

    def __init__(self, master):
        #call parent constructor
        super().__init__(master)
        self.master.title("Pairs Trading Backtester")
        #create component frames
        self.control_frame = ControlFrame(self, run_callback=self.handle_run_backtest)

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


        #data.py
        price_data = fetch_data(input_tickers, time_period)

        #analysis.py
        processed_data, hedge_ratio = calculate_spread(price_data)
   
        if processed_data is not None:
            #add signals to DataFrame
            signals_data = create_signals(processed_data)
            
            #run backtester
            equity_curve = run_backtest(
                signals_data,
                hedge_ratio,
                starting_capital,
                trading_fees
                )

            #get KPMS
            performance_data = create_report(equity_curve)

            #plot graph
            self.plot_frame.plot_graph(performance_data)

            #show button
            self.control_frame.show_button(True)








