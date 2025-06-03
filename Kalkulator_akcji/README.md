To jest program do obliczania należnego podatku od zysków giełdowych, obsługujący pliki CSV od brokera Exante oraz transakcje z lat ubiegłych. Dodatkowy moduł testowy umożliwia weryfikację podstawowych funkcji programu. 

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
Cel: Pobiera kurs wymiany waluty z API NBP dla poprzedniego dnia lub najbliższego wcześniejszego dnia roboczego.

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


4. Opcjonalne ręczne wprowadzanie danych (add_manual_transaction).

Pozwala użytkownikowi ręcznie dodać transakcję do DataFrame. Funkcja jest przydatna do wprowadzania transakcji niestandardowych, takich jak zakupy z lat poprzednich.

Działanie funkcji:
Pętla interaktywna:

Funkcja działa w pętli, pytając użytkownika, czy chce dodać nową transakcję.

Opcje:

y: Rozpoczyna proces dodawania transakcji.

n: Przerywa działanie funkcji i zwraca DataFrame.

Wprowadzanie danych:

Użytkownik wprowadza szczegóły transakcji:

Symbol ID: Unikalny identyfikator symbolu giełdowego.

Time: Data i godzina transakcji w formacie YYYY-MM-DD HH:MM:SS.

Quantity: Ilość instrumentów finansowych.

PLN Traded Volume: Kwota transakcji przeliczona na PLN.

PLN Commission: Prowizja transakcji w PLN.

Tworzenie nowej transakcji:

Nowa transakcja jest tworzona jako tymczasowy DataFrame z predefiniowanymi wartościami:

Kolumny wymagane przez inne funkcje, takie jak NBP Rate, Currency, Commission Currency, są domyślnie uzupełniane (np. NBP Rate = 1 dla transakcji w PLN).

Potwierdzenie transakcji:

Użytkownik może zatwierdzić lub odrzucić wprowadzoną transakcję:

y: Transakcja jest dodawana do głównego DataFrame.

n: Transakcja zostaje odrzucona.

Obsługa błędów:

Funkcja wykrywa błędy wprowadzania danych (np. nieprawidłowy format daty lub liczby).

W przypadku błędu użytkownik jest proszony o ponowne wprowadzenie danych.

Parametry wejściowe:
df: Główny DataFrame z istniejącymi transakcjami.

Zwracane dane:
Zaktualizowany DataFrame z ręcznie dodanymi transakcjami.

Uwagi:
Wszystkie ręcznie dodane transakcje zakładają, że waluta to PLN (ustawione domyślnie).

Funkcja nie umożliwia edycji ani usuwania już dodanych transakcji – jedynie ich zatwierdzanie lub odrzucanie w momencie wprowadzania.

Obsługa walut innych niż PLN wymagałaby dodatkowego mechanizmu weryfikacji i przeliczeń. Autor zakłada, że kursy ręcznie dodawanych transakcji zostały obliczone w ubiegłym roku.

5. Obliczanie zysków i kosztów (Funkcja: calculate_profit)

Cel:
Oblicza zyski i koszty dla transakcji typu "sell", dopasowując je do wcześniejszych transakcji "buy" według zasady FIFO. Zysk jest różnicą między wartością sprzedaży a kosztami zakupu, uwzględniającymi proporcjonalne prowizje.

Kroki działania funkcji:
Tworzenie struktur pomocniczych:

fifo_queues: Słownik przechowujący kolejki FIFO dla każdej unikalnej wartości Symbol ID.

Listy: profits, costs, status, warnings do przechowywania wyników dla każdej transakcji.

Iterowanie przez wiersze DataFrame:

Dla każdej transakcji sprawdzane jest pole Side:

buy:

Transakcja dodawana do odpowiedniej kolejki FIFO.

Zysk i koszt ustawiane na NaN.

sell:

Wartości transakcji "sell" są dopasowywane do "buy" z kolejki FIFO.

Jeśli brakuje odpowiednich transakcji "buy", funkcja zgłasza ostrzeżenie.

Koszty są wyliczane proporcjonalnie, uwzględniając prowizje.

Obliczany jest zysk jako różnica wartości "sell" i kosztów.

Inne wartości w Side:

Zysk i koszt ustawiane na NaN, bez zmian w kolejce.

Obsługa przypadku braku zakupów lub niedopasowania ilości:

Jeśli dla "sell" nie ma odpowiednich "buy", funkcja dodaje wpis w kolumnie Warnings.

Jeśli ilość w "buy" jest niewystarczająca, transakcja zostaje oznaczona jako Check.

Dostosowanie transakcji "buy":

W przypadku częściowego wykorzystania transakcji "buy", pozostała ilość jest zwracana do kolejki.

Dodanie kolumn do DataFrame:

COSTS - KOSZT: Koszty związane z transakcją.

PROFIT - DOCHÓD: Zysk dla transakcji typu "sell".

STATUS: Status przetwarzania transakcji.

Warnings: Ostrzeżenia dotyczące braków lub błędów w dopasowaniu.

Parametry:
df: DataFrame zawierający kolumny:

Symbol ID, Side, Quantity, PLN Traded Volume, PLN Commission.

Zwracane dane:
DataFrame: Oryginalny DataFrame uzupełniony o kolumny:

COSTS - KOSZT, PROFIT - DOCHÓD, STATUS, Warnings.

Uwagi:
Funkcja zakłada, że dane wejściowe są poprawne, a transakcje "sell" nie przekraczają całkowitej ilości "buy" dla danego Symbol ID.

Jeśli brakuje transakcji "buy" lub ilość jest niewystarczająca, użytkownik otrzyma ostrzeżenia w kolumnie Warnings.

Rozliczanie prowizji uwzględnia proporcje między transakcjami "buy" i "sell".


6. Przypisanie do dochodu symbolu kraju giełdy - zgodnie z wymogami dla rozliczeń z Urzędem skarbowym (map_exchange_to_country).

Cel:
Mapuje identyfikatory giełd papierów wartościowych (zawarte w Symbol ID) na kody krajów na podstawie transakcji typu "sell".

Kroki działania funkcji:
Tworzenie mapowania exchange_to_country:

Słownik przypisuje identyfikator giełdy (np. "WSE", "XETRA") do kodu kraju (np. "PL", "DE").

Dla nieznanych giełd funkcja zwróci "UNKNOWN".

Niektóre giełdy wymagają weryfikacji ("Check").

Definiowanie funkcji pomocniczej get_country:

Sprawdza wartość w kolumnie Side:

Jeśli wartość to "sell", funkcja wyodrębnia kod giełdy z pola Symbol ID (część po ostatniej kropce).

Wyszukuje kod kraju w słowniku exchange_to_country. Jeśli kod giełdy nie istnieje w słowniku, zwraca "UNKNOWN".

Jeśli Side różni się od "sell", funkcja zwraca None.

Dodanie kolumny Exchange country:

Funkcja apply() wywołuje get_country dla każdego wiersza, tworząc nową kolumnę z kodami krajów.

Zwracany wynik:

Oryginalny DataFrame z dodatkową kolumną Exchange country.

Parametry:
df: DataFrame zawierający kolumny:

Symbol ID — identyfikator symbolu, w którym znajduje się giełda (np. "ABC.WSE").

Side — typ transakcji (np. "buy", "sell").

Zwracane dane:
DataFrame: Zawiera oryginalne dane oraz kolumnę:

Exchange country — kod kraju (np. "PL", "DE") lub None dla transakcji innych niż "sell".

Przykład działania:
Dane wejściowe:

Symbol ID	Side
ABC.WSE	sell
DEF.XETRA	sell
GHI.NASDAQ	buy

Dane wyjściowe:

Symbol ID	Side	Exchange country
ABC.WSE	sell	PL
DEF.XETRA	sell	DE
GHI.NASDAQ	buy	None

Uwagi:
Funkcja zakłada, że Symbol ID zawsze zawiera kod giełdy po ostatniej kropce.

Jeśli identyfikator giełdy nie istnieje w exchange_to_country, zwracane jest "UNKNOWN".

Transakcje inne niż "sell" są ignorowane (kolumna Exchange country ma wartość None).


7. Zapis DataFrame do pliku excel (write_to_excel i create_path_write).

Cel: Zapisuje DataFrame do pliku Excel w folderze określonym przez użytkownika. Użytkownik podaje nazwę pliku w trakcie działania programu.

Szczegóły implementacji:
write_to_excel(df, folder):

Funkcja zapisuje dany DataFrame do pliku Excel.

Plik jest tworzony w folderze wskazanym w parametrze folder.

Wywołuje funkcję pomocniczą create_path_write(folder) do uzyskania pełnej ścieżki do pliku.

Obsługuje potencjalne wyjątki (np. błędy zapisu do pliku) i wyświetla odpowiedni komunikat.

create_path_write(folder):

Funkcja prosi użytkownika o nazwę pliku bez rozszerzenia.

Dodaje rozszerzenie .xlsx do podanej nazwy.

Łączy nazwę pliku z podanym folderem za pomocą os.path.join.

Parametry:
df: DataFrame do zapisania.

folder: Ścieżka do folderu, w którym zostanie zapisany plik.

Zwracane dane:
Funkcja create_path_write zwraca pełną ścieżkę do pliku jako string.

Funkcja write_to_excel nie zwraca wartości, lecz zapisuje plik w określonym miejscu.

Uwagi:
Obsługa błędów:

Jeśli podana ścieżka jest nieprawidłowa (np. brak uprawnień zapisu), funkcja poinformuje o błędzie.


Wymagania

Python 3.10+

Biblioteki: pandas, os, requests, numpy, datetime

Pliki w projekcie:

Kalkulator_akcji.py - Główny program obsługujący dane giełdowe.
README.md
test_kalkulator_akcji.py - Testowy program zawierający dane do testowania strategicznych funkcji programu.

Autorstwo i kontakt:
Stworzone przez Paweł Wojtyński.

## Licencja

Ten projekt jest licencjonowany na zasadach licencji MIT. Szczegóły znajdziesz w pliku LICENSE.