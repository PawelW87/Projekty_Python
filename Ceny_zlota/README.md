Analiza cen złota w PLN i USD oraz kursów USD/PLN

Opis programu

Ten program analizuje dane o cenach złota w PLN za gram oraz kursach USD/PLN, korzystając z API Narodowego Banku Polskiego (NBP). Umożliwia:

Pobranie danych o cenach złota w PLN oraz kursach USD/PLN dla określonego zakresu dat.

Przekształcenie cen złota z PLN na USD za uncję przy użyciu kursów USD/PLN.

Wizualizację:

Wykresu kursu USD/PLN w czasie.

Wykresu cen złota w USD za uncję w czasie.

Eksport przetworzonych danych do pliku CSV.

Wymagane biblioteki

Program wykorzystuje następujące biblioteki Python:

requests - do pobierania danych z API.

pandas - do przetwarzania danych.

plotly - do tworzenia wykresów.

click - do obsługi interfejsu wiersza poleceń.

Aby zainstalować wymagane pakiety, użyj:

pip install requests pandas plotly click

Struktura programu

fetch_gold_price_in_pln(from_date, to_date) - Pobiera ceny złota w PLN za gram dla podanego zakresu dat.

fetch_usd_exchange_rate(from_date, to_date) - Pobiera kursy średnie USD/PLN dla podanego zakresu dat.

calculate_gold_price_in_usd(gold_prices, usd_rates) - Oblicza ceny złota w USD za uncję na podstawie cen w PLN i kursu USD/PLN.

plot_(DF, x_, y_, title_) - Tworzy wykres liniowy na podstawie dostarczonych danych.

Komendy CLI

Program obsługuje kilka komend wiersza poleceń:

usd - Wyświetla wykres kursu USD/PLN w czasie.

gold - Wyświetla wykres cen złota w USD za uncję w czasie.

csv - Zapisuje przetworzone dane do pliku CSV o nazwie gold_prices_usd.csv.

Uruchomienie

Aby uruchomić program, użyj:

python ceny_zlota.py [komenda]

Przykłady:

Wyświetlenie wykresu kursu USD/PLN:

python ceny_zlota.py usd

Wyświetlenie wykresu cen złota w USD:

python ceny_zlota.py gold

Eksport danych do pliku CSV:

python ceny_zlota.py csv

Uwagi

Program domyślnie analizuje dane dla zakresu dat od 2024-01-01 do 2024-12-31. Zakres dat można dostosować, modyfikując zmienne from_date i to_date w funkcji głównej.

API NBP może zwracać różne komunikaty o błędach w przypadku braku danych dla określonego zakresu dat.

W przypadku błędów podczas pobierania danych program wyświetli odpowiednie komunikaty.
