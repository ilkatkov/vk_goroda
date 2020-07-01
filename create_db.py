# создание базы данных и таблицы для Города (vk version)

# импорт библиотек
import sqlite3
import os

# создаем файл db.sqlite, если его не существует
if os.path.exists("db.sqlite") == False:
    db_file = open("db.sqlite", 'w')
    db_file.close()

# подключение к db.sqlite
conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()

# создание таблицы в db.sqlite
cursor.execute("""CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, surname TEXT, points INTEGER, last_letter TEXT, last_word TEXT)""")
cursor.execute("""CREATE TABLE steps (id INTEGER, words TEXT)""")
cursor.execute("""CREATE TABLE cities (city TEXT)""")

# закрываем соединение с db.sqlite
conn.commit()

print("OK")