import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    # Calculate short-term (12-period) and long-term (26-period) exponential moving averages (EMA)
    data['EMA_12'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data['EMA_26'] = data['Close'].ewm(span=long_window, adjust=False).mean()

    # Calculate MACD line
    data['MACD'] = data['EMA_12'] - data['EMA_26']

    # Calculate Signal line (9-period EMA of MACD line)
    data['Signal_Line'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()

    return data

def generate_signals(data):
    # Create buy and sell signals
    data['Buy_Signal'] = np.where((data['MACD'] > data['Signal_Line']) & (data['MACD'].shift(1) <= data['Signal_Line'].shift(1)), 1, 0)
    data['Sell_Signal'] = np.where((data['MACD'] < data['Signal_Line']) & (data['MACD'].shift(1) >= data['Signal_Line'].shift(1)), -1, 0)

    return data

def macd_strategy(data):
    # Calculate MACD and Signal lines
    data = calculate_macd(data)

    # Generate Buy/Sell signals
    data = generate_signals(data)

    # Return the relevant data with signals
    return data[['Close', 'MACD', 'Signal_Line', 'Buy_Signal', 'Sell_Signal']]

def fetch_stock_data(ticker, period="7d", interval="5m"):
    # Fetch stock data from Yahoo Finance with 5-minute intervals
    stock_data = yf.download(ticker, period=period, interval=interval)
    return stock_data

def simulate_investment(data, initial_investment=10000):
    # Start with an initial investment
    cash = initial_investment
    shares = 0
    for index, row in data.iterrows():
        # Buy condition
        if row['Buy_Signal'] == 1 and cash > 0:
            # Buy as many shares as possible
            shares = cash / row['Close']
            cash = 0
            print(f"Buy at {row['Close']} on {index} - Shares: {shares}")
        
        # Sell condition
        elif row['Sell_Signal'] == -1 and shares > 0:
            # Sell all shares
            cash = shares * row['Close']
            shares = 0
            print(f"Sell at {row['Close']} on {index} - Cash: {cash}")
    
    # Final portfolio value (either cash or value of remaining shares)
    if shares > 0:
        final_value = shares * data['Close'].iloc[-1]
        print(f"End of period - Still holding shares worth: {final_value}")
    else:
        final_value = cash
        print(f"End of period - Total cash: {final_value}")

    profit = final_value - initial_investment
    print(f"\nFinal profit or loss: {profit}")
    return final_value

# Example usage
if __name__ == "__main__":
    # Define the stock ticker and data parameters
    ticker = "AAPL"  # Example: Apple Inc.
    period = "1mo"    # Fetch up to 5 days of 5-minute data
    interval = "5m"  # 5-minute interval data

    # Fetch stock data
    stock_data = fetch_stock_data(ticker, period, interval)

    # Calculate MACD strategy and signals
    signals = macd_strategy(stock_data)

    # Simulate investment using buy/sell signals
    final_value = simulate_investment(signals, initial_investment=10000)

