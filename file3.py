import sys
import pandas as pd
import requests
from datetime import datetime, timedelta

def import_transactions(csv_file):
    """Read CSV"""
    columns_to_load = ['Symbol ID', 'Operation type', 'When', 'Sum', 'Asset', 'Comment']
    df = pd.read_csv(csv_file, sep=';', header=0, encoding='cp1250', usecols=columns_to_load)
    df['When'] = pd.to_datetime(df['When'], format='%d.%m.%Y %H:%M')

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
            has_date = False            # back one day after
            print(f"Brak kursu dla {currency.upper()} z dnia {format_date}.\nSzukam w poprzednim dniu")  
            new_date -= timedelta(days=1)

    rate = (data["rates"][0]['mid'])
    rate_date = (data["rates"][0]['effectiveDate'])
    return rate, rate_date

def add_exchange_rate(row):
    currency = row['Asset']
    date = row['When']
    sum_ = row['Sum']

    if currency == 'PLN':
        rate = sum_
        rate_date = date.date()
    else:
        rate, rate_date = get_nbp_exchange_rate(currency, date)
    
    return pd.Series([rate, rate_date])


# Wyświetlamy wynik
# print(df[['When', 'Asset', 'kurs NBP', 'data kursu']].head())



def main():
    csv_file = r'csv_files\div2_.csv'
    df = import_transactions(csv_file)
    df_filtered = df[df['Operation type'].isin(['DIVIDEND', 'TAX', 'US TAX'])]
    df_filtered[['NBP Rate', 'NBP Date']] = df_filtered.apply(add_exchange_rate, axis=1)
    print(df_filtered)
    
    
    
    
    # get_nbp_exchange_rate('usd', datetime.strptime('2024-12-09', '%Y-%m-%d'))



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