import sqlite3

# инициализация db.sqlite
conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()

# открываем файл city.txt
fcity = open('city.txt', 'r', encoding='windows-1251')
city = fcity.read().splitlines()  # считываем файл с городами построчно

for i in city:
    query = "INSERT or REPLACE INTO cities VALUES ('{0}')".format(i)
    cursor.execute(query)

conn.commit()
