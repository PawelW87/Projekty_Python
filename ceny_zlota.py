import pandas as pd
import plotly.express as px
import requests
from datetime import datetime

def fetch_gold_price_in_pln(from_date, to_date):
    """
    Pobiera ceny złota w PLN za gram z API NBP dla podanego zakresu dat.
    """
    url = f"https://api.nbp.pl/api/cenyzlota/{from_date}/{to_date}/?format=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas pobierania cen złota: {e}")
        return None


def fetch_usd_exchange_rate(from_date, to_date):
    """
    Pobiera kursy średnie USD/PLN z API NBP dla podanego zakresu dat.
    """
    url = f"https://api.nbp.pl/api/exchangerates/rates/A/USD/{from_date}/{to_date}/?format=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['rates']  # API NBP zwraca listę kursów w polu 'rates'
    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas pobierania kursów USD/PLN: {e}")
        return None


def calculate_gold_price_in_usd(gold_prices, usd_rates):
    """
    Oblicza ceny złota w USD za uncję na podstawie cen w PLN za gram i kursu USD/PLN.
    """
    # Konwersja danych na DataFrame dla łatwiejszego przetwarzania
    gold_df = pd.DataFrame(gold_prices)
    usd_df = pd.DataFrame(usd_rates)
    
    # Konwersja kolumny 'effectiveDate' w USD na typ datetime
    gold_df['data'] = pd.to_datetime(gold_df['data'])
    usd_df['effectiveDate'] = pd.to_datetime(usd_df['effectiveDate'])

    # Łączenie danych na podstawie dat
    merged_df = pd.merge(gold_df, usd_df, left_on='data', right_on='effectiveDate', how='inner')

    # Obliczanie ceny złota w USD za uncję
    merged_df['gold_price_usd'] = (merged_df['cena'] / merged_df['mid']) * 31.1035

    # Zwrócenie wyników
    return merged_df[['data', 'cena', 'mid', 'gold_price_usd']]


# Główna część programu
from_date = "2024-01-01"
to_date = "2024-12-30"

gold_prices = fetch_gold_price_in_pln(from_date, to_date)
usd_rates = fetch_usd_exchange_rate(from_date, to_date)

if gold_prices and usd_rates:
    result_df = calculate_gold_price_in_usd(gold_prices, usd_rates)
    # print(result_df)
    # result_df.to_csv('gold_prices_usd.csv', index=False)  # Zapis wyników do pliku CSV
    # print("Dane zapisane do pliku 'gold_prices_usd.csv'")
else:
    print("Nie udało się pobrać danych.")



fig = px.line(result_df, x='data', y='gold_price_usd', title='Wykres cen złota')
fig.show()




