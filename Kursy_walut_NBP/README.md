README
Program do Sprawdzania Kursów Walut z Serwisu NBP
Ten program pozwala na szybkie sprawdzenie kursu średniego wybranej waluty względem PLN na wybrany dzień, korzystając z danych publikowanych przez Narodowy Bank Polski (NBP).

Funkcje programu
Walidacja wprowadzonych danych:

Sprawdza poprawność kodu waluty (3-literowy symbol zgodny ze standardem ISO 4217).

Weryfikuje format daty.

Pobieranie danych z serwera NBP:

Sprawdza kurs dla podanej daty.

Jeśli kursu nie ma dla wybranego dnia, automatycznie szuka kursu z najbliższego wcześniejszego dnia.

Obsługa błędów:

Informuje o braku danych dla podanej waluty.

Wskazuje na błędy w wprowadzonych danych.

Elastyczność wejścia:

Dane można podać jako argumenty w wierszu poleceń lub wprowadzić ręcznie w trakcie działania programu.

Wymagania
Python 3.7 lub nowszy.

Zainstalowane biblioteki:

requests

python-dateutil

Dostęp do Internetu.

Instalacja
Upewnij się, że masz zainstalowany Python oraz wymagane biblioteki:

pip install requests python-dateutil
Pobierz kod programu i zapisz go jako plik .py.

Uruchomienie programu
Program można uruchomić na dwa sposoby:

1. Podając dane w wierszu poleceń

python program.py <waluta> <data>
Przykład:

python program.py usd 2024-09-25
Możesz zamienić kolejność argumentów:

python program.py 2024-09-25 usd
2. Bez argumentów w wierszu poleceń
W takim przypadku program poprosi o podanie daty i waluty w trakcie działania.

Obsługa błędów
Jeśli podano błędny kod waluty:

Komunikat: Podano nieprawidłową walutę

Jeśli podano datę w złym formacie:

Komunikat: Nieudana próba sformatowania daty.

Jeśli nie znaleziono kursu dla podanego dnia:

Komunikat: Brak kursu dla <waluta> z dnia <data>. Szukam w poprzednim dniu

Jeśli waluta nie występuje w tabeli NBP:

Komunikat: Brak podanej waluty w tabeli A średnich kursów walut publikowanych przez NBP.

Wynik działania programu
Po poprawnym wykonaniu programu zostanie wyświetlony kurs waluty względem PLN:


Kurs USD (dolar amerykański) względem PLN z dnia: 2024-09-24 wynosi: 4.1234
Uwagi
Program korzysta z API NBP dostępnego pod adresem: https://api.nbp.pl.

Obsługuje jedynie waluty zawarte w tabeli A średnich kursów walut.

Format daty akceptowany przez program: YYYY-MM-DD.

Przykłady użycia
Podanie pełnych danych:

python program.py 2024-09-25 usd
Podanie tylko waluty:


python program.py usd
Podanie tylko daty:

python program.py 2024-09-25