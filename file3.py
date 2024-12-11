import pandas as pd

def wczytaj_transakcje(plik_csv):
    """Wczytuje plik CSV, wybierając kolumny związane z dywidendami"""
    # Wczytanie pliku CSV i usunięcie spacji z nazw kolumn
    df = pd.read_csv(plik_csv, sep='', encoding='cp1250', usecols=[2,4,5,6,7,9])
    df.columns = df.columns.str.strip()  # Usunięcie spacji z początku i końca nazw kolumn
 
    # Zmiana nazw kolumn na bardziej czytelne
    df.rename(columns={
        'ID symbolu': 'Akcja', 
        'Rodzaj operacji': 'Typ', 
        'Gdy': 'Data', 
        'Suma': 'Kwota dywidendy', 
        'Aktywa': 'Waluta', 
        'Komentarz': 'Notatka'
    }, inplace=True)


    return df

def oblicz_podatek_od_dywidend(df):
    """Filtruje dywidendy i oblicza całkowity podatek"""
    # Wybieramy tylko operacje związane z dywidendami (przykładowo 'DYWIDENDA' w kolumnie 'Typ')
    df_dywidendy = df[df['Typ'].str.contains('DIVIDEND', case=False)]
    calkowita_kwota_dywidend = df_dywidendy['Kwota dywidendy'].sum()
    
    # Obliczamy podatek (19% od łącznej kwoty dywidend)
    podatek = 0.19 * calkowita_kwota_dywidend
    return calkowita_kwota_dywidend, podatek

def main():
    plik_csv = r'csv_files\div2.csv'
    df = wczytaj_transakcje(plik_csv)
    print("Wczytano transakcje:")
    print(df.to_string())
    # df_dividend = df[df['Typ'] == 'DIVIDEND']
    # print(df_dividend)
    
  
  

if __name__ == "__main__":
    main()
