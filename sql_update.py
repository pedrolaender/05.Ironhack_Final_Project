# Import libraries
import pandas as pd
import numpy as np
import os
import yfinance as yf
import datetime
import sqlalchemy as db
from dotenv import load_dotenv
from datetime import timedelta



def create_engine():
    """Create engine to connect to MySQL server

    Returns: 
        engine (sqlalchemy.engine): engine that connects to the stocks_project dataset on MySQL Server 
    """
    
    # Import sql_password
    load_dotenv(r'C:\Users\Pedro\OneDrive\Desktop\Ironhack\04. GitHub\05.Ironhack_Final_Project/password.env')
    sql_password = os.getenv('sql_password')
    
    # Set SQL configurations
    user = "root"
    password = sql_password
    url_banco = "localhost"
    nome_db = "stocks_project"
    conn_str = f"mysql+pymysql://{user}:{password}@{url_banco}/{nome_db}"  

    # Create engine object
    engine = db.create_engine(conn_str)
    
    return engine


def add_days_to_date(date, days):
    """Add days to a date and return the date.
    
    Args: 
        date (string): Date string in YYYY-MM-DD format. 
        days (int): Number of days to add to date
    
    Returns: 
        date (date): Date in YYYY-MM-DD with X days added. 
    """
    
    added_date = pd.to_datetime(date) + timedelta(days=days)
    added_date = added_date.strftime("%Y-%m-%d")

    return added_date


def get_start_date(engine):
    """Get the start date to be used in 'create_update_dataframe' function

    Args: 
        engine (sqlalchemy.engine): engine that connects to the stocks_project dataset on MySQL Server 
    
    Returns: 
        start (str): date to be used in 'create_update_dataframe' function
    """

    last_update = pd.read_sql(sql = "SELECT MAX(Date) FROM date_test_01", con=engine)
    start = last_update.iloc[0,0]
    start= add_days_to_date(start, 1)

    return start

def get_end_date():
    """Get yesterdays's date to be used as end date in 'create_update_dataframe' function 

    Returns: 
        yesterday (str): Date string in YYYY-MM-DD format - Today
    """
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days = 1)
    yesterday = yesterday.strftime("%Y-%m-%d")

    return yesterday


def get_ticker_list(engine):
    """Get the ticker list to be used in 'create_update_dataframe' function

    Args: 
        engine (sqlalchemy.engine): engine that connects to the stocks_project dataset on MySQL Server 
    
    Returns: 
        ticker_list (iterable): iterable containing yfinance code for the companies and indexes
    """

    ticker_list = pd.read_sql(sql='SELECT cod_yfinance FROM companies', con=engine)['cod_yfinance']

    return ticker_list


def create_update_dataframe(start, end, ticker_list):
    """Create a DataFrame with last days historical data.
    
    Args: 
        start (string): Date string in YYYY-MM-DD format - One day after the last update 
        end (string): Date string in YYYY-MM-DD format - Today
        ticker_list (iterable): iterable containing yfinance code for the companies and indexes
    
    Returns: 
        df (dataframe): DataFrame with last days historical data. 
    """
    
    df = pd.DataFrame()

    for ticker in ticker_list:
        aux_df = pd.DataFrame()
        aux_df = yf.Ticker(ticker).history(start=start, end=end)
        aux_df['cod_yfinance'] = ticker

        df = pd.concat([df, aux_df], axis=0)

    return df


def format_update_dataframe(dataframe):
    """Transform index to da columns with dates and round Open, High, Low, Close and Dividends columns to 3 decimal places
    
    Args: 
        dataframe (DataFrame): DataFrame containing last days historical data. 
    
    Returns: 
        df (DataFrame): Formated Dataframe. 
    """

    dataframe.reset_index(inplace=True)
    
    # Transform date to datetime
    dataframe['Date'] = pd.to_datetime(dataframe['Date'], utc=True) 

    # Transform datetime to YYYY-MM-DD
    dataframe['Date'] = dataframe['Date'].dt.date

    # Round Columns
    dataframe['Open'] = dataframe['Open'].round(3)
    dataframe['High'] = dataframe['High'].round(3)
    dataframe['Low'] = dataframe['Low'].round(3)
    dataframe['Close'] = dataframe['Close'].round(3)
    dataframe['Dividends'] = dataframe['Dividends'].round(3)

    return dataframe


def append_update_dataframe(dataframe):
    """Append update DataFrame to SQL dataset

    Args: 
        dataframe (DataFrame): DataFrame, already formated, containing last days historical data. 
    
    Returns**: 
        Append update DataFrame to SQL dataset 
    """

    dataframe.to_sql(name='date_test_02', con=engine, if_exists='append', index=False)


engine = create_engine()
start = get_start_date(engine)
end = get_end_date()
ticker_list = get_ticker_list(engine)
df = create_update_dataframe('2023-01-08', end, ['ABMD', 'SULA11.SA', 'BRML3.SA', 'DMMO3.SA', '^GSPC'])
df = format_update_dataframe(df)
append_update_dataframe(df)

print('done')