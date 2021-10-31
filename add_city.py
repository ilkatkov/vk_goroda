<<<<<<< HEAD
import sqlite3

# инициализация 
conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()

s = input("Vvedite gorod: ").encode('utf8','surrogateescape').decode('utf8','surrogateescape')

query = "INSERT or REPLACE INTO cities VALUES ('{0}')".format(s)
cursor.execute(query)
print("Gorod dobavlen!")

conn.commit()
=======
import sqlite3

# инициализация 
conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()

s = input("Vvedite gorod: ").encode('utf8','surrogateescape').decode('utf8','surrogateescape')

query = "INSERT or REPLACE INTO cities VALUES ('{0}')".format(s)
cursor.execute(query)
print("Gorod dobavlen!")

conn.commit()
>>>>>>> d208c912f5c0e2e42da463cc7d4d83c9d99f5894
