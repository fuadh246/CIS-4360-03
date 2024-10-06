import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# Fetch historical stock data for Apple (AAPL)
stock_data = yf.download('AAPL', start='2023-01-01', end='2023-12-31')

# Calculate daily returns
stock_data['Daily Return'] = stock_data['Adj Close'].pct_change()

# Drop missing values for returns
returns = stock_data['Daily Return'].dropna()

# Calculate daily variance and standard deviation
stock_data['Daily Variance'] = (stock_data['Daily Return'] - returns.mean())**2
stock_data['Daily Standard Deviation'] = np.sqrt(stock_data['Daily Variance'])

# Calculate overall variance and standard deviation
overall_variance = np.var(returns, ddof=1)  # ddof=1 for sample variance
overall_std_dev = np.std(returns, ddof=1)   # ddof=1 for sample standard deviation

# Print overall variance and standard deviation
print("Overall Variance of Apple stock returns:", overall_variance)
print("Overall Standard Deviation of Apple stock returns:", overall_std_dev)

# Print first 5 rows of daily returns, variance, and standard deviation for inspection
print(stock_data[['Daily Return', 'Daily Variance', 'Daily Standard Deviation']].dropna().head())

# Plot Adjusted Close Prices, Daily Return, Daily Variance, and Daily Standard Deviation
plt.figure(figsize=(14, 12))

# Plot Adjusted Close Prices
plt.subplot(4, 1, 1)
plt.plot(stock_data['Adj Close'], color='blue', label='Adjusted Close Price')
plt.title('Apple (AAPL) Stock Price (Adjusted Close)')
plt.ylabel('Price (USD)')
plt.legend(loc='upper left')

# Plot Daily Returns
plt.subplot(4, 1, 2)
plt.plot(stock_data['Daily Return'], color='orange', label='Daily Returns')
plt.title('Apple (AAPL) Daily Returns')
plt.ylabel('Daily Return (%)')
plt.legend(loc='upper left')

# Plot Daily Variance
plt.subplot(4, 1, 3)
plt.plot(stock_data['Daily Variance'], color='green', label='Daily Variance')
plt.title('Apple (AAPL) Daily Variance')
plt.ylabel('Variance')
plt.legend(loc='upper left')

# Plot Daily Standard Deviation
plt.subplot(4, 1, 4)
plt.plot(stock_data['Daily Standard Deviation'], color='red', label='Daily Standard Deviation')
plt.title('Apple (AAPL) Daily Standard Deviation')
plt.ylabel('Standard Deviation')
plt.legend(loc='upper left')

# Display the plot
plt.tight_layout()
plt.show()
