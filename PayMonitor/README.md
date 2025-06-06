README
Polski
Opis
Program "PayMonitor" umożliwia monitorowanie wpłat uczestników i generowanie raportów dotyczących ich statusu płatności. Analizuje dane z listy uczestników oraz wyciągu bankowego, dopasowując wpłaty do oczekiwanych kwot.

Funkcje
Wczytywanie uczestników: Z pliku tekstowego zawierającego nazwiska i oczekiwane kwoty.

Wczytywanie wpłat: Z pliku Excel (XLSX) zawierającego dane o transakcjach.

Dopasowanie wpłat: Przypisuje wpłaty do uczestników na podstawie ich nazwisk.

Generowanie raportu: Tworzy raport w formacie tekstowym, wskazujący kto zapłacił, a kto nie.

Pliki wejściowe
lista_test.txt: Plik tekstowy z listą uczestników w formacie:


Imię Nazwisko, Kwota
Przykład:


Jan Kowalski, 100
Anna Nowak, 200
wyciag_test.xlsx: Plik Excel z wyciągiem bankowym, który zawiera kolumny:

Nadawca / odbiorca: Dane nadawcy płatności (wielowierszowe).

Kwota zlecenia: Kwota wpłaty.

Plik wyjściowy
raport.txt: Raport zawierający:

Listę uczestników, którzy nie zapłacili pełnej kwoty.

Listę uczestników, którzy zapłacili.

Instrukcja uruchamiania
Umieść pliki lista_test.txt i wyciag_test.xlsx w katalogu PayMonitor.

Uruchom program poleceniem:


python nazwa_pliku.py
Raport zostanie zapisany w pliku raport.txt.

English
Description
The "PayMonitor" program tracks participant payments and generates reports on their payment statuses. It analyzes data from a participant list and a bank statement, matching payments to expected amounts.

Features
Participant loading: Reads participants from a text file with names and expected amounts.

Payment loading: Reads payments from an Excel (XLSX) file.

Payment matching: Matches payments to participants based on their names.

Report generation: Creates a text report indicating who has paid and who has not.

Input Files
lista_test.txt: Text file containing a list of participants in the format:


First Last Name, Amount
Example:


John Smith, 100
Anna Brown, 200
wyciag_test.xlsx: Excel file containing the bank statement with the following columns:

Nadawca / odbiorca: Payer information (multiline).

Kwota zlecenia: Payment amount.

Output File
raport.txt: Report containing:

A list of participants who have not fully paid.

A list of participants who have fully paid.

How to Run
Place the lista_test.txt and wyciag_test.xlsx files in the PayMonitor directory.

Run the program with:

python script_name.py
The report will be saved to raport.txt.