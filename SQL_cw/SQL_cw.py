import sqlite3

# 1. Połączenie z bazą danych

# Nawiązanie połączenia z bazą (utworzenie pliku "example.db", jeśli nie istnieje)
conn = sqlite3.connect('pracownicy.db')

# Utworzenie obiektu kursora (do wykonywania poleceń SQL)
cursor = conn.cursor()

# 2. Tworzenie tabeli

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS produkty (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     nazwa TEXT NOT NULL UNIQUE,
#     cena REAL NOT NULL,
#     kategoria TEXT
# )
# ''')

# # Zapisanie zmian
# conn.commit()

# 3. Wstawianie danych do tabeli
# cursor.execute('''
# INSERT INTO produkty (nazwa, cena, kategoria) 
# VALUES (?, ?, ?)
# ''', ('Wódka Sobieski', 35, 'alkohol'))

# # Dodanie wielu użytkowników na raz
# users_data = [
#     ('Nóż kuchenny', 125, 'narzędzia'),
#     ('rura miedź', 335, 'przemysł')
# ]

# cursor.executemany('''
# INSERT INTO produkty (nazwa, cena, kategoria) 
# VALUES (?, ?, ?)
# ''', users_data)

# # Zapisanie zmian
# conn.commit()

# 4. Odczytywanie danych

cursor.execute('SELECT * FROM produkty')
produkty = cursor.fetchall()  # Pobiera wszystkie wiersze z wyniku

for p in produkty:
    print(p)

# 5. Filtrowanie danych (WHERE)
cursor.execute('SELECT * FROM produkty WHERE cena > 30')
produkty = cursor.fetchall()
print('\n')
for p in produkty:
    print(p)

# # 6. Aktualizowanie danych
# cursor.execute('''
# UPDATE produkty 
# SET cena = ? 
# WHERE nazwa = ?
# ''', (40, 'rura miedź'))

# # Zapisanie zmian
# conn.commit()

# # 7. Usuwanie danych
# cursor.execute('''
# DELETE FROM produkty 
# WHERE cena < ?
# ''', (30,))

# # Zapisanie zmian
# conn.commit()

# # 8. Obsługa wyjątków (try-except)
# try:
#     cursor.execute('''
#     INSERT INTO users (name, age, email) 
#     VALUES (?, ?, ?)
#     ''', ('Jan Kowalski', 40, 'jan@example.com'))  # Duplikat e-maila
# except sqlite3.IntegrityError as e:
#     print('Błąd: ', e)

# # Zapisanie zmian
# conn.commit()

# #  9. Zamknięcie połączenia
# conn.close()



