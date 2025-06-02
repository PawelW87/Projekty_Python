"""
Ten program umożliwia zarządzanie wydatkami osobistymi z wykorzystaniem bazy danych SQLite. 
Dostępne funkcjonalności obejmują:

1. **Dodawanie wydatków**: Użytkownik może dodawać nowe wydatki z kwotą oraz opisem.
2. **Usuwanie wydatków**: Użytkownik może usunąć wydatki, podając ich unikalne ID.
3. **Wyświetlanie raportu**: Program generuje listę wszystkich wydatków wraz z ich identyfikatorami, kwotami oraz opisami, a także oblicza łączną sumę wydatków.
4. **Import z pliku CSV**: Możliwość zaimportowania wydatków z pliku CSV z danymi w formacie `amount` i `description`.

### Struktura programu:
- **Baza danych SQLite**: Program automatycznie tworzy tabelę `expenses` w pliku `budget.db`, jeśli tabela nie istnieje.
- **Interfejs CLI**: Dzięki bibliotece `click` program obsługuje różne komendy w wierszu poleceń:
  - `add`: Dodaje nowy wydatek.
  - `delete`: Usuwa istniejący wydatek według jego ID.
  - `report`: Wyświetla listę wydatków i sumę wydatków.
  - `import-csv`: Importuje dane z pliku CSV.
  
Program wymaga pliku CSV o nazwie `expenses.csv` w katalogu `D:\IT\Portfolio\Zarządzanie_wydatkami_click_sql\expenses.csv` przy imporcie wydatków.

### Wymagane biblioteki:
- `sqlite3`: Do obsługi bazy danych SQLite.
- `csv`: Do wczytywania danych z pliku CSV.
- `click`: Do tworzenia interfejsu wiersza poleceń.
- `dataclasses`: Do modelowania wydatków w postaci obiektów klasy `Expense`.

Przykłady użycia:
- Wyświetlenie raportu:
python D:\IT\Portfolio\Zarządzanie_wydatkami_click_sql\Wydatki_SQL.py report
- Dodanie nowego wydatku:
python D:\IT\Portfolio\Zarządzanie_wydatkami_click_sql\Wydatki_SQL.py add 150.50 "Zakupy spożywcze"
- Usunięcie wydatku o ID 2:
python D:\IT\Portfolio\Zarządzanie_wydatkami_click_sql\Wydatki_SQL.py delete 2
- Importowanie wydatków z pliku CSV:
python D:\IT\Portfolio\Zarządzanie_wydatkami_click_sql\Wydatki_SQL.py import-csv
"""

import csv 
from dataclasses import dataclass
import sys
import sqlite3
from typing import List

import click

BIG_EXPENSE_THRESHOLD = 1000
DB_FILE = r'D:\IT\Portfolio\Zarządzanie_wydatkami_click_sql\budget.db'

@dataclass
class Expense:
    id: int
    amount: float
    description: str

    def __post_init__(self):
        if self.amount <=0:
            raise ValueError("Amount cannot be zero or negative")

def initialize_db():
    """Initialize the database and create table if it doesn't exist."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            description TEXT NOT NULL
            )"""
        )

def fetch_expenses() -> List[Expense]:
    """Fetch all expenses from the database."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute("SELECT id, amount, description FROM expenses")
        return [Expense(*row) for row in cursor.fetchall()]

def insert_expense(amount: float, description: str):
    """Insert a new expense into the database"""
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "INSERT INTO expenses (amount, description) VALUES (?, ?)",
            (amount, description),
        )

def delete_expense(number: int):
    """Remove an expense from database."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "DELETE FROM expenses WHERE id=?", (number,)
        )

def compute_total() -> float:
    """Compute the total of all expenses."""
    with sqlite3.connect(DB_FILE) as conn:
        total = conn.execute("SELECT SUM(amount) FROM expenses").fetchone()[0]
        return total if total is not None else 0.0


def display(expenses: List[Expense], total: float):
    """Displays list of exepenses"""
    if expenses:
        print(f"{'ID':<8}{'Amount':<9}{'BIG?':<3}    {'Opis':<10}")
        for row in expenses:
            if row.id is None or row.amount is None:
                print(f"Invalid data found: {row}")
                continue  # Pomija wiersz z błędnymi danymi

            if row.amount >= BIG_EXPENSE_THRESHOLD:
                big = '(!)'
            else:
                big = ''
            print(f"{row.id:<8}{row.amount:<9}{big:^3}     {row.description:<10}")
        print(f"{'TOTAL:':<8}{total:<9}")
    else:
        print("No expenses recorded yet.")

  
@click.group()
def cli():
    """Expenses management"""
    initialize_db()

@cli.command()
def report():
    """Displays the existing list of expenses"""
    expenses = fetch_expenses()
    total = compute_total()
    display(expenses, total)

@cli.command()
@click.argument('amount', type=float)
@click.argument('description')
def add(amount, description):
    """Adds a new expense."""
    try:
        insert_expense(amount, description)
    except ValueError as e:
        print(f'Error: {e}')
        sys.exit(1)
    print("Expense added successfully.")

@cli.command()
@click.argument('number', type=int)
def delete(number):
    """Delete an expense. (ID)"""
    try:
        delete_expense(number)
    except ValueError as e:
        print(f'Error: {e}')
        sys.exit(1)
    print("Expense deleted successfully.")

@cli.command()
def import_csv():
    """Imports expenses from a CSV file."""
    csv_file = r'D:\IT\Portfolio\Zarządzanie_wydatkami_click_sql\expenses.csv'
    try:
        with open(csv_file, encoding="utf-8") as stream:
            reader = csv.DictReader(stream) 
            for row in reader:
                try:
                    amount = float(row['amount'])
                    description = row['description']
                    insert_expense(amount, description)
                except ValueError:
                    print(f"Invalid data in row: {row}")
    except FileNotFoundError:
        print("CSV file not found.")
        sys.exit(1)
    print("Expenses imported from CSV.")


if __name__ == "__main__":
    cli()