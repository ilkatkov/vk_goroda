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

