import tkinter as tk 
from tkinter import ttk
import tkinter.messagebox as messagebox
import matplotlib.pyplot as plt
import webbrowser
import os
from .control_frame import ControlFrame
from .plot_frame import PlotFrame
from app.core.pipeline import run_pipeline
from app.core.optimiser import run_optimiser
from app.core.report import create_detailed_report
from app.core.exceptions import CointegrationError, DataFetchError



#App class representing main window

class Application(ttk.Frame):

    def __init__(self, master):
        #call parent constructor
        super().__init__(master)
        self.master.title("Pairs Trading Backtester")

        #set theme
        style = ttk.Style(self.master)
        style.theme_use('clam')

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

    def _get_validated_inputs(self):
        try:
            input_tickers = self.control_frame.get_tickers()
            if len(input_tickers) != 2:
                messagebox.showerror("Invalid Tickers", "Please provide exactly two tickers, separated by a comma.")
                return None

            backtest_params = self.control_frame.get_backtest_params()
            time_period = backtest_params[0]
            starting_capital = backtest_params[1]
            trading_fees = backtest_params[2]

            default_capital = 100000.0
            default_fees = 0.001
            default_period = '10y'

            if starting_capital.strip():
                initial_capital = float(starting_capital)
            else:
                initial_capital = default_capital
        
            if trading_fees.strip():
                initial_fees = float(trading_fees)
            else:
                initial_fees = default_fees
        
            if time_period:
                initial_period = time_period
            else:
                initial_period = default_period

            return input_tickers, initial_period, initial_capital, initial_fees

        except ValueError:
            messagebox.showerror("Invalid Input", "Starting capital and trading fees must be numbers.")
            return None

    def handle_run_backtest(self):
        self.control_frame.set_controls_enabled(False)
        
        try:
            validated_inputs = self._get_validated_inputs()
            if validated_inputs is None:
                return

            input_tickers, initial_period, initial_capital, initial_fees = validated_inputs

            default_z_window = 60
            default_z_threshold = 2.0

            #call pipeliine function
            performance_data = run_pipeline(
                tickers=input_tickers,
                time_period=initial_period,
                initial_capital=initial_capital,
                trading_fees=initial_fees,
                z_window=default_z_window,
                z_threshold=default_z_threshold
            )

            kpm_dict, equity_curve = performance_data

            if kpm_dict and equity_curve is not None:
                #format dict into a str
                report_str = (
                    f"Total Return: {kpm_dict['total_return']:.2f}% | "
                    f"Sharpe Ratio: {kpm_dict['sharpe_ratio']:.2f} | "
                    f"Max Drawdown: {kpm_dict['max_drawdown']:.2f}%"
                )
                #call plot function passing above data as tuple
                self.plot_frame.plot_graph((report_str, equity_curve))

        except (DataFetchError, CointegrationError) as e:
            messagebox.showerror("Backtest failed", str(e))
        except Exception as e:
            messagebox.showerror("An unexpected error occurred", str(e))
        finally:
            self.control_frame.set_controls_enabled(True)

    #handles calls to optimisation function
    def handle_run_optimisation(self):
        self.control_frame.set_controls_enabled(False)
        try:
            validated_inputs = self._get_validated_inputs()
            if validated_inputs is None:
                return

            input_tickers, initial_period, initial_capital, initial_fees = validated_inputs

            #call optimisation engine
            optimal_params = run_optimiser(
                tickers=input_tickers,
                time_period=initial_period,
                initial_capital=initial_capital,
                trading_fees=initial_fees
            )

            #if no result, show error
            if optimal_params is None or optimal_params.empty:
                messagebox.showerror(
                    "Optimisation failed",
                    "Could not find optimal parameters. Check tickers and time period."
                )
                return

            #if result was found, run pipeline again with it
            optimal_window = int(optimal_params['z_window'])
            optimal_threshold = optimal_params['z_threshold']

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

                #generate detailed report and open in browser
                title = f"Report for pairs: {input_tickers[0]} & {input_tickers[1]}"
                create_detailed_report(equity_curve, title)
                webbrowser.open('file://' + os.path.realpath('report.html'))
        
        except (DataFetchError, CointegrationError) as e:
            messagebox.showerror("Optimisation failed", str(e))
        except Exception as e:
            messagebox.showerror("An unexpected error occurred", str(e))
        finally:
            self.control_frame.set_controls_enabled(True)




