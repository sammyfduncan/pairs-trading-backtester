from tkinter import *
from tkinter import ttk
from .control_frame import ControlFrame
from core.data import get_stock_choice, fetch_data
from core.analysis import calculate_spread
from core.signals import create_signals
from core.backtester import run_backtest
from core.report import create_report
import matplotlib.pyplot as plt


#App class representing main window

class Application(Frame):

    def __init__(self, master):
        #call parent constructor
        super().__init__(master)
        self.master.title("Pairs Trading Backtester")
        #create component frames
        self.control_frame = ControlFrame(
            self, run_callback=self.handle_run_backtest)

        self.control_frame.pack(
            side="top", fill="x",
            padyx=10, pady=10)
        


    def handle_run_backtest(self):
        #get user inputs
        input_tickers = self.control_frame.get_tickers()
        
        #data.py
        price_data = fetch_data(input_tickers)

        #analysis.py
        processed_data, hedge_ratio = calculate_spread(price_data)
   
        if processed_data is not None:
            #add signals to DataFrame
            signals_data = create_signals(processed_data)
            
            #run backtester
            equity_curve = run_backtest(signals_data, hedge_ratio)

            #get KPMS
            create_report(equity_curve)
            






