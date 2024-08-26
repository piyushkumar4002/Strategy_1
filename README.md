# Trading Strategy Backtest

This repository contains a Python script that backtests a simple trading strategy using historical stock data. The strategy dynamically selects a portfolio of top-performing stocks and evaluates its performance against the Dow Jones Industrial Average (DJI) index.

## Strategy Overview

The strategy involves:
1. **Monthly Selection**: Selecting a portfolio of `m` top-performing stocks from a given list of DJI constituents.
2. **Dynamic Rebalancing**: Each month, the `x` worst-performing stocks are removed from the portfolio and replaced with new top-performing stocks.
3. **Performance Evaluation**: The script calculates the portfolio's cumulative returns, and key performance indicators (KPIs) like CAGR, Sharpe Ratio, and Maximum Drawdown.

## Files

- **`backtest.py`**: The main script that performs the backtest and calculates the strategy's performance metrics.

## Requirements

- Python 3.x
- `numpy`
- `pandas`
- `yfinance`
- `matplotlib`
- `datetime`

Install the required packages using:

```
pip install numpy pandas yfinance matplotlib
```
#Usage

Download Historical Data: The script downloads historical monthly data for DJI constituent stocks using the yfinance API.

Calculate Monthly Returns: The monthly returns for each stock are calculated and consolidated into a DataFrame.

Run the Backtest: The strategy is backtested by iteratively selecting and rebalancing the portfolio based on historical performance.

Compare with Index: The strategy's performance is compared with a buy-and-hold strategy on the DJI index.

Visualize Results: The script visualizes the cumulative returns of the strategy vs. the DJI index.

Functions
CAGR(DF): Calculates the Cumulative Annual Growth Rate (CAGR) of a trading strategy.
volatility(DF): Calculates the annualized volatility of a trading strategy.
sharpe(DF, rf): Calculates the Sharpe Ratio of a trading strategy (adjusted for risk-free rate rf).
max_dd(DF): Calculates the maximum drawdown of a trading strategy.
pflio(DF, m, x): Calculates the cumulative portfolio return with m stocks and x monthly removals of underperforming stocks.
Example Output
The script outputs the following performance metrics:

CAGR: The annual growth rate of the strategy.
Sharpe Ratio: The risk-adjusted return of the strategy.
Maximum Drawdown: The maximum observed loss from a peak to a trough.
A comparison plot of cumulative returns between the strategy and the DJI index is also generated.

How to Run
Execute the script by running:

bash
Copy code
python backtest.py
The script will print the performance metrics and display a plot comparing the strategy's return with the DJI index return.

License
This project is open-source and available under the MIT License.
