<<<<<<< HEAD
import vk_api
import sqlite3
import random

# ---НАСТРОЙКИ VK---#
token = "api-key"  # api-ключ "Города"
vk = vk_api.VkApi(token=token)
vk._auth_token()
# ---НАСТРОЙКИ VK---#

# инициализация db.sqlite
conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()

query_sms = """SELECT id FROM users"""
cursor.execute(query_sms)
result = cursor.fetchall()

info = []
for row in range(0, len(result)):
    info.append(result[row][0])

def call_1():
    message = input("Vvdeite soobschenie:\n").encode('utf8','surrogateescape').decode('utf8','surrogateescape')
    for i in info:
        try:
            vk.method("messages.send", {"peer_id": i, "message": message, "random_id": random.randint(1, 2147483647)})
        except Exception:
            pass    
    conn.commit()
    print(len(info), "messages: OK")
    
call_1()
=======
import vk_api
import sqlite3
import random

# ---НАСТРОЙКИ VK---#
token = "141f17d2389cfabf7da8b4ba2424090167b47708f6ae1d915a3c5b217c11d37bc2eeffa9839146322e5a2"  # api-ключ "Города"
vk = vk_api.VkApi(token=token)
vk._auth_token()
# ---НАСТРОЙКИ VK---#

# инициализация db.sqlite
conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()

query_sms = """SELECT id FROM users"""
cursor.execute(query_sms)
result = cursor.fetchall()

info = []
for row in range(0, len(result)):
    info.append(result[row][0])

def call_1():
    for i in info:
        try:
            vk.method("messages.send", {"peer_id": i, "message": "Привет! А помнишь мы с тобой в Города играли... И я помню, так что давай продолжим!", "random_id": random.randint(1, 2147483647)})
        except Exception:
            pass    
    conn.commit()
    
call_1()
>>>>>>> d208c912f5c0e2e42da463cc7d4d83c9d99f5894
