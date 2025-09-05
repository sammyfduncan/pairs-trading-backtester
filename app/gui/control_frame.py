from tkinter import *
from tkinter import ttk
from app_window import Application

#Frame with user inputs

class ControlFrame(ttk.Frame):
    #constructor
    def __init__(
            self,
            master = None, *,
            border = ..., borderwidth = ...,
            class_ = "", cursor = "",  
            height = 0, name = ...,
            padding = ..., relief = ...,
            style = "", takefocus = "",
            width = 0, run_callback = ...
            ):
        super().__init__(
            master, border=border, borderwidth=borderwidth, class_=class_,
            cursor=cursor, height=height, name=name, padding=padding, relief=relief,
            style=style, takefocus=takefocus, width=width)
        
        
    #create widgets
    def add_widgets(self):
        #container for controls
        widgets_frame = ttk.LabelFrame(self, text="Controls")
        widgets_frame.grid()
        #add widgets
        #tickers
        ticker_1_label = ttk.Label(text="Ticker 1:").grid(
            row=0, column=0,
            padx=5, pady=5, sticky='w'
        )
        self.ticker_1_entry = ttk.Entry(...).grid(
            row=0, column=1,
            padx=5, pady=5
        )
        ticker_2_label = ttk.Label(text="Ticker 2:").grid(
            row=1, column=0,
            padx=5, pady=5, sticky='w'
        )
        self.ticker_2_entry = ttk.Entry(...).grid(
            row=1, column=1,
            padx=5, pady=5
        )
        #run button
        run_button = ttk.Button(
            text="Run Backtest",
            command=self.handle_run_backtest()
        ).grid(row=2, columnspan=2,pady=10)


    #get str value of tickers inputted by user
    def get_tickers(self) -> tuple:
        ticker1 = self.ticker_1_entry.get()
        ticker2 = self.ticker_2_entry.get()
        return (ticker1, ticker2)
    


        





