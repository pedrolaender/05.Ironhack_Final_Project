# Import libraries
import pandas as pd
import numpy as np
import os
import yfinance as yf
import datetime
import sqlalchemy as db
from dotenv import load_dotenv
from datetime import timedelta

import logging

# Logging path
logging_path = r'C:\Users\Pedro\OneDrive\Desktop\Ironhack\05. Dados\stock_project_datasets\Logging/'

today = datetime.datetime.today()
today = today.strftime("%Y-%m-%d")

logging.basicConfig(level=logging.INFO,
                    filename=f'{logging_path}{today}.log',
                    format='%(asctime)s.%(msecs)03d %(levelname)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('Logging')



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
    logger.info('Connection to SQL: Successful')

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


def get_start_date(engine, table):
    """Get the start date to be used in 'create_update_dataframe' function

    Args: 
        engine (sqlalchemy.engine): engine that connects to the stocks_project dataset on MySQL Server 
    
    Returns: 
        start (str): date to be used in 'create_update_dataframe' function
    """

    last_update = pd.read_sql(sql = f"SELECT MAX(Date) FROM {table}", con=engine)
    start = last_update.iloc[0,0]
    start= add_days_to_date(start, 1)

    logger.info(f'Get start date: Successful - Start date: {start}')

    return start


def get_end_date():
    """Get yesterdays's date to be used as end date in 'create_update_dataframe' function 

    Returns: 
        yesterday (str): Date string in YYYY-MM-DD format - Today
    """
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days = 1)
    yesterday = yesterday.strftime("%Y-%m-%d")

    logger.info(f'Get end date: Successful - End date: {yesterday}')

    return yesterday


def get_ticker_list(engine):
    """Get the ticker list to be used in 'create_update_dataframe' function

    Args: 
        engine (sqlalchemy.engine): engine that connects to the stocks_project dataset on MySQL Server 
    
    Returns: 
        ticker_list (iterable): iterable containing yfinance code for the companies and indexes
    """

    ticker_list = pd.read_sql(sql='SELECT cod_yfinance FROM companies', con=engine)['cod_yfinance']

    if ticker_list.shape[0] == 735:
        logger.info(f'Get ticker list: Successful - Number of tickers: {ticker_list.shape[0]}')
    
    else:
        logger.warning(f'Get ticker list: ERROR - Number of tickers expected: 735 -- Number of ticker found: {ticker_list.shape[0]}')

    return ticker_list


def create_update_dataframe(start, end, ticker_list):
    """Create a DataFrame with last days historical data.
        Logging tracks how many entries each ticker got and save on a new .txt for each day the code runs
    
    Args: 
        start (string): Date string in YYYY-MM-DD format - One day after the last update 
        end (string): Date string in YYYY-MM-DD format - Today
        ticker_list (iterable): iterable containing yfinance code for the companies and indexes
    
    Returns: 
        df (dataframe): DataFrame with last days historical data. 
    """
    
    #Track number of entries for each ticker
    entries_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, '7+':0 } 
    ticker_dict = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], '7+':[]}

    #ticker_list = ticker_list.sort_values()

    df = pd.DataFrame()

    for ticker in ticker_list:
        aux_df = pd.DataFrame()
        aux_df = yf.Ticker(ticker).history(start=start, end=end)

        if aux_df.empty:
            logging.warning(f'{ticker}: No data found for this range')
            entries_dict[0] += 1
            ticker_dict[0].append(ticker)

        else:
            if aux_df.shape[0] == 1:
                entries_dict[1] += 1
                ticker_dict[1].append(ticker)

            elif aux_df.shape[0] == 2:
                entries_dict[2] += 1
                ticker_dict[2].append(ticker)

            elif aux_df.shape[0] == 3:
                entries_dict[3] += 1
                ticker_dict[3].append(ticker)

            elif aux_df.shape[0] == 4:
                entries_dict[4] += 1
                ticker_dict[4].append(ticker)

            elif aux_df.shape[0] == 5:
                entries_dict[5] += 1
                ticker_dict[5].append(ticker)

            elif aux_df.shape[0] == 6:
                entries_dict[6] += 1
                ticker_dict[6].append(ticker)

            elif aux_df.shape[0] == 7:
                entries_dict[7] += 1
                ticker_dict[7].append(ticker)

            else:
                entries_dict['7+'] += 1
                ticker_dict['7+'].append(ticker)

            aux_df['cod_yfinance'] = ticker

        df = pd.concat([df, aux_df], axis=0)

    for key, value in entries_dict.items():
        if value == 0:
            logger.info(f'No tickers with {key} entries')
        else: 
            logger.info(f'Number of tickers with {key} entries: {value}')
            logger.info(f'Tickers: {ticker_dict[key]}')

    logger.info(f'Create update DataFrame: Successful - Rows in DF: {df.shape[0]}')
    
    return df


def format_update_dataframe(dataframe):
    """Transform index to da columns with dates and round Open, High, Low, Close and Dividends columns to 3 decimal places
    
    Args: 
        dataframe (DataFrame): DataFrame containing last days historical data. 
    
    Returns: 
        df (DataFrame): Formated Dataframe. 
    """
    
    # Transform the Index into Date Column
    dataframe.reset_index(inplace= True)

    # Transform 'Date' to datetime
    dataframe['Date'] = dataframe['Date'].astype(str)
    dataframe['Date'] = dataframe['Date'].str.extract(r'([0-9]{4}-[0-9]{2}-[0-9]{2})')
    dataframe['Date'] = pd.to_datetime(dataframe['Date'], format='%Y-%m-%d')

    dataframe = dataframe.loc[:,['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits', 'cod_yfinance']]

    # Transform datetime to YYYY-MM-DD
    #dataframe['Date'] = dataframe['Date'].dt.date

    # Round Columns
    dataframe['Open'] = dataframe['Open'].round(3)
    dataframe['High'] = dataframe['High'].round(3)
    dataframe['Low'] = dataframe['Low'].round(3)
    dataframe['Close'] = dataframe['Close'].round(3)
    dataframe['Dividends'] = dataframe['Dividends'].round(3)

    logger.info('Format update DataFrame - Successful')
    
    return dataframe


def append_update_dataframe(dataframe, table):
    """Append update DataFrame to SQL dataset
    Verify if SQL got all the rows in the DF

    Args: 
        dataframe (DataFrame): DataFrame, already formated, containing last days historical data. 
    """

    rows_df = dataframe.shape[0]
    rows_SQL = dataframe.to_sql(name=table, con=engine, if_exists='append', index=False)
    
    if rows_df == rows_SQL:
        logger.info(f'SQL update successfull. All {rows_df} rows where appended to "{table}" database')

    else:
        logger.warning(f'ERROR in SQL update. Only {rows_SQL} out of {rows_df} where appended to "{table}" database')


# Define wich database will get the new data
table = 'historical_data'

engine = create_engine()
start = get_start_date(engine, table)
end = get_end_date()
ticker_list = get_ticker_list(engine)
df = create_update_dataframe(start, end, ticker_list)
df = format_update_dataframe(df, table)
append_update_dataframe(df)

logger.info('Done')