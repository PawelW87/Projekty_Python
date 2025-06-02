Tytuł projektu

„Program do obliczania należnego podatku od zysków giełdowych, obsługujący pliki CSV od brokerów oraz transakcje z lat ubiegłych. Dodatkowy moduł testowy umożliwia weryfikację podstawowych funkcji programu.”

Funkcjonalności:

1. Obsługa plików CSV od brokera (import_transactions):

Wczytuje plik CSV zawierający dane transakcji giełdowych i przekształca go w DataFrame Pandas z wybranymi kolumnami, dostosowując niektóre dane do dalszego przetwarzania.
Szczegóły działania:
Wczytywanie danych:

Funkcja wykorzystuje bibliotekę Pandas do odczytu pliku CSV.

Obsługiwany format:

Separator: tabulator (\t).

Kodowanie: UTF-16.

Nagłówki: w pierwszym wierszu pliku.

Wczytywane kolumny:

Time: Czas transakcji.

Side: Typ transakcji (np. kupno/sprzedaż).

Symbol ID: Identyfikator instrumentu finansowego.

ISIN: Międzynarodowy numer identyfikacyjny papierów wartościowych.

Price: Cena jednostkowa.

Currency: Waluta transakcji.

Quantity: Liczba jednostek transakcyjnych.

Commission: Prowizja brokera.

Commission Currency: Waluta prowizji.

Traded Volume: Całkowita wartość transakcji.

Przetwarzanie danych:

Kolumna Time jest automatycznie konwertowana na obiekty datetime Pandas.

Zwracana wartość:

DataFrame zawierający wybrane kolumny, gotowy do dalszej obróbki.

Potencjalne błędy:
Brak pliku lub błędna ścieżka.

Plik niezgodny ze strukturą:

Brak wymaganych kolumn.

Niewłaściwe kodowanie.

Problemy z konwersją dat w kolumnie Time.

2. Pobranie kursu waluty (assign_exchange_rate):

Dodaje do DataFrame informacje o kursie wymiany waluty na PLN oraz datę kursu, wykorzystując dane z API NBP.
Szczegóły działania:
Funkcja tworzy nowe kolumny:

NBP Rate: Kurs wymiany na PLN.

NBP Date: Data użytego kursu.

Dla każdej transakcji wywołuje funkcję assign_exchange_rate, aby obliczyć kurs i przypisać odpowiednią datę.

Zwraca zaktualizowany DataFrame.

Opis funkcji: assign_exchange_rate
Cel: Określa kurs wymiany waluty na PLN oraz odpowiednią datę dla każdej transakcji.

Szczegóły działania:
Pobiera walutę i datę z wiersza DataFrame.

Jeśli waluta to PLN:

Ustawia kurs wymiany na 1.

Datę kursu ustala na datę transakcji.

Jeśli waluta jest inna niż PLN:

Wywołuje funkcję get_nbp_exchange_rate, aby pobrać kurs z API NBP.

Zwraca kurs i datę w formie serii Pandas.

Opis funkcji: get_nbp_exchange_rate
Cel: Pobiera kurs wymiany waluty z API NBP dla danego dnia lub najbliższego wcześniejszego dnia roboczego.

Szczegóły działania:
Wejście:

currency: Kod waluty w formacie trzyliterowym (np. USD, EUR).

date: Data transakcji w formacie datetime.

Przetwarzanie:

Sprawdza API NBP dla kursu waluty na dzień poprzedzający podaną datę.

Jeśli kursu brak (np. weekend lub święto), cofa się o jeden dzień i ponawia próbę.

Wyjście:

rate: Kurs wymiany waluty.

rate_date: Data obowiązywania kursu.

Komunikaty diagnostyczne:

Informuje użytkownika, gdy brakuje kursu dla danego dnia, i szuka kursu dla wcześniejszych dni.

Potencjalne błędy i wyjątki:
Brak połączenia z API NBP.

Nieprawidłowy format waluty.

Kurs waluty niedostępny dla podanej daty i wcześniejszych.

3. Przeliczanie wartości z walut obcych na PLN(calculate_pln_values):
Dodawane kolumny:
PLN Traded Volume:

Reprezentuje wartość transakcji (Traded Volume) przeliczoną na PLN za pomocą kursu NBP.

Obliczenie: NBP Rate * Traded Volume.

PLN Commission:

Prowizja przeliczona na PLN, jeśli waluta transakcji zgadza się z walutą prowizji.

Jeśli waluty nie zgadzają się, wstawiany jest komunikat Currency error.

PLN INCOME - PRZYCHÓD:

Przychód w PLN dla transakcji typu sell.

Dla innych typów transakcji wartość jest ustawiona na 0.

Parametry wejściowe:
df: DataFrame zawierający dane transakcji.

Kolumny wymagane do działania funkcji:

NBP Rate

Traded Volume

Commission

Currency

Commission Currency

Side

Działanie funkcji:
PLN Traded Volume:

Przelicza wolumen transakcji na PLN.

Kolumna ta jest zawsze uzupełniana poprawnymi wartościami.

PLN Commission:

Sprawdza zgodność walut prowizji i transakcji:

Jeśli waluty się zgadzają, prowizja jest przeliczana na PLN za pomocą kursu NBP.

Jeśli waluty się różnią, wpisuje Currency error jako błąd waluty.

PLN INCOME - PRZYCHÓD:

Dla transakcji typu sell wartość jest równoważna wartości PLN Traded Volume.

Dla pozostałych typów transakcji (buy, inne) wartość wynosi 0.

Zwracane dane:
Zaktualizowany DataFrame z trzema dodatkowymi kolumnami:

PLN Traded Volume

PLN Commission

PLN INCOME - PRZYCHÓD

Uwagi:
Funkcja wymaga, aby wcześniej w DataFrame znajdowała się kolumna NBP Rate, obliczana w funkcji add_exchange_rate.

Brak walidacji dla wartości wejściowych (np. czy Commission jest liczbą). Funkcja zakłada poprawność danych wejściowych.

4. TU SKOŃCZYŁEM 02-06-2025
____________________________________________________________________________________________________

Rozliczanie transakcji giełdowych krajowych i zagranicznych.

Automatyczne oznaczanie nierozliczonych pozycji do przeniesienia na kolejny rok.

Generowanie pliku .xlsx z gotowymi danymi do deklaracji podatkowej.

Moduł testowy do weryfikacji poprawności funkcji programu.

Wymagania

Wymień wymagania techniczne, np.:

Python 3.10+

Biblioteki: pandas, openpyxl, pytest (dla testów)

Struktura plików

Wskaż, jakie pliki znajdują się w projekcie:

main_program.py: Główny program obsługujący dane giełdowe.

test_module.py: Moduł testowy weryfikujący działanie funkcji.

Instrukcja użytkowania

Uruchamianie głównego programu
Opisz, jak przygotować dane i uruchomić program, np.:

bash
Kopiuj
Edytuj
python main_program.py --input dane_brokera.csv --output podatek.xlsx

Uruchamianie modułu testowego

test_kalkulator_akcji.py

Struktura danych wejściowych/wyjściowych

Wyjaśnij format plików CSV i .xlsx:

Dane wejściowe: Plik CSV od brokera (np. kolumny: Data, Instrument, Ilość, Cena, Waluta).

Dane wyjściowe: Plik .xlsx (np. kolumny: Zysk/Strata, Podatek do zapłaty, Uwagi).

Uwagi i ograniczenia

Wspomnij, że oznaczenia nierozliczonych pozycji wymagają uwagi użytkownika.

Autorstwo i kontakt

Dodaj swoje dane kontaktowe lub notkę, np. „Stworzone przez [Twoje Imię]”.