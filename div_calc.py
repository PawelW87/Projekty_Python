import sys
import pandas as pd
import requests
from datetime import datetime, timedelta
from csv_1 import create_path_write

def import_transactions(csv_file):
    """Read CSV"""
    columns_to_load = ['Symbol ID', 'Operation type', 'When', 'Sum', 'Asset', 'Comment']

    df = pd.read_csv(csv_file, sep='\t', header=0, usecols=columns_to_load)
    
    # Conversion of 'When' column for datetime
    df['When'] = pd.to_datetime(df['When'])

    # Usunięcie zbędnych znaków (np. spacje, przecinki) i konwersja 'Sum' na float
    # df['Sum'] = df['Sum'].replace(',', '.', regex=True)  # Zmiana przecinków na kropki (jeśli są)
    df['Sum'] = pd.to_numeric(df['Sum'], errors='coerce')  # Konwersja na float (nieprawidłowe wartości zamienią się na NaN)

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


def main():
    FOLDER = 'csv_files'
    csv_file = r'csv_files\Custom_.csv'
    df = import_transactions(csv_file)
    # print(df.to_string())
    # print(df)
    df_filtered = df[df['Operation type'].isin(['DIVIDEND', 'TAX', 'US TAX'])].copy()
    df_filtered[['NBP Rate', 'NBP Date']] = df_filtered.apply(add_exchange_rate, axis=1)
    print(df_filtered)
    # write_to_csv(df_filtered, FOLDER)


if __name__ == "__main__":
    main()


# def oblicz_podatek_od_dywidend(df):
#     """Filtruje dywidendy i oblicza całkowity podatek"""
#     # Wybieramy tylko operacje związane z dywidendami (przykładowo 'DYWIDENDA' w kolumnie 'Typ')
#     df_dywidendy = df[df['Typ'].str.contains('DIVIDEND', case=False)]
#     calkowita_kwota_dywidend = df_dywidendy['Kwota dywidendy'].sum()
    
#     # Obliczamy podatek (19% od łącznej kwoty dywidend)
#     podatek = 0.19 * calkowita_kwota_dywidend
#     return calkowita_kwota_dywidend, podatek
