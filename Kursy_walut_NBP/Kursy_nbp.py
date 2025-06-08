import requests, sys
from dateutil import parser
from datetime import datetime, timedelta

#### Predefinicja waluty (3 litery)
def is_currency(symbol):      
    return len(symbol) == 3 and symbol.isalpha()

print('Witaj w programie do sprawdzania kursów walut. Dane są pobierane z serwera NBP')

###  POBIERANIE DANYCH OD UŻYTKOWNIKA
date_ask = "Wprowadź datę (YYYY-MM-DD):"
currency_ask = "Wprowadź walutę (3 litery):"
wrong_cur = "Podano nieprawidłową walutę"
wrong_date = "Nieudana próba sformatowania daty."
args = sys.argv[1:]

if len(args) == 2:            #wprowadzono oba argumenty   
    if is_currency(args[0]):
        currency = args[0]
        date = args[1]
    elif is_currency(args[1]):
        currency = args[1]
        date = args[0]
    else:
        print(wrong_cur)
        sys.exit(1)
elif len(args) == 1:          #wprowadzono jeden argument
    if is_currency(args[0]):
        currency = args[0]
        date = input(date_ask)
    else: 
        date = args[0]
        currency = input(currency_ask)
elif len(args) < 1:           #brak arumentu w wierszu poleceń
    date = input(date_ask)
    currency = input(currency_ask)
else:                         #za dużo argumentów w wierszu poleceń
    print("Podano za dużo argumentów")
    sys.exit(1)

#### Sprawdzenie daty i waluty
has_error = False             # Flaga

try:                          #### Przeformatowanie na datetime
    new_date = parser.parse(date)
except:
    print(wrong_date)
    has_error = True

if not is_currency(currency):      #### sprawdza inputy waluty
    print(wrong_cur)
    has_error = True
if has_error:
    sys.exit(1)

###### Sprawdzanie waluty, dnia w NBP. Pobranie danych
has_date = False          # Flaga

while not has_date:
    format_date = new_date.strftime('%Y-%m-%d')
    url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency.lower()}/{format_date}/?format=json"
    url_cur = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency.lower()}?format=json"
    try:                                   # Idziemy na całość
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        has_date = True
    except:                                 # A jak nie wyjdzie to sprawdzimy czy w ogóle waluta istnieje w tabeli
        try:
            resp = requests.get(url_cur)    # Jak jest waluta to...
            resp.raise_for_status()
            if resp.ok:
                has_date = False            # cofamy datę o 1 dzień
                print(f"Brak kursu dla {currency.upper()} z dnia {format_date}.\nSzukam w poprzednim dniu")  
                new_date -= timedelta(days=1)
        except:                            # A jak nie ma waluty to sprawdzamy walutę.
            print(f"Brak podanej waluty ({currency.upper()}) w tabeli A śrenich kursów walut publikowanych przez NBP. Sprawdź walutę.")
            sys.exit(1)

###### Prezentacja wyników
nbp_rate = (data["rates"][0]['mid'])
nbp_date = (data["rates"][0]['effectiveDate'])
nbp_cur = (data["code"])
nbp_name = (data["currency"])
print(f"Kurs {nbp_cur.upper()} ({nbp_name}) względem PLN z dnia: {nbp_date} wynosi: {nbp_rate}")


### Przykładowe uruchomienia:
# python D:\IT\Praktyczny_Python_\M04\M04PROJEKT.py 25.09.2024 usd 
# python D:\IT\Praktyczny_Python_\M04\M04PROJEKT.py us 25.0.2024
# python D:\IT\Praktyczny_Python_\M04\M04PROJEKT.py afn 25,09,2024 usd
# python D:\IT\Praktyczny_Python_\M04\M04PROJEKT.py usd 
# python D:\IT\Praktyczny_Python_\M04\M04PROJEKT.py 25,09,2024
# python D:\IT\Praktyczny_Python_\M04\M04PROJEKT.py 25,09,2024 op