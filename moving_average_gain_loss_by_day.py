import pandas as pd
import plotly.graph_objects as go

def calculate_daily_gain_loss_and_moving_average(stock_data, n=7):
    """
    This function calculates the daily gain/loss based on stock closing prices 
    and the 7-day moving average gain/loss for each specific day of the week.
    
    Parameters:
    stock_data (pd.DataFrame): A pandas DataFrame containing stock data with 'Date' and 'Close' columns.
    n (int): The number of occurrences to consider for the moving average (default is 7).
    
    Returns:
    pd.DataFrame: A DataFrame with two new columns: 'Daily Gain/Loss' and '7-Day Moving Average Gain/Loss'.
    """
    # Ensure 'Date' column is in datetime format and handle potential timezone issues
    stock_data['Date'] = pd.to_datetime(stock_data['Date'], errors='coerce', utc=True)

    # Check for any parsing errors (NaT values)
    if stock_data['Date'].isnull().any():
        raise ValueError("Some date values could not be converted to datetime format. Please check your 'Date' column.")

    # Remove timezone information by converting to naive datetime in the system's local time
    stock_data['Date'] = stock_data['Date'].dt.tz_convert(None)

    # Filter data from 2024 to today
    start_date = pd.Timestamp("2024-01-01")
    end_date = pd.Timestamp("2024-10-08")
    stock_data = stock_data[(stock_data['Date'] >= start_date) & (stock_data['Date'] <= end_date)]

    # Sort data by date to ensure sequential calculations
    stock_data = stock_data.sort_values('Date')

    # Calculate the daily percentage gain/loss
    stock_data['Daily Gain/Loss'] = stock_data['Close'].pct_change() * 100

    # Add a 'Day of Week' column
    stock_data['Day of Week'] = stock_data['Date'].dt.day_name()

    # Create an empty column for the 7-day moving average gain/loss
    stock_data['7-Day Moving Average Gain/Loss'] = None

    # Calculate the 7-day moving average for each specific day of the week
    for day in stock_data['Day of Week'].unique():
        # Filter data for the specific day of the week
        day_data = stock_data[stock_data['Day of Week'] == day]
        
        # Calculate the moving average for the specific day of the week
        stock_data.loc[day_data.index, '7-Day Moving Average Gain/Loss'] = day_data['Daily Gain/Loss'].rolling(window=n).mean()

    return stock_data

def calculate_price_with_gain_loss(stock_data):
    """
    This function calculates the cumulative price impact based on the daily gain/loss 
    and the 7-day moving average gain/loss and reflects them on the closing price.
    
    Parameters:
    stock_data (pd.DataFrame): A DataFrame containing stock data with 'Date', 'Close', 'Daily Gain/Loss', and '7-Day Moving Average Gain/Loss'.
    
    Returns:
    pd.DataFrame: The updated DataFrame with two new columns: 'Price with Daily Gain/Loss' and 'Price with 7-Day Moving Average Gain/Loss'.
    """
    # Calculate cumulative price effect for daily gain/loss
    stock_data['Price with Daily Gain/Loss'] = stock_data['Close'] * (1 + stock_data['Daily Gain/Loss'] / 100).cumprod()

    # Calculate cumulative price effect for 7-day moving average gain/loss
    stock_data['Price with 7-Day Moving Avg Gain/Loss'] = stock_data['Close'] * (1 + stock_data['7-Day Moving Average Gain/Loss'] / 100).cumprod()

    return stock_data

def plot_stock_data_with_metrics(stock_data):
    """
    Plot the stock data including Volume, Close Price, and the reflected Price with Gain/Loss on the primary y-axis,
    interactively using plotly.
    
    Parameters:
    stock_data (pd.DataFrame): A DataFrame containing 'Date', 'Volume', 'Close', 'Price with Daily Gain/Loss', and 'Price with 7-Day Moving Average Gain/Loss'.
    """
    # Create a figure
    fig = go.Figure()

    # Add Volume as a bar chart (secondary y-axis)
    fig.add_trace(go.Bar(x=stock_data['Date'], y=stock_data['Volume'], name='Volume', marker_color='gray', opacity=0.6, yaxis='y2'))

    # Add Close Price as a line chart (primary y-axis)
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Close'], mode='lines', name='Close Price', line=dict(color='blue')))

    # Add Price with Daily Gain/Loss as a line chart (primary y-axis)
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Price with Daily Gain/Loss'], mode='lines', name='Price with Daily Gain/Loss', line=dict(color='green', dash='solid')))

    # Add Price with 7-Day Moving Average Gain/Loss as a line chart (primary y-axis)
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Price with 7-Day Moving Avg Gain/Loss'], mode='lines', name='Price with 7-Day Moving Avg Gain/Loss', line=dict(color='red', dash='dot')))

    # Update layout to include a secondary y-axis for Volume
    fig.update_layout(
        title="Interactive Stock Data: Volume, Close Price, Price with Daily Gain/Loss, 7-Day Moving Avg Gain/Loss",
        xaxis_title="Date",
        yaxis_title="Price",
        yaxis2=dict(title="Volume", overlaying='y', side='right'),  # Secondary y-axis for volume
        legend=dict(x=0, y=1),
        hovermode="x unified"
    )

    # Show the plot
    fig.show()

def main():
    # Load data
    df = pd.read_csv("./data/daily/AAPL_daily.csv")

    # Calculate daily gain/loss and 7-day moving average
    df = calculate_daily_gain_loss_and_moving_average(df, n=7)

    # Calculate price impacts based on gain/loss
    df = calculate_price_with_gain_loss(df)

    # Plot the stock data
    plot_stock_data_with_metrics(df)

    # Print the resulting dataframe (optional)
    print(df)


if __name__ == "__main__":
    main()
