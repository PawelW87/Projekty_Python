import csv 
from dataclasses import dataclass
import sys
import sqlite3
from typing import List


import click

BIG_EXPENSE_THRESHOLD = 1000
DB_FILE = 'budget.db'


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
    csv_file = r'D:\IT\Praktyczny_Python_\M07\expenses.csv'
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


# python D:\IT\folder_do_cwiczen\M07_SQL.py report
# python D:\IT\folder_do_cwiczen\M07_SQL.py import-csv
# python D:\IT\folder_do_cwiczen\M07_SQL.py add
# python D:\IT\folder_do_cwiczen\M07_SQL.py delete