from tkinter import *
from tkinter import ttk

#Frame with user inputs

class ControlFrame(ttk.Frame):
    #constructor
    def __init__(self, master, run_callback):
        super().__init__(master)
        self.run_callback = run_callback
        self.add_widgets()
        

    #create widgets
    def add_widgets(self):
        #container for controls
        widgets_frame = ttk.LabelFrame(self, text="Controls")
        widgets_frame.grid(
            row=0, column=0, padx=10, pady=10, sticky="ew"
        )
        widgets_frame.columnconfigure(1, weight=1)

        #add widgets
        #tickers
        ticker_1_label = ttk.Label(widgets_frame, text="Ticker 1:")
        self.ticker_1_entry = ttk.Entry(widgets_frame)
        ticker_2_label = ttk.Label(widgets_frame, text="Ticker 2:")
        self.ticker_2_entry = ttk.Entry(widgets_frame)

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

        #run button
        self.run_button = ttk.Button(
            widgets_frame,
            text="Run Backtest",
            command=self.run_callback
        )
        self.run_button.grid(row=2, columnspan=2,pady=10)

    



    #get str value of tickers inputted by user
    def get_tickers(self) -> tuple:
        ticker1 = self.ticker_1_entry.get()
        ticker2 = self.ticker_2_entry.get()
        return (ticker1, ticker2)
    
    #disable button
    def show_button(self, state: bool):
        if state is False:
            self.run_button.config(state="disabled")
        elif state is True:
            self.run_button.config(state="normal")
    

        





