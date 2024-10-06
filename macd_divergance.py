import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Function to calculate MACD and Signal Line
def calculate_macd(data, slow=26, fast=12, signal=9):
    data['EMA_Fast'] = data['Adj Close'].ewm(span=fast, min_periods=fast).mean()
    data['EMA_Slow'] = data['Adj Close'].ewm(span=slow, min_periods=slow).mean()
    data['MACD'] = data['EMA_Fast'] - data['EMA_Slow']
    data['Signal_Line'] = data['MACD'].ewm(span=signal, min_periods=signal).mean()
    data['MACD_Histogram'] = data['MACD'] - data['Signal_Line']
    return data

# Function to identify divergences
def find_divergences(data):
    divergences = pd.DataFrame(index=data.index)
    for i in range(1, len(data)):
        # Price increasing, MACD decreasing (Bearish Divergence)
        if (data['Adj Close'].iloc[i] > data['Adj Close'].iloc[i-1]) and (data['MACD'].iloc[i] < data['MACD'].iloc[i-1]):
            divergences.loc[data.index[i], 'Divergence'] = 'Bearish'
        # Price decreasing, MACD increasing (Bullish Divergence)
        elif (data['Adj Close'].iloc[i] < data['Adj Close'].iloc[i-1]) and (data['MACD'].iloc[i] > data['MACD'].iloc[i-1]):
            divergences.loc[data.index[i], 'Divergence'] = 'Bullish'
    return divergences

# Download historical data for the last 3 months
ticker = 'AAPL'
end_date = datetime.today()
start_date = end_date - timedelta(days=90)  # Last 3 months
data = yf.download(ticker, start=start_date, end=end_date)
data = calculate_macd(data)

# Find divergences
divergences = find_divergences(data)

# Plot the results
plt.figure(figsize=(14, 8))

# Plot stock price
plt.subplot(2, 1, 1)
plt.plot(data['Adj Close'], label='Price', color='blue')
plt.scatter(divergences[divergences['Divergence'] == 'Bullish'].index, data['Adj Close'][divergences['Divergence'] == 'Bullish'], color='green', label='Bullish Divergence', marker='^', alpha=1)
plt.scatter(divergences[divergences['Divergence'] == 'Bearish'].index, data['Adj Close'][divergences['Divergence'] == 'Bearish'], color='red', label='Bearish Divergence', marker='v', alpha=1)
plt.title(f'{ticker} Price with MACD Divergences (Last 3 months)')
plt.legend()

# Plot MACD and Signal line
plt.subplot(2, 1, 2)
plt.plot(data['MACD'], label='MACD', color='blue')
plt.plot(data['Signal_Line'], label='Signal Line', color='red')
plt.fill_between(data.index, data['MACD_Histogram'], color='gray', alpha=0.5)
plt.title('MACD and Signal Line')
plt.legend()

plt.tight_layout()
plt.show()
