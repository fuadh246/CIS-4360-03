import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from datetime import datetime, timedelta
import numpy as np

# Function to identify the local minima (lows) and maxima (highs)
def identify_trends(data, order=5):
    data['Low_Minima'] = data['Adj Close'][argrelextrema(data['Adj Close'].values, np.less_equal, order=order)[0]]
    data['High_Maxima'] = data['Adj Close'][argrelextrema(data['Adj Close'].values, np.greater_equal, order=order)[0]]
    
    # Identifying the trend points (HH, LH, HL, LL)
    trends = pd.DataFrame(index=data.index)
    trends['Type'] = ''
    
    # Flagging points for HH, LH, HL, LL
    last_low = None
    last_high = None
    
    for i in range(1, len(data)):
        if pd.notnull(data['High_Maxima'].iloc[i]):
            if last_high is not None and data['High_Maxima'].iloc[i] > last_high:
                trends['Type'].iloc[i] = 'HH'  # Higher High
            else:
                trends['Type'].iloc[i] = 'LH'  # Lower High
            last_high = data['High_Maxima'].iloc[i]
        elif pd.notnull(data['Low_Minima'].iloc[i]):
            if last_low is not None and data['Low_Minima'].iloc[i] > last_low:
                trends['Type'].iloc[i] = 'HL'  # Higher Low
            else:
                trends['Type'].iloc[i] = 'LL'  # Lower Low
            last_low = data['Low_Minima'].iloc[i]
    
    return data, trends

ticker = 'AAPL'
end_date = datetime.today()
start_date = end_date - timedelta(days=365)  # Last 3 months
data = yf.download(ticker, start=start_date, end=end_date)

# Identify lower lows, lower highs, higher lows, and higher highs
order = 20  # Adjust this value to better capture highs and lows
data, trends = identify_trends(data, order)

# Plot the results
plt.figure(figsize=(14, 8))

# Plot stock price
plt.plot(data['Adj Close'], label='Price', color='blue')

# Plot the trend points
plt.scatter(data.index, data['Low_Minima'], color='green', label='Lows (LL/HL)', marker='^')
plt.scatter(data.index, data['High_Maxima'], color='red', label='Highs (LH/HH)', marker='v')

# Annotate the points with HH, LH, HL, LL
for i in range(len(trends)):
    if trends['Type'].iloc[i] in ['HH', 'LH', 'HL', 'LL']:
        plt.text(data.index[i], data['Adj Close'].iloc[i], trends['Type'].iloc[i], fontsize=9, color='black')

plt.title(f'{ticker} Price with Higher Highs, Lower Highs, Higher Lows, and Lower Lows')
plt.legend()

plt.tight_layout()
plt.show()
