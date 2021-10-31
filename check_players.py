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
