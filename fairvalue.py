import yfinance as yf
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from datetime import datetime

# Step 1: Fetch historical data for the stock and market index
stock_ticker = 'AAPL'
market_ticker = '^GSPC'  # S&P 500 Index ticker

# Get today's date for the end date
end_date = datetime.today().strftime('%Y-%m-%d')

# Define the start date
start_date = "2020-01-01"

# Download data using yfinance
stock_data = yf.download(stock_ticker, start=start_date, end=end_date)
market_data = yf.download(market_ticker, start=start_date, end=end_date)

# Step 2: Calculate daily returns for both the stock and the market
stock_data['Returns'] = stock_data['Adj Close'].pct_change()
market_data['Market Returns'] = market_data['Adj Close'].pct_change()

# Step 3: Remove missing data
returns = pd.concat([stock_data['Returns'], market_data['Market Returns']], axis=1).dropna()

# Step 4: Calculate covariance and variance
covariance = np.cov(returns['Returns'], returns['Market Returns'])[0][1]
market_variance = np.var(returns['Market Returns'])

# Step 5: Calculate beta
beta = covariance / market_variance

# Display the beta value
print(f"Beta of {stock_ticker} relative to {market_ticker}: {beta:.2f}")
