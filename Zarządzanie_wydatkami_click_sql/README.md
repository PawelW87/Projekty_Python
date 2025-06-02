# Zarządzanie Wydatkami – CLI z SQLite

Ten program pozwala na zarządzanie osobistymi wydatkami przy użyciu bazy danych SQLite oraz wygodnego interfejsu wiersza poleceń (CLI) opartego na bibliotece `click`.

## Funkcjonalności

- **Dodawanie wydatków** – wpisz kwotę i opis, aby zapisać nowy wydatek.
- **Usuwanie wydatków** – usuń wydatek, podając jego unikalne ID.
- **Wyświetlanie raportu** – zobacz listę wszystkich wydatków wraz z ich ID, kwotami i opisami oraz sumę wszystkich wydatków.
- **Import z pliku CSV** – zaimportuj wydatki z pliku CSV (`amount`, `description`).

## Szczegóły techniczne

- Program tworzy i korzysta z bazy SQLite (`budget.db`), gdzie przechowuje tabelę `expenses`.
- Do interakcji z użytkownikiem służy CLI oparte na `click` z następującymi komendami:
  - `add [amount] [description]` – dodaje wydatek.
  - `delete [id]` – usuwa wydatek o podanym ID.
  - `report` – pokazuje listę wydatków i sumę.
  - `import-csv` – importuje wydatki z pliku CSV.

## Struktura bazy danych

Tabela `expenses` posiada kolumny:

| Kolumna      | Typ     | Opis                                  |
|--------------|---------|-------------------------------------|
| `id`         | INTEGER | Unikalny identyfikator (auto increment) |
| `amount`     | REAL    | Kwota wydatku                       |
| `description`| TEXT    | Opis wydatku                       |

## Wymagania

- Python 3.x
- Biblioteki: `sqlite3`, `csv`, `click`, `dataclasses`

## Użycie

Przykłady wywołań programu w terminalu:

```bash
# Wyświetlenie raportu wydatków
python Wydatki_SQL.py report

# Dodanie nowego wydatku
python Wydatki_SQL.py add 150.50 "Zakupy spożywcze"

# Usunięcie wydatku o ID 2
python Wydatki_SQL.py delete 2

# Import wydatków z pliku CSV
python Wydatki_SQL.py import-csv
```

Uwagi
Program oznacza wydatki powyżej 1000 jako duże (oznaczenie (!)).

W przypadku błędów (np. nieprawidłowa kwota lub brak pliku CSV) program informuje użytkownika i kończy działanie.