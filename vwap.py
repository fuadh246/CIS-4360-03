import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Fetch Apple stock data from Yahoo Finance
ticker = 'AAPL'
start_date = '2024-01-01'
end_date = pd.Timestamp.today().strftime('%Y-%m-%d')

data = yf.download(ticker, start=start_date, end=end_date)

# Calculate VWAP (Volume Weighted Average Price)
def calculate_vwap(df):
    df['VWAP'] = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()
    return df

# Apply VWAP calculation to the data
data = calculate_vwap(data)

# Initialize portfolio parameters
initial_balance = 100
cash = initial_balance
shares = 0

# Create a column to store portfolio value at each time step
data['Portfolio Value'] = 0

# Backtest VWAP Strategy
for i in range(1, len(data)):
    current_price = data['Close'].iloc[i]
    vwap = data['VWAP'].iloc[i]
    
    # If the current price is below VWAP, buy
    if current_price < vwap and cash > 0:
        # Buy as many shares as possible with the current cash
        shares_bought = cash // current_price
        shares += shares_bought
        cash -= shares_bought * current_price
    
    # If the current price is above VWAP, sell all shares
    elif current_price > vwap and shares > 0:
        # Sell all shares
        cash += shares * current_price
        shares = 0
    
    # Calculate the portfolio value (cash + value of shares)
    data['Portfolio Value'].iloc[i] = cash + shares * current_price

# Plot the stock price and portfolio value over time
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Close'], label='AAPL Price', color='blue')
plt.plot(data.index, data['VWAP'], label='VWAP', color='orange', linestyle='--')
plt.plot(data.index, data['Portfolio Value'], label='Portfolio Value', color='green')
plt.title('AAPL VWAP Strategy Backtest')
plt.xlabel('Date')
plt.ylabel('Price / Portfolio Value')
plt.legend()
plt.show()

# Display final portfolio value and cash
final_portfolio_value = cash + shares * data['Close'].iloc[-1]
print(f"Final Portfolio Value: ${final_portfolio_value:.2f}")
print(f"Cash Remaining: ${cash:.2f}")
print(f"Shares Held: {shares}")
