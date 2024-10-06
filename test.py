import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Define the portfolio allocation
tickers = {
    "FXAIX": 0.30,  # U.S. Large-Cap Stocks
    "IWM": 0.10,  # U.S. Small-Cap Stocks
    "VO": 0.10,   # U.S. Mid-Cap Stocks
    "VEA": 0.15,  # Developed Market Stocks
    "EEM": 0.05,  # Emerging Markets Stocks
    "GOVT": 0.05, # Bonds
    "VNQ": 0.05,  # Real Estate (REITs)
    "GLD": 0.03   # Commodities (Gold)
}

# Weekly investment amount
weekly_investment = 50

# Calculate the date range: Last week's Wednesday and this week's Wednesday
today = datetime.today()
last_week_wednesday = today - timedelta(days=(today.weekday() - 2 + 7))  # Last Wednesday
this_week_wednesday = today - timedelta(days=(today.weekday() - 2))  # This Wednesday

# Function to calculate the gain or loss for a week's investment
def calculate_weekly_gain(ticker, allocation):
    # Get historical data for last week's Wednesday and this week's Wednesday
    data = yf.download(ticker, 
                   start=last_week_wednesday.strftime('%Y-%m-%d'), 
                   end=this_week_wednesday.strftime('%Y-%m-%d'), 
                   progress=False)
    
    if data.empty:
        return 0, 0, 0  # No data, return 0
    
    # Get last week's Wednesday closing price and this week's Wednesday closing price
    last_week_price = data['Close'][0]  # Last week's Wednesday closing price
    this_week_price = data['Close'][-1]  # This week's Wednesday closing price
    
    # Calculate the invested amount for this asset
    invested_amount = weekly_investment * allocation
    
    # Calculate the gain/loss for this week's investment
    gain_or_loss = invested_amount * (this_week_price - last_week_price) / last_week_price
    
    return invested_amount, gain_or_loss, gain_or_loss / invested_amount * 100

# Track total gain and total invested
total_invested = 0
total_gain = 0

# Loop through each ticker in the portfolio and calculate the weekly gains
for ticker, allocation in tickers.items():
    invested, gain, percentage_gain = calculate_weekly_gain(ticker, allocation)
    total_invested += invested
    total_gain += gain
    print(f"{ticker} - Invested: ${invested:.2f}, Gain/Loss: ${gain:.2f}, Percentage Gain/Loss: {percentage_gain:.2f}%")

# Print overall results
print(f"\nTotal Invested Last Week: ${total_invested:.2f}")
print(f"Total Gain/Loss This Week: ${total_gain:.2f}")
print(f"Overall Percentage Gain/Loss: {(total_gain / total_invested * 100):.2f}%")
