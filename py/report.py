import pandas, numpy
import matplotlib.pyplot as plt

#Performance analysis reporting

#Takes backtested trades and plots report
def create_report(equity_curve: pandas.Series):
    #calculate KPMs

    #total return:
    starting_cap = equity_curve.iloc[0]
    final_equity = equity_curve.iloc[-1]
    total_return_pct = (final_equity / (starting_cap - 1)) * 100

    #sharpe ratio:
    #create new series of daily returns
    daily_returns = equity_curve.pct_change()
    average_daily_returns = daily_returns.mean()
    std_daily_returns = daily_returns.std()

    #convert daily to annual (252 trading days)
    sharpe_ratio = (average_daily_returns / std_daily_returns) * numpy.sqrt(252)

    #Maximum drawdown:
    #find highest mark
    high_mark = equity_curve.cummax()

    #find daily drawdown
    daily_drawdown = (equity_curve - high_mark) / high_mark

    #find worst day
    maximum_drawdown = daily_drawdown.min()


    #create visualisations
    #plot equity curve
    fig, ax = plt.subplots()
    ax.plot(equity_curve)
    ax.set_title("Equity Curve")
    ax.set_xlabel("Date")
    ax.set_ylabel("Portfolio Value")
    ax.grid(True)
    
    #display KPMS by formatting into str
    report_str = (
        f"Total Return: {total_return_pct:.2f}% | "
        f"Sharpe Ratio: {sharpe_ratio:.2f} | "
        f"Max Drawdown: {maximum_drawdown:.2f}%"
    )

    ax.set_title(f"Performance:\n{report_str}")

    #show the plot
    plt.show()
    


