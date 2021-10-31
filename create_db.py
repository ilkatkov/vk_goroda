# создание базы данных и таблицы для Города (vk version)

# импорт библиотек
import sqlite3
import os

# создаем файл db.sqlite, если его не существует
if os.path.exists("db.sqlite") == False:
    db_file = open("db.sqlite", 'w')
    db_file.close()
    print("DB create: OK")

# подключение к db.sqlite
conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()
print("DB connect: OK")

# создание таблицы в db.sqlite
cursor.execute(
    """CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, surname TEXT, points INTEGER, last_letter TEXT, last_word TEXT)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS steps (id INTEGER, words TEXT)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS cities (city TEXT)""")
print("Table create: OK")

# закрываем соединение с db.sqlite
conn.commit()

print("\nAdd cities...")
# ------------- заполнение базы данных городами ---------------

# инициализация db.sqlite
conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()
print("DB connect: OK")

# открываем файл city.txt
fcity = open('city.txt', 'r', encoding='utf-8')
city = fcity.read().splitlines()  # считываем файл с городами построчно
print("Open cities.txt: OK")

for i in city:
    query = "INSERT or REPLACE INTO cities VALUES ('{0}')".format(i)
    cursor.execute(query)
print("Insert", len(city), "cities: OK")

conn.commit()
print("Successful!")