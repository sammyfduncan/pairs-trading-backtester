from tkinter import *
from tkinter import ttk

class ControlFrame(ttk.Frame):
    def __init__(self, master, run_callback, optimise_callback):
        super().__init__(master)
        self.run_callback = run_callback
        self.optimise_callback = optimise_callback
        
        #Define widgets that need to be disabled during run
        self.disable_widgets = [] 

        self.add_widgets()

    def add_widgets(self):
        #Parameters frame
        params_frame = ttk.LabelFrame(self, text="Trade Parameters", padding=(10, 5))
        params_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        params_frame.columnconfigure(1, weight=1)

        #Tickers
        tickers_label = ttk.Label(params_frame, text="Ticker Pair:")
        tickers_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.tickers_entry = ttk.Entry(params_frame)
        self.tickers_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.tickers_entry.insert(0, "AAPL, MSFT")
        self.disable_widgets.append(self.tickers_entry)

        #time period
        time_period_label = ttk.Label(params_frame, text="Time Period:")
        time_period_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.time_period_entry = ttk.Combobox(params_frame, values=['5y', '10y', '15y', '20y'])
        self.time_period_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.time_period_entry.set('10y')
        self.disable_widgets.append(self.time_period_entry)

        # Config frame
        config_frame = ttk.LabelFrame(self, text="Backtest Configuration", padding=(10, 5))
        config_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        config_frame.columnconfigure(1, weight=1)

        #starting capital
        capital_label = ttk.Label(config_frame, text="Starting Capital:")
        capital_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.capital_entry = ttk.Entry(config_frame)
        self.capital_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.capital_entry.insert(0, "100000")
        self.disable_widgets.append(self.capital_entry)

        #Trading fees
        fees_label = ttk.Label(config_frame, text="Trading Fees:")
        fees_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.fees_entry = ttk.Entry(config_frame)
        self.fees_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.fees_entry.insert(0, "0.001")
        self.disable_widgets.append(self.fees_entry)

        #Execution frame
        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, pady=10)

        self.run_button = ttk.Button(button_frame, text="Run Backtest", command=self.run_callback)
        self.run_button.pack(side="left", padx=5)
        self.disable_widgets.append(self.run_button)

        self.optimise_button = ttk.Button(button_frame, text="Run Optimisation", command=self.optimise_callback)
        self.optimise_button.pack(side="left", padx=5)
        self.disable_widgets.append(self.optimise_button)

    def get_tickers(self) -> tuple:
        tickers_str = self.tickers_entry.get()
        tickers = [ticker.strip() for ticker in tickers_str.split(',')]
        return tuple(tickers)

    def set_controls_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        for widget in self.disable_widgets:
            widget.config(state=state)

    def get_backtest_params(self) -> tuple:
        time_period = self.time_period_entry.get()
        starting_capital = self.capital_entry.get()
        trading_fees = self.fees_entry.get()
        return (time_period, starting_capital, trading_fees)
