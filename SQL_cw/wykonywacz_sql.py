import sqlite3

conn = sqlite3.connect('SQL_cw/pracownicy.db')
with open('SQL_cw/moje_pytania.sql', 'r') as file:
        sql_script = file.read()

cursor = conn.cursor()
cursor.execute(sql_script)
pracownicy = cursor.fetchall()  # Pobiera wszystkie wiersze z wyniku

for p in pracownicy:
    print(p)