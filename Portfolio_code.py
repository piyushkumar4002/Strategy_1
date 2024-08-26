import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
import copy
import matplotlib.pyplot as plt

# Function to calculate the Cumulative Annual Growth Rate (CAGR) of a trading strategy
def CAGR(DF):
    df = DF.copy()  # Create a copy of the DataFrame
    df["cum_return"] = (1 + df["mon_ret"]).cumprod()  # Calculate cumulative returns
    n = len(df) / 12  # Number of years
    CAGR = (df["cum_return"].tolist()[-1])**(1/n) - 1  # Calculate CAGR
    return CAGR

# Function to calculate the annualized volatility of a trading strategy
def volatility(DF):
    df = DF.copy()  # Create a copy of the DataFrame
    vol = df["mon_ret"].std() * np.sqrt(12)  # Calculate annualized volatility
    return vol

# Function to calculate the Sharpe ratio of a trading strategy
def sharpe(DF, rf):
    df = DF.copy()  # Create a copy of the DataFrame
    sr = (CAGR(df) - rf) / volatility(df)  # Calculate Sharpe ratio
    return sr

# Function to calculate the maximum drawdown of a trading strategy
def max_dd(DF):
    df = DF.copy()  # Create a copy of the DataFrame
    df["cum_return"] = (1 + df["mon_ret"]).cumprod()  # Calculate cumulative returns
    df["cum_roll_max"] = df["cum_return"].cummax()  # Calculate rolling maximum cumulative returns
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]  # Calculate drawdowns
    df["drawdown_pct"] = df["drawdown"] / df["cum_roll_max"]  # Calculate drawdown percentage
    max_dd = df["drawdown_pct"].max()  # Find the maximum drawdown
    return max_dd

# Download historical data (monthly) for DJI constituent stocks
tickers = ["MMM", "AXP", "T", "BA", "CAT", "CSCO", "KO", "XOM", "GE", "GS", "HD",
           "IBM", "INTC", "JNJ", "JPM", "MCD", "MRK", "MSFT", "NKE", "PFE", "PG", "TRV",
           "UNH", "VZ", "V", "WMT", "DIS"]

ohlc_mon = {}  # Dictionary to store OHLC data for each stock
start = dt.datetime.today() - dt.timedelta(3650)  # Start date 10 years ago
end = dt.datetime.today()  # End date (today)

# Looping over tickers and downloading historical data for each stock
for ticker in tickers:
    ohlc_mon[ticker] = yf.download(ticker, start, end, interval='1mo')
    ohlc_mon[ticker].dropna(inplace=True, how="all")  # Remove rows with all NaN values

tickers = ohlc_mon.keys()  # Redefine tickers variable after removing any tickers with corrupted data

# Calculate monthly return for each stock and consolidate return information in a separate DataFrame
ohlc_dict = copy.deepcopy(ohlc_mon)  # Deep copy of OHLC data
return_df = pd.DataFrame()  # Initialize DataFrame to store monthly returns
for ticker in tickers:
    print("Calculating monthly return for ", ticker)
    ohlc_dict[ticker]["mon_ret"] = ohlc_dict[ticker]["Adj Close"].pct_change()  # Calculate monthly returns
    return_df[ticker] = ohlc_dict[ticker]["mon_ret"]  # Add monthly returns to DataFrame
return_df.dropna(inplace=True)  # Drop rows with NaN values

# Function to calculate portfolio return iteratively
def pflio(DF, m, x):
    """Returns cumulative portfolio return
    DF = DataFrame with monthly return info for all stocks
    m = number of stocks in the portfolio
    x = number of underperforming stocks to be removed from portfolio monthly"""
    df = DF.copy()  # Create a copy of the DataFrame
    portfolio = []  # Initialize portfolio
    monthly_ret = [0]  # Initialize list to store monthly returns
    for i in range(len(df)):
        if len(portfolio) > 0:
            monthly_ret.append(df[portfolio].iloc[i, :].mean())  # Calculate mean return of current portfolio
            bad_stocks = df[portfolio].iloc[i, :].sort_values(ascending=True)[:x].index.values.tolist()  # Identify underperforming stocks
            portfolio = [t for t in portfolio if t not in bad_stocks]  # Remove underperforming stocks from portfolio
        fill = m - len(portfolio)  # Calculate the number of stocks to add
        new_picks = df.iloc[i, :].sort_values(ascending=False)[:fill].index.values.tolist()  # Pick new top-performing stocks
        portfolio = portfolio + new_picks  # Update portfolio
        print(portfolio)
    monthly_ret_df = pd.DataFrame(np.array(monthly_ret), columns=["mon_ret"])  # Create DataFrame of monthly returns
    return monthly_ret_df

# Calculating overall strategy's Key Performance Indicators (KPIs)
strategy_returns = pflio(return_df, 6, 3)  # Calculate portfolio returns
print("CAGR:", CAGR(strategy_returns))  # Calculate and print CAGR
print("Sharpe Ratio:", sharpe(strategy_returns, 0.025))  # Calculate and print Sharpe Ratio
print("Max Drawdown:", max_dd(strategy_returns))  # Calculate and print Max Drawdown

# Calculating KPIs for Index buy and hold strategy over the same period
DJI = yf.download("^DJI", dt.date.today() - dt.timedelta(3650), dt.date.today(), interval='1mo')  # Download DJI data
DJI["mon_ret"] = DJI["Adj Close"].pct_change().fillna(0)  # Calculate monthly returns for DJI
print("CAGR (DJI):", CAGR(DJI))  # Calculate and print CAGR for DJI
print("Sharpe Ratio (DJI):", sharpe(DJI, 0.025))  # Calculate and print Sharpe Ratio for DJI
print("Max Drawdown (DJI):", max_dd(DJI))  # Calculate and print Max Drawdown for DJI

# Visualization
fig, ax = plt.subplots()
plt.plot((1 + strategy_returns).cumprod())  # Plot cumulative returns of the strategy
plt.plot((1 + DJI["mon_ret"].reset_index(drop=True)).cumprod())  # Plot cumulative returns of DJI
plt.title("Index Return vs Strategy Return")  # Add title to the plot
plt.ylabel("Cumulative Return")  # Add y-axis label
plt.xlabel("Months")  # Add x-axis label
ax.legend(["Strategy Return", "Index Return"])  # Add legend
plt.show()  # Display the plot
