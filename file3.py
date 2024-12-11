import pandas as pd
import requests
from datetime import datetime, timedelta

def wczytaj_transakcje(plik_csv):
    """Wczytuje plik CSV"""
    columns_to_load = ['Symbol ID', 'Operation type', 'When', 'Sum', 'Asset', 'Comment']
    df = pd.read_csv(plik_csv, sep=';', header=0, encoding='cp1250', usecols=columns_to_load)
    df['When'] = pd.to_datetime(df['When'], format='%d.%m.%Y %H:%M')

    return df


def get_nbp_exchange_rate(currency, date):
    
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
        except:                                 # A jak nie wyjdzie to sprawdzimy czy w ogóle waluta istnieje w tabeli
            has_date = False            # cofamy datę o 1 dzień
            print(f"Brak kursu dla {currency.upper()} z dnia {format_date}.\nSzukam w poprzednim dniu")  
            new_date -= timedelta(days=1)

    nbp_rate = (data["rates"][0]['mid'])
    nbp_date = (data["rates"][0]['effectiveDate'])
    print(nbp_rate, nbp_date)
    return nbp_date, nbp_rate

def oblicz_podatek_od_dywidend(df):
    """Filtruje dywidendy i oblicza całkowity podatek"""
    # Wybieramy tylko operacje związane z dywidendami (przykładowo 'DYWIDENDA' w kolumnie 'Typ')
    df_dywidendy = df[df['Typ'].str.contains('DIVIDEND', case=False)]
    calkowita_kwota_dywidend = df_dywidendy['Kwota dywidendy'].sum()
    
    # Obliczamy podatek (19% od łącznej kwoty dywidend)
    podatek = 0.19 * calkowita_kwota_dywidend
    return calkowita_kwota_dywidend, podatek

def main():
    plik_csv = r'csv_files\div2_.csv'
    df = wczytaj_transakcje(plik_csv)
    # print(df)
    df_filtered = df[df['Operation type'].isin(['DIVIDEND', 'TAX', 'US TAX'])]
    print(df_filtered)
    
    
    
    
    # get_nbp_exchange_rate('usd', datetime.strptime('2024-12-09', '%Y-%m-%d'))



if __name__ == "__main__":
    main()
