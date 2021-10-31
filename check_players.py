<<<<<<< HEAD
import sqlite3

# инициализация db.sqlite
conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()
query = "SELECT * FROM users"
cursor.execute(query)
l = cursor.fetchall()
l = sorted(l, key = lambda points: int(points[3]), reverse=True)

for i in l:
    print(i)
=======
import sqlite3

# инициализация db.sqlite
conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()
query = "SELECT * FROM users"
cursor.execute(query)
l = cursor.fetchall()
l = sorted(l, key = lambda points: int(points[3]), reverse=True)
for i in l:
    print(i)
>>>>>>> d208c912f5c0e2e42da463cc7d4d83c9d99f5894
