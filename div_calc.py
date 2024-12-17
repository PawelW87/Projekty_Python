import pandas as pd
import requests
from datetime import datetime, timedelta
from csv_1 import create_path_write


def import_transactions(csv_file):
    """
    Reads CSV. Creates DataFrame with useful columns. Converts 'When' column to datetime objects.
    """
    columns_to_load = ['Symbol ID', 'Operation type', 'When', 'Sum', 'Asset', 'Comment']

    df = pd.read_csv(csv_file, sep='\t', header=0, encoding='utf-16', usecols=columns_to_load)
    
    df['When'] = pd.to_datetime(df['When'])

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

    currency = row['Asset']
    date = row['When']
    
    if currency == 'PLN':
        rate = 1
        rate_date = date.date()
    else:
        rate, rate_date = get_nbp_exchange_rate(currency, date)
    
    return pd.Series([rate, rate_date])

def write_to_csv(df, folder):
    try:
        df.to_excel(create_path_write(folder), index=False, header=True)
        print(f"Writing successful")
    except Exception as e:
        print(f"Unexpected error: {e}")

def calc_the_tax(df):
    """
    Shows the difference between tax already paid and tax due. If greater than zero, additional payment in Poland must be made.
    """
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

def check_tax_corrections(df):
    """
    Assigning the 'KOREKTA' word to the 'Dopłata' column if word 'recalculation' is in 'Comment'
    """
    df['Dopłata'] = df['Dopłata'].where(~df['Comment'].str.contains('recalculation', case=False), 'KOREKTA')
    return df

def show_FUNDING_WITHDRAWAL(df):
    """
    Present fundings and withdrawals
    """
    df_FUNDING_WITHDRAWAL = df[df['Operation type'].isin(['FUNDING/WITHDRAWAL'])].copy()  
    total_sum = df_FUNDING_WITHDRAWAL['Sum'].sum()
    print(df_FUNDING_WITHDRAWAL)
    print(f"Suma wpłat i wypłat to: {total_sum} EUR")

def main():
    FOLDER = 'csv_files'
    csv_file = r'csv_files\div2.csv'
    df = import_transactions(csv_file)
    # print(df.to_string()) ### Present all rows.
    # print(df)
    # show_FUNDING_WITHDRAWAL(df)
    df_filtered = df[df['Operation type'].isin(['DIVIDEND', 'TAX', 'US TAX'])].copy()
    df_filtered[['NBP Rate', 'NBP Date']] = df_filtered.apply(add_exchange_rate, axis=1)
    df_filtered['PLN Sum'] = df_filtered['NBP Rate'] * df_filtered['Sum']
    df_filtered.loc[df_filtered['Operation type'] == 'DIVIDEND', '19% TAX'] = df_filtered['PLN Sum'] * 0.19
    df_filtered2 = check_tax_corrections(calc_the_tax(df_filtered))
    print(df_filtered2)
    # write_to_csv(df_filtered2, FOLDER)


if __name__ == "__main__":
    main()