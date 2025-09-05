from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#Frame for displaying matplotlib

class PlotFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        #creates canvas for plot
        self.figure = Figure(figsize=(12, 6), dpi=100)
        
        #this is area to draw lines on
        self.ax = self.figure.add_subplot(111)
        
        #create tkinter bridge to matplotlib
        self.canvas = FigureCanvasTkAgg(self.figure, self)

        #display canvas
        self.canvas.get_tk_widget().pack(
            side="top", fill="both", expand=True
        )

    #public method to update chart
    def plot_graph(self, report_data: tuple):
        #clear any old plot
        self.ax.clear()

        #format args data 
        #0-report Str, 1-equity curve
        report_str = report_data[0]
        equity_curve_plot = report_data[1]

        #plot graph
        self.ax.plot(equity_curve_plot, label="Portfolio Value")
        self.ax.set_title(f"{report_str}")
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Value")
        self.ax.grid(True)
        self.ax.legend()
        #draw on the canvas
        self.canvas.draw()
