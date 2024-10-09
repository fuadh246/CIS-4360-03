'''
@project       : Temple University CIS 4360 Computational Methods in Finance
@Instructor    : Dr. Alex Pang

@Student Name  : Fuad Hassan

@Date          : 10/06/2024

Download daily stock price from Yahoo

'''

import os
import pandas as pd
import numpy as np
import sqlite3
import warnings
warnings.filterwarnings('ignore')

import yfinance as yf

import option

# https://www.geeksforgeeks.org/python-stock-data-visualisation/

def get_daily_from_yahoo(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date)
    if df.empty:
        print(f"No data found for {ticker} between {start_date} and {end_date}")
        return None
    # Add an extra column for the ticker
    df['Ticker'] = ticker
    return(df)

def download_data_to_csv(opt, list_of_tickers):
    #
    ''' 
    iterate through the list of tickers, call the get_daily_from_yahoo between two dates
    specified from the option, save the dataframe to a csv file <ticker>_daily.csv in the output_dir
    remember to add a extra column with the ticker
    '''
    # Iterate through the list of tickers
    if not os.path.exists(opt.output_dir):
        os.makedirs(opt.output_dir)
        print(f"Created directory: {opt.output_dir}")

    # Iterate through the list of tickers
    for ticker in list_of_tickers:
        # Call get_daily_from_yahoo for each ticker
        df = get_daily_from_yahoo(ticker, opt.start_date, opt.end_date)
        if df is not None:
            # Save the DataFrame to a CSV file in the output_dir
            output_file = os.path.join(opt.output_dir, f"{ticker}_daily.csv")
            print(f"Saving {ticker} data to {output_file}")
            df.to_csv(output_file, index=True)  # Write to CSV
            print(f"Saved {ticker} data to {output_file}")

def csv_to_table(csv_file_name, fields_map, db_connection, db_table):
    # insert data from a csv file to a table
    df = pd.read_csv(csv_file_name)
    if df.shape[0] <= 0:
        return
    
    # change the column header to match how they are spelled in the database
    df.columns = [fields_map.get(x, x) for x in df.columns]
    print(df.columns)

    # move ticker columns
    # new_df = df[['Ticker']]
    # for c in df.columns[:-1]:
    #     new_df[c] = df[c]

    ticker = os.path.basename(csv_file_name).replace('.csv','').replace("_daily", "")
    print(ticker)
    cursor = db_connection.cursor()

    '''
    Delete from the table any old data for the ticker
    hint: sql = f"delete from {db_table} .... ", then call execute
    turn the dataframe into tuples
    
    insert data by using a insert ... values statement under executemany method
    hint: sql = f"insert into {db_table} (Ticker, AsOfDate, ...)  VALUES (?, ?, ...) "
    print(sql)

    remember to close the db connection
    
    '''
    sql_delete = f"DELETE FROM {db_table} WHERE Ticker = ?"
    # cursor.execute(sql_delete, (ticker,))
    cursor.execute(sql_delete, (df['Ticker'][0],))
    
    # Insert new data
    sql_insert = f"""INSERT INTO {db_table} 
                    (Ticker, AsOfDate, Open, High, Low, Close, Volume, Dividend, StockSplits) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    data_tuples = [tuple(x) for x in df[['Ticker', 'AsOfDate', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividend', 'StockSplits']].values]
    
    cursor.executemany(sql_insert, data_tuples)
    db_connection.commit()
    print(f"Inserted data for {ticker} into {db_table}")

def save_daily_data_to_sqlite(opt, daily_file_dir, list_of_tickers):
    # read all daily.csv files from a dir and load them into sqlite table
    db_file = os.path.join(opt.sqlite_db)
    db_conn = sqlite3.connect(db_file)
    db_table = 'EquityDailyPrice'

    # define a fields_map dictionary to map the column name of the csv file to what is expected in the database table

    fields_map = {
        'Date': 'AsOfDate',
        'Open': 'Open',
        'High': 'High',
        'Low': 'Low',
        'Close': 'Close',
        'Volume': 'Volume',
        'Dividends': 'Dividend',
        'Stock Splits': 'StockSplits'
    }
    
    for ticker in list_of_tickers:
        file_name = os.path.join(daily_file_dir, f"{ticker}_daily.csv")
        print(file_name)
    # Check if the file exists
        if os.path.isfile(file_name):
            csv_to_table(file_name, fields_map, db_conn, db_table)
        else:
            print(f"File not found: {file_name}")

    
def _test():
    ticker = 'MSFT'
    start_date = '2020-01-01'
    end_date = '2024-09-01'

    print (f"Testing getting data for {ticker}:")
    df = get_daily_from_yahoo(ticker, start_date, end_date)
    print(df)

    
def run():
    #
    parser = option.get_default_parser()
    parser.add_argument('--data_dir', dest = 'data_dir', default='./data', help='data dir')    
    
    args = parser.parse_args()
    opt = option.Option(args = args)

    opt.output_dir = os.path.join(opt.data_dir, "daily")
    opt.sqlite_db = os.path.join(opt.data_dir, "sqlite/Equity.db")

    if opt.tickers is not None:
        list_of_tickers = opt.tickers.split(',')
    else:
        fname = os.path.join(opt.data_dir, "S&P500.csv")
        df = pd.read_csv(fname)
        list_of_tickers = list(df['Symbol'])
        print(f"Read tickers from {fname}")
        

    # print(list_of_tickers)
    # print(opt.start_date, opt.end_date)

    # download all daily price data into a output dir
    # toggle between 1 and 0 to run or skip the block of code below in testing phrase
    if 1:
        print(f"Download data to {opt.data_dir} directory")
        download_data_to_csv(opt, list_of_tickers)

    # read the csv file back and save the data into sqlite database
    if 1:
        save_daily_data_to_sqlite(opt, opt.output_dir, list_of_tickers)
    
if __name__ == "__main__":
    _test()
    run()
