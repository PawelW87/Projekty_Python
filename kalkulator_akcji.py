import pandas as pd
import requests
from datetime import timedelta
from csv_1 import create_path_write


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

def add_exchange_rate(row):
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

def calc_the_tax(df):
    """
    Shows the difference between tax already paid and tax due. If greater than zero, additional payment in Poland must be made.
    """
    pass  ##########DO ogarniecia 
    # Divides the DataFrame into rows with 'DIVIDEND' and rows with 'TAX' or 'US TAX'
    dividend_df = df[df['Operation type'] == 'DIVIDEND'][['Symbol ID', 'NBP Date', '19% TAX']]
    tax_df = df[df['Operation type'].isin(['TAX', 'US TAX'])][['Symbol ID', 'NBP Date', 'PLN Sum']]

    # Joines 'DIVIDEND' rows with 'TAX/US TAX' rows based on Symbol ID and NBP Date
    merged_df = pd.merge(dividend_df, tax_df, on=['Symbol ID', 'NBP Date'], how='left')

    # Calculates the sum between '19% TAX' (DIVIDEND) and 'PLN Sum' (TAX/US TAX)
    merged_df['Dopłata'] = merged_df['19% TAX'] + merged_df['PLN Sum']

    # Merges the results with the original table
    df = pd.merge(df, merged_df[['Symbol ID', 'NBP Date', 'Dopłata']], on=['Symbol ID', 'NBP Date'], how='left')
    df.loc[df['Operation type'] != 'DIVIDEND', 'Dopłata'] = None

    return df

def main():
    FOLDER = 'csv_files'
    csv_file = r'csv_files\Akcje.csv'
    df = import_transactions(csv_file)
    # print(df.to_string()) ### Present all rows.
    # print(df)
    df[['NBP Rate', 'NBP Date']] = df.apply(add_exchange_rate, axis=1)
    df['PLN Sum'] = df['NBP Rate'] * df['Traded Volume']
    print(df)
    write_to_excel(df, FOLDER)


if __name__ == "__main__":
    main()