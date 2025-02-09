import os
import pandas as pd
import requests
from datetime import timedelta

def create_path_write(folder):
    """
    Takes filename from user.
    """
    filename = input("Enter the name of the file to write (without extension): ") + '.xls'
    path = os.path.join(folder, filename)
    return path

def import_transactions(csv_file):
    """
    Reads CSV. Creates DataFrame with useful columns. Converts 'Time' column to datetime objects.
    """
    columns_to_load = ['Time', 'Side', 'Symbol ID', 'ISIN', 'Currency', 'Quantity', 'Commission', 'Commission Currency', 'Traded Volume']

    df = pd.read_csv(csv_file, sep='\t', header=0, encoding='utf-16', usecols=columns_to_load)
    
    df['Time'] = pd.to_datetime(df['Time'])

    return df

def get_nbp_exchange_rate(currency, date):

    """
    Gets the exchange rate from the NBP API website for the previous business day.

    Parameters:

    currency: Three letters currency shortcut
    date: Date in datetime format object.
    
    Returns:

    Rate
    Date of the course

    """
   
    new_date = date - timedelta(days=1)

    has_date = False

    while not has_date:        
        format_date = new_date.strftime('%Y-%m-%d')
        url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency.lower()}/{format_date}/?format=json"
        try:                                   
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            has_date = True                                  
        except:                                
            has_date = False            # back one day before
            print(f"Brak kursu dla {currency.upper()} z dnia {format_date}.\nSzukam w poprzednim dniu")  
            new_date -= timedelta(days=1)

    rate = (data["rates"][0]['mid'])
    rate_date = (data["rates"][0]['effectiveDate'])
    return rate, rate_date

def download_exchange_rate(row):
    """
    Assigns the currency rate and date taken from the NBP
    """

    currency = row['Currency']
    date = row['Time']
    
    if currency == 'PLN':
        rate = 1
        rate_date = date.date()
    else:
        rate, rate_date = get_nbp_exchange_rate(currency, date)
    
    return pd.Series([rate, rate_date])

def write_to_excel(df, folder):
    try:
        df.to_excel(create_path_write(folder), index=False, header=True)
        print(f"Writing successful")
    except Exception as e:
        print(f"Unexpected error: {e}")

def add_exchange_rate(df):
    """
    Adds the NBP exchange rate and the exchange rate date to the DataFrame.

    The function calls `download_exchange_rate` for each row,
    to fill the 'NBP Rate' and 'NBP Date' columns.

    Args:
    df (pd.DataFrame): DataFrame with stock market transaction data.

    Returns:
    pd.DataFrame: Updated DataFrame with added columns.
    """
    df[['NBP Rate', 'NBP Date']] = df.apply(download_exchange_rate, axis=1)
    return df

def calculate_pln_values(df):
    """
    Calculates and adds columns to the DataFrame representing financial values in PLN (Polish Zloty).
    
    The function performs the following operations:
    1. Calculates 'PLN Traded Volume' by multiplying the 'NBP Rate' with 'Traded Volume'.
    2. Calculates 'PLN Commission' based on the 'NBP Rate' and 'Commission', if the 'Currency' matches the 'Commission Currency'.
       Otherwise, it returns 'Currency error'.
    3. Calculates 'PLN Values minus costs' by adjusting the 'PLN Traded Volume' with the 'PLN Commission'.
       The result is different for 'buy' and 'sell' sides: for 'buy', it adds the values, while for 'sell', it subtracts them.
       If the 'Side' is not 'buy' or 'sell', it returns 'Calculation error'.
    
    Args:
        df (pandas.DataFrame): A DataFrame containing columns 'NBP Rate', 'Traded Volume', 'Currency', 'Commission Currency', 'Commission', and 'Side'.
    
    Returns:
        pandas.DataFrame: The updated DataFrame with the added columns 'PLN Traded Volume', 'PLN Commission', and 'PLN Values minus costs'.
    """
    df['PLN Traded Volume'] = df['NBP Rate'] * df['Traded Volume']
    
    df['PLN Commission'] = df.apply(
    lambda row: row['NBP Rate'] * row['Commission'] if row['Currency'] == row['Commission Currency'] else 'Currency error',
    axis=1)

    df['PLN Values minus costs'] = df.apply(
    lambda row: row['PLN Traded Volume'] + row['PLN Commission'] if row['Side'] == 'buy' else 
    (row['PLN Traded Volume'] - row['PLN Commission'] if row['Side'] == 'sell' else 'Calculation error'), axis=1)
    
    return df

def main():
    FOLDER = 'csv_files'
    csv_file = r'csv_files\Akcje.csv'
    df = import_transactions(csv_file)
    add_exchange_rate(df)
    calculate_pln_values(df)
    df = df.sort_values(by=['Symbol ID', 'Time'])
    # print(df)
    print(df.to_string()) ### Present all rows.
    # write_to_excel(df, FOLDER)


if __name__ == "__main__":
    main()