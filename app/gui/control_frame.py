from tkinter import *
from tkinter import ttk

#Frame with user inputs

class ControlFrame(ttk.Frame):
    #constructor
    def __init__(self, master, run_callback, optimise_callback):
        super().__init__(master)
        self.run_callback = run_callback
        self.optimise_callback = optimise_callback
        self.add_widgets()
        

    #create widgets
    def add_widgets(self):
        #container for controls
        widgets_frame = ttk.LabelFrame(self)
        widgets_frame.grid(
            row=0, column=0, padx=10, pady=10, sticky="ew"
        )
        widgets_frame.columnconfigure(0, weight=1)
        widgets_frame.columnconfigure(1, weight=1)

        tickers_frame = ttk.Frame(widgets_frame)
        tickers_frame.grid(row=0, column=0, sticky="nsew")
        tickers_frame.columnconfigure(1, weight=1)
        #add widgets
        #tickers
        ticker_1_label = ttk.Label(tickers_frame, text="Ticker 1:")
        self.ticker_1_entry = ttk.Entry(tickers_frame)
        ticker_2_label = ttk.Label(tickers_frame, text="Ticker 2:")
        self.ticker_2_entry = ttk.Entry(tickers_frame)

        #geometry 
        ticker_1_label.grid(
            row=0, column=0,
            padx=5, pady=5, sticky='w'
        )
        self.ticker_1_entry.grid(
            row=0, column=1,
            padx=5, pady=5, sticky="ew"
        )
        ticker_2_label.grid(
            row=1, column=0,
            padx=5, pady=5, sticky='w'
        )
        self.ticker_2_entry.grid(
            row=1, column=1,
            padx=5, pady=5, sticky="ew"
        )
        

        #other options
        params_frame = ttk.Frame(widgets_frame)
        params_frame.grid(row=0, column=1, sticky="nsew")
        params_frame.columnconfigure(1, weight=1)

        self.time_period_entry = ttk.Combobox(
            params_frame,
            values=['5y', '10y', '15y', '20y']
        )
        time_period_label = ttk.Label(params_frame, text="Time Period:")
        capital_label = ttk.Label(params_frame, text="Starting Capital:")
        self.capital_entry = ttk.Entry(params_frame)
        fees_label = ttk.Label(params_frame, text="Trading Fees:")
        self.fees_entry = ttk.Entry(params_frame)

        time_period_label.grid(
            row=0, column=0, sticky='w',
            padx=5, pady=5
        )
        self.time_period_entry.grid(
            row=0, column=1, sticky='ew',
            padx=5, pady=5
        )
        capital_label.grid(
            row=1, column=0, sticky='w',
            padx=5, pady=5
        )
        self.capital_entry.grid(
            row=1, column=1, sticky='ew',
            padx=5, pady=5
        )
        self.capital_entry.insert(0, "100000")
        fees_label.grid(
            row=2, column=0, sticky='w',
            padx=5, pady=5
        )
        self.fees_entry.grid(
            row=2, column=1, sticky='ew',
            padx=5, pady=5
        )
        self.fees_entry.insert(0, "0.001")
        

        #buttons
        button_frame = ttk.Frame(widgets_frame)
        button_frame.grid(
            row=1, columnspan=2, pady=10
        )

        self.run_button = ttk.Button(
            button_frame,
            text="Run Backtest",
            command=self.run_callback
        )
        self.run_button.pack(side="left", padx=5)

        self.optimise_button = ttk.Button(
            button_frame,
            text="Run Optimisation",
            command=self.optimise_callback
        )
        self.optimise_button.pack(side="left", padx=5)

    



    #get str value of tickers inputted by user
    def get_tickers(self) -> tuple:
        ticker1 = self.ticker_1_entry.get()
        ticker2 = self.ticker_2_entry.get()
        return (ticker1, ticker2)
    
    #disable button
    def show_button(self, state: bool):
        if state is False:
            self.run_button.config(state="disabled")
            self.optimise_button.config(state="disabled")
        elif state is True:
            self.run_button.config(state="normal")
            self.optimise_button.config(state="normal")
    
    #get backtest params input
    def get_backtest_params(self) -> tuple:
        time_period: str = self.time_period_entry.get()
        starting_capital = self.capital_entry.get()
        trading_fees = self.fees_entry.get()
        return (time_period, starting_capital, trading_fees)
    
        





