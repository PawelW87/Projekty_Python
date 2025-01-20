import sqlite3
con = sqlite3.connect("tutorial.db")
cur = con.cursor()
# cur.execute("CREATE TABLE movies(title, year, score)")
res = cur.execute("SELECT * FROM movies")
tab = res.fetchall()
for t in tab:
    print(t)
# res = cur.execute("SELECT SUM(score) AS total FROM movies WHERE score > 7.9")
# tab = res.fetchall()
# for t in tab:
#     print(t)
# res2 = cur.execute("SELECT title, year FROM movies ORDER BY score DESC")
# title, year = res2.fetchone()
# print(f"The highest scoring Monty Python movie is {title!r}, released in {year}.")

# cur.execute("""
#     INSERT INTO movies VALUES
#         ('Monty Python and the Holy Grail', 1975, 8.2),
#         ('And Now for Something Completely Different', 1971, 7.5)
# """)

# data = [
#     ("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
#     ("Monty Python's The Meaning of Life", 1983, 7.5),
#     ("Monty Python's Life of Brian", 1979, 8.0),
# ]
# cur.executemany("INSERT INTO movies VALUES(?, ?, ?)", data)
# con.commit()
con.close()