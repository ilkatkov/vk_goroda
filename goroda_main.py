# Goroda / Cities (vk version)
# Alt+3 Studio
# Ilya Katkov

# import modules
import vk_api
import random
import os
import json
import datetime
import sqlite3

admin = 142446929 # id админа в ВК

# ---SETTINGS VK---#
token = "api_key"  # api-key
vk = vk_api.VkApi(token=token)
vk._auth_token()
# ---SETTINGS VK---#

def get_button(label, color, payload=''):  # функция вызова клавиатуры
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }

keyboard = {"one_time": False, "buttons": [[get_button(label="Таблица рекордов", color="positive")], [get_button(label="Сбросить города", color="negative"), get_button(label="Правила", color="primary")]]}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

# инициализация db.sqlite
conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()

# собираем список городов
cities = [] # список городов
query = "SELECT * FROM cities"
cursor.execute(query)
l = cursor.fetchall()
for i in l:
    cities.append(i[0])


def computer_answer(id, word):
    try:
        global cursor
        global conn
        global cities
        # ---ОТВЕТ ПК---#
        # выбираем последнюю букву от ответа игрока
        if (word[-1] == "ь") or (word[-1] == "ъ") or (word[-1] == "ы") or (word[-1] == "й"):
            last_letter = word[-2]  # выбрали последней буквой предпоследнюю
        else:
            last_letter = word[-1]  # выбрали последнюю букву

        words_letter = []  # создаем список городов, оканчивающихся на последнюю букву игрока
        for city in cities:  # заносим в список города
            if city[0] == last_letter:
                words_letter.append(city)
                    # выбор города компьютером
        step_query = "SELECT words FROM steps WHERE id = {0}".format(str(id)) # собираем список названных городов
        cursor.execute(step_query)
        result = cursor.fetchall()
        already = []
        for row in result:
            already.append(row[0].lower())

        def rnd_city():
            try:
                rnd = random.randint(0, len(words_letter) - 1)
                computer_word = words_letter[rnd]
                if computer_word in already:
                    rnd_city()  # если город уже использовался в игре, то ищем город дальше
                else:
                    return computer_word
            except Exception as ex:
                vk.method("messages.send", {"peer_id": admin, "message": str(id) + "\n" + rnd + "\n" + computer_word,"keyboard": keyboard, "random_id": random.randint(1, 2147483647)})    
        return rnd_city()  # выбираем рандомный город, как ответ компьютера


    except Exception as ex:
        return vk.method("messages.send", {"peer_id": admin, "message": str(id) + "\n" + ex + "\n" + word + "\n" + last_letter + "\n" + words_letter,"keyboard": keyboard, "random_id": random.randint(1, 2147483647)})


def answer(id, word):
    global cursor
    global conn
    global cities
    vk_info = vk.method("users.get", {"user_ids": int(id)})
    name = vk_info[0].get('first_name')
    surname = vk_info[0].get('last_name')

    info_query = "SELECT EXISTS(SELECT * FROM users WHERE id = {0}".format(str(id))+")"
    cursor.execute(info_query)
    result = cursor.fetchall()

    # игрок не зареган
    if result[0][0] == 0:
        rnd = random.randint(0, len(cities) - 1)
        computer_word = cities[rnd]

        # выбираем последнюю букву ответа компьютера
        if (computer_word[-1] == "ь") or (computer_word[-1] == "ъ") or (computer_word[-1] == "ы") or (computer_word[-1] == "й"):
            last_letter = computer_word[-2]
        else:
            last_letter = computer_word[-1]
        step_query = "INSERT INTO users VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(str(id), name, surname, "0", last_letter, "")
        cursor.execute(step_query)
        result = cursor.fetchall()
        step_query = "INSERT INTO steps VALUES ('{0}', '{1}')".format(str(id), computer_word.title())
        cursor.execute(step_query) # вносим новую инфу в steps

        conn.commit() 

        # говорим игроку о ходе компьютера
        vk.method("messages.send", {"peer_id": id,
                                    "message": 'Город компьютера:\n{0}\n\nТебе на {1}!'.format(computer_word.title(), last_letter.upper()),
                                    "keyboard": keyboard,"random_id": random.randint(1, 2147483647)})
        
        
    # игрок зареган и ходит
    else:
        step_query = "SELECT words FROM steps WHERE id = {0}".format(str(id)) # собираем список названных городов
        cursor.execute(step_query)
        result = cursor.fetchall()
        already = []
        for row in result:
            already.append(row[0].lower())
        
        step_query = "SELECT * FROM cities" # собираем список городов
        cursor.execute(step_query)
        result = cursor.fetchall()
        cities = []
        for row in result:
            cities.append(row[0].lower()) 

        step_query = "SELECT last_letter FROM users WHERE id = {0}".format(str(id)) # смотрим последнюю букву
        cursor.execute(step_query)
        result = cursor.fetchall()
        last_letter = result[0][0]

        if word.lower() in already:
            return vk.method("messages.send", {"peer_id": id, "message": "Город " + word.title() + " уже был назван!","keyboard": keyboard, "random_id": random.randint(1, 2147483647)})
        if (word.lower() in cities) and (word[0].lower() != last_letter):
            return vk.method("messages.send", {"peer_id": id, "message": "Город " + word.title() + " не подходит!","keyboard": keyboard, "random_id": random.randint(1, 2147483647)})
        if word[0].lower() != last_letter:
            return vk.method("messages.send", {"peer_id": id, "message": "Тебе на " + last_letter.upper() + "!","keyboard": keyboard, "random_id": random.randint(1, 2147483647)})
        if word.lower() not in cities:
            return vk.method("messages.send", {"peer_id": id, "message": "Я не знаю такого города, либо его не существует!","keyboard": keyboard, "random_id": random.randint(1, 2147483647)})
            
        step_query = "SELECT points FROM users WHERE id = {0}".format(str(id)) # узнаем сколько было баллов
        cursor.execute(step_query)
        result = cursor.fetchall()
        points = int(result[0][0])

        step_query = "INSERT INTO steps VALUES ('{0}', '{1}')".format(str(id), word.title())
        cursor.execute(step_query) # вносим новую инфу в steps

        computer_word = computer_answer(id, word)
        # выбираем последнюю букву ответа компьютера
        if (computer_word[-1] == "ь") or (computer_word[-1] == "ъ") or (computer_word[-1] == "ы") or (computer_word[-1] == "й"):
            last_letter = computer_word[-2]
        else:
            last_letter = computer_word[-1]
        step_query = "UPDATE users SET points = '{0}', last_letter = '{1}', last_word = '{2}' WHERE id = '{3}'".format(str(points+1), last_letter, word, str(id))
        cursor.execute(step_query) # вносим новую инфу в users
        result = cursor.fetchall()
        step_query = "INSERT INTO steps VALUES ('{0}', '{1}')".format(str(id), computer_word.title())
        cursor.execute(step_query) # вносим новую инфу в steps
        conn.commit() 
        # говорим игроку о ходе компьютера
        vk.method("messages.send", {"peer_id": id,
                                    "message": 'Город компьютера:\n{0}\n\nТебе на {1}!'.format(computer_word.title(), last_letter.upper()),"keyboard": keyboard, 
                                    "random_id": random.randint(1, 2147483647)}) 
def restart(id):
        step_query = "DELETE FROM steps WHERE id = {0}".format(str(id))
        cursor.execute(step_query)
        conn.commit() 
        return vk.method("messages.send", {"peer_id": id, "message": "Города сброшены!","keyboard": keyboard, "random_id": random.randint(1, 2147483647)})

def records(id):
    try:
        step_query = "SELECT name, surname, points FROM users ORDER BY points DESC"
        cursor.execute(step_query)
        result = cursor.fetchall()
        user_query = "SELECT name, surname, points FROM users WHERE id = {0}".format(str(id))
        cursor.execute(user_query)
        result_user = cursor.fetchall()[0]        
        info = "Таблица рекордов:\n\n1. {0} {1} - {2}\n2. {3} {4} - {5}\n3. {6} {7} - {8}\n4. {9} {10} - {11}\n5. {12} {13} - {14}\n\nВы на {15} месте.\nВаш счёт: {16}".format(
            result[0][0], result[0][1], result[0][2], result[1][0], result[1][1], result[1][2], result[2][0], result[2][1], result[2][2], result[3][0], result[3][1], result[3][2],
            result[4][0], result[4][1], result[4][2], str(int(result.index(result_user))+1), result_user[2]
        )
        return vk.method("messages.send", {"peer_id": id, "message": info,"keyboard": keyboard, "random_id": random.randint(1, 2147483647)})
    except Exception as ex:
        vk.method("messages.send", {"peer_id": admin, "message": str(ex),"keyboard": keyboard,  "random_id": random.randint(1, 2147483647)})
# ---ОСНОВНОЙ ЦИКЛ ИГРЫ---#
while True:
    try:	
        while True:
            try:
                messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
                if messages["count"] >= 1:
                    id = messages["items"][0]["last_message"]["from_id"]
                    user_word = messages["items"][0]["last_message"]["text"]
                    if user_word == "Сбросить города":
                        restart(id)
                    elif user_word == "Таблица рекордов":
                        records(id)
                    elif user_word == "Правила":
                        info = "Бот Города - игра, где каждый игрок называет реально\nсуществующий город любой страны, название которого\nначинается на ту букву, которой оканчивается название\nгорода чат-бота.\n\nУдачи!"
                        vk.method("messages.send", {"peer_id": id, "message": info,"keyboard": keyboard, "random_id": random.randint(1, 2147483647)})
                    else:
                        answer(id, user_word)
            except IndexError:
                vk.method("messages.send", {"peer_id": id, "message": "Я не знаю такого города, либо его не существует!","keyboard": keyboard, "random_id": random.randint(1, 2147483647)})
            except Exception as ex:
                vk.method("messages.send", {"peer_id": admin, "message": str(ex),"keyboard": keyboard,  "random_id": random.randint(1, 2147483647)})
    except Exception as ex:
        continue
# ---ОСНОВНОЙ ЦИКЛ ИГРЫ---#
