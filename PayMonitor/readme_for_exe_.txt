Zaplacone – Instrukcja obsługi
Opis programu
Zaplacone to prosty program do sprawdzania, którzy klienci zapłacili za zajęcia sportowe na podstawie wyciągu bankowego i listy uczestników.

Program działa na systemie Windows jako plik Zaplacone.exe.
Nie wymaga instalowania Pythona ani dodatkowych narzędzi.

Przygotowanie plików
Lista uczestników:
Przygotuj plik tekstowy o nazwie uczestnicy.txt.
Każda linia powinna mieć format:

Imię Nazwisko, kwota
Przykład:

Jan Kowalski, 150
Anna Nowak, 200
Wyciąg bankowy:
Pobierz wyciąg z konta bankowego w formacie .xlsx (Excel).
Upewnij się, że plik zawiera kolumny:

Nadawca / odbiorca
Kwota
Nazwij plik np. wyciag.xlsx.

Umieść oba pliki (uczestnicy.txt i wyciag.xlsx) w tym samym folderze co program Zaplacone.exe.

Uruchomienie programu
Kliknij dwukrotnie plik Zaplacone.exe.
Program automatycznie przetworzy pliki i wygeneruje raport.
Wynik działania
Po zakończeniu działania programu w folderze pojawi się plik raport.txt.
W pliku raport.txt znajdziesz listę:
Klientów, którzy nie zapłacili (lub zapłacili za mało)
Klientów, którzy zapłacili całą wymaganą kwotę
Uwagi
Program rozpoznaje uczestników na podstawie imienia i nazwiska wpisanego w polu "Nadawca / odbiorca" w wyciągu bankowym.
Jeśli ktoś wpłacił w kilku ratach, kwoty zostaną zsumowane.
Najczęstsze problemy
Brak pliku uczestnicy.txt lub wyciag.xlsx Upewnij się, że oba pliki są w tym samym folderze co program.
Błąd formatu pliku Sprawdź, czy plik uczestnicy.txt ma poprawny format (każda linia: imię nazwisko (musi mieć taką samą kolejność jak w przelewie bankowym), kwota).
Nieprawidłowy format wyciągu bankowego Program wymaga, by wyciąg miał kolumny "Nadawca / odbiorca" oraz "Kwota".
Kontakt
W razie problemów lub pytań skontaktuj się z autorem programu - Paweł Wojtyński.

Dziękuję za korzystanie z Zaplacone!