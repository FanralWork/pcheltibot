# import os
import requests
# from bs4 import BeautifulSoup as be
# import json
#
# for a in (range(2012, 2013)):
#     for b in (range(1, 12)):
#         for d in (range(1, 28)):
#             c = []
#             if len(str(b)) == 1:
#                 if len(str(d)) == 1:
#                     r = requests.get(f"https://www.anekdot.ru/last/good/{a}-0{b}-0{d}/")
#                 else:
#                     r = requests.get(f"https://www.anekdot.ru/last/good/{a}-0{b}-{d}/")
#             else:
#                 r = requests.get(f"https://www.anekdot.ru/last/good/{a}-{b}-{d}/")
#             soup = be(r.text,'html.parser')
#             anekdots = soup.find_all('div',class_='text')
#             #print(type(anekdots))
#             print("anekdots: ", anekdots)
#             with open("good_jokes.json", "a", encoding="utf-8") as file:
#                 json.dump([c.text for c in anekdots], file, ensure_ascii=None)
import cmath
import sqlite3

db = sqlite3.connect('DB.db')

cur = db.cursor()

#Создание таблицы
# cur.execute("""CREATE TABLE users (
#     id INTEGER,
#     user_id INTEGER,
#     full_name TEXT,
#     username TEXT,
#     join_data TEXT
# )""")

# #Добавление данных
# #cur.execute("INSERT INTO users VALUES()")
#
# #Выборка данных
# cur.execute("SELECT * FROM users")
# items = print(cur.fetchall())
#
# for el in items:
#     print()
#
#
#
# db.commit()
#
# db.close()

print(requests.get("https://vk.com/rznnews62"))