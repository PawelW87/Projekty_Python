"""
Ten program analizuje ceny złota w PLN za gram oraz kurs USD/PLN na podstawie danych pobranych z API NBP. 
Program umożliwia:

1. Pobranie danych o cenach złota w PLN oraz kursach USD/PLN dla określonego zakresu dat.
2. Przekształcenie cen złota w PLN na ceny w USD za uncję przy użyciu kursów USD/PLN.
3. Wizualizację:
   - Wykres kursu USD/PLN w czasie.
   - Wykres cen złota w USD w czasie.
4. Eksport przetworzonych danych do pliku CSV.

Wykorzystuje biblioteki `requests`, `pandas`, `plotly` oraz `click` do realizacji funkcjonalności.
"""

import pandas as pd
import plotly.express as px
import requests
from datetime import datetime

import click

def fetch_gold_price_in_pln(from_date, to_date):
    """
    Pobiera ceny złota w PLN za gram z API NBP dla podanego zakresu dat.
    """
    url = f"https://api.nbp.pl/api/cenyzlota/{from_date}/{to_date}/?format=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        # print("Gold data structure:", data)  # Diagnostyka
        return data
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
        # print("USD rates structure:", data)  # Diagnostyka
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

def plot_(DF, x_, y_, title_):
    """
    Tworzy wykres liniowy na podstawie dostarczonych danych.

    Parameters:
    DF: pandas.DataFrame
        DataFrame zawierający dane do wykresu.
    x_: str
        Nazwa kolumny w DataFrame użytej jako oś X.
    y_: str
        Nazwa kolumny w DataFrame użytej jako oś Y.
    title_: str
        Tytuł wykresu.
    """
    fig = px.line(DF, x=x_, y=y_, title=title_)
    fig.show()

@click.group()
@click.pass_context
def cli(ctx):
    """
    Program analizujący ceny złota i kurs USD/PLN.
    """
    print("Hello! Przygotowuję dane...")
    ctx.ensure_object(dict)   # Tworzenie obiektu kontekstu

    # Zakres dat
    from_date = "2024-01-01"
    to_date = "2024-12-31"

    # Pobieranie danych
    gold_prices = fetch_gold_price_in_pln(from_date, to_date)
    usd_rates = fetch_usd_exchange_rate(from_date, to_date)
    
    if gold_prices and usd_rates:
        ctx.obj['DF'] = calculate_gold_price_in_usd(gold_prices, usd_rates)
    else:
        print("Nie udało się pobrać danych.")
    
@cli.command()
@click.pass_context
def usd(ctx):
    """
    Wyświetla wykres kursu USD/PLN w czasie.
    """
    DF = ctx.obj['DF']
    if DF is not None:
        plot_(DF, 'data', 'mid', 'Kurs USD/PLN w czasie')
    else:
        print("Brak danych do wyświetlenia.")

@cli.command()
@click.pass_context
def gold(ctx):
    """
    Wyświetla wykres cen złota w USD w czasie.
    """
    DF = ctx.obj['DF']
    if DF is not None:
        plot_(DF, 'data', 'gold_price_usd', 'Wykres cen złota')
    else:
        print("Brak danych do wyświetlenia.")

@cli.command()
@click.pass_context
def csv(ctx):
    """
    Zapisuje dane do pliku CSV.
    """
    DF = ctx.obj['DF']
    if DF is not None:
        DF.to_csv('gold_prices_usd.csv', index=False)
        print("Dane zapisane do pliku 'gold_prices_usd.csv'")
    else:
        print("Brak danych do zapisania.")

if __name__ == "__main__":
    cli()

# python D:\IT\folder_do_cwiczen\ceny_zlota.py usd