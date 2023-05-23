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

for a in range(len(news["response"]["items"][0]["attachments"])):
    if len(caption_photo) > 1000:
        if len(news["response"]["items"][0]["attachments"]) <= 1:
            if news["response"]["items"][0]["attachments"][a]["type"] == "photo":
                await bot.send_photo(chat_id=msg.chat.id,
                                     photo=news["response"]["items"][0]["attachments"][a]["photo"]["sizes"][-1]["url"],
                                     caption=f'{caption_photo[:900]}...\n (Источник: https://vk.com/wall'
                                             f'{news["response"]["items"][0]["from_id"]}_{news["response"]["items"][0]["id"]})',
                                     parse_mode="html")
        if news["response"]["items"][0]["attachments"][a]["type"] == "video":
            video_post_id = news["response"]["items"][0]["attachments"][a]["video"]["id"]
            video_owner_id = news["response"]["items"][0]["attachments"][a]["video"]["owner_id"]
            await bot.send_message(chat_id=msg.chat.id,
                                   text=f'{f"https://vk.com/video{video_owner_id}_{video_post_id}"}'
                                        f' \n {caption_photo[:900]}...\n '
                                        f'(Источник: https://vk.com/wall{news["response"]["items"][0]["from_id"]}_{news["response"]["items"][0]["id"]})',
                                   parse_mode="html")

        if len(news["response"]["items"][0]["attachments"]) > 1:
            if a == 0:
                for b in range(len(news["response"]["items"][0]["attachments"])):
                    if news["response"]["items"][0]["attachments"][b]["type"] == "video":
                        video_post_id = news["response"]["items"][0]["attachments"][b]["video"]["id"]
                        video_owner_id = news["response"]["items"][0]["attachments"][b]["video"]["owner_id"]
                        video_url.append(f'{f"https://vk.com/video{video_owner_id}_{video_post_id}"}'
                                         f' \n {caption_photo[:900]}...\n '
                                         f'(Источник: https://vk.com/wall{news["response"]["items"][0]["from_id"]}_{news["response"]["items"][0]["id"]})')
                    if news["response"]["items"][0]["attachments"][b]["type"] == "photo":
                        y += 1
                for p in range(video_url):
                    txt.join(video_url[p])
                print(txt)
                txt.join(f'{caption_photo[:900]}...\n (Источник: {url.replace("https://", " ")})')
                print(txt)

                if news["response"]["items"][0]["attachments"][a]["type"] == "photo":
                    media.attach_photo(news["response"]["items"][0]["attachments"][a]["photo"]["sizes"][-1]["url"],
                                       txt)
            if a > 0:
                if news["response"]["items"][0]["attachments"][a]["type"] == "photo":
                    media.attach_photo(news["response"]["items"][0]["attachments"][a]["photo"]["sizes"][-1]["url"],
                                       f'{caption_photo}\n (Источник: {url.replace("https://", " ")})')
    else:
        if len(news["response"]["items"][0]["attachments"]) <= 1:
            if news["response"]["items"][0]["attachments"][a]["type"] == "photo":
                await bot.send_photo(chat_id=msg.chat.id,
                                     photo=news["response"]["items"][0]["attachments"][a]["photo"]["sizes"][-1]["url"])
        if news["response"]["items"][0]["attachments"][a]["type"] == "video":
            video_post_id = news["response"]["items"][0]["attachments"][a]["video"]["id"]
            video_owner_id = news["response"]["items"][0]["attachments"][a]["video"]["owner_id"]
            await bot.send_message(chat_id=msg.chat.id,
                                   text=f'{f"https://vk.com/video{video_owner_id}_{video_post_id}"} \n {caption_photo}\n (Источник: https://vk.com/wall{news["response"]["items"][0]["from_id"]}_{news["response"]["items"][0]["id"]})',
                                   parse_mode="html")

        if len(news["response"]["items"][0]["attachments"]) > 1:
            if a == 0:
                for b in range(len(news["response"]["items"][0]["attachments"])):
                    if news["response"]["items"][0]["attachments"][b]["type"] == "video":
                        video_post_id = news["response"]["items"][0]["attachments"][b]["video"]["id"]
                        video_owner_id = news["response"]["items"][0]["attachments"][b]["video"]["owner_id"]
                        video_url.append(f'{f"https://vk.com/video{video_owner_id}_{video_post_id}"}'
                                         f' \n {caption_photo}\n '
                                         f'(Источник: https://vk.com/wall{news["response"]["items"][0]["from_id"]}_{news["response"]["items"][0]["id"]})')
                    if news["response"]["items"][0]["attachments"][b]["type"] == "photo":
                        y += 1
                for p in range(video_url):
                    txt.join(video_url[p])
                print(txt)
                txt.join(f'{caption_photo[:900]}...\n (Источник: {url.replace("https://", " ")})')
                print(txt)

                if news["response"]["items"][0]["attachments"][a]["type"] == "photo":
                    media.attach_photo(
                        news["response"]["items"][0]["attachments"][a]["photo"]["sizes"][-1]["url"],
                        txt)
            if a > 0:
                if news["response"]["items"][0]["attachments"][a]["type"] == "photo":
                    media.attach_photo(
                        news["response"]["items"][0]["attachments"][a]["photo"]["sizes"][-1]["url"],
                        f'{caption_photo}\n (Источник: {url.replace("https://", " ")})')
print(media)
print(txt)
print(video_url)
print(y)
if y > 0:
    await bot.send_media_group(chat_id=msg.chat.id, media=media)
else:
    await bot.send_message(chat_id=msg.chat.id, text=txt)

    if news["response"]["items"][0]["attachments"][a]["type"] == "photo":
        if len(caption_photo) > 1000:
            media.attach_photo(news["response"]["items"][0]["attachments"][a]["photo"]["sizes"][-1]["url"],
                               f'{caption_photo[:900]}...\n (Источник: {url.replace("https://", " ")})')
        else:
            media.attach_photo(news["response"]["items"][0]["attachments"][a]["photo"]["sizes"][-1]["url"],
                               f'{caption_photo}\n (Источник: {url.replace("https://", " ")})',
                               parse_mode="html")
        b = b + 1
        # print(f"Media: {media}")
    if news["response"]["items"][0]["attachments"][a]["type"] == "video":
        video_post_id = news["response"]["items"][0]["attachments"][a]["video"]["id"]
        video_owner_id = news["response"]["items"][0]["attachments"][a]["video"]["owner_id"]
        video_url.append(f"https://vk.com/video{video_owner_id}_{video_post_id}")
if b == 1:
    if len(video_url) > 0:
        c = 0
        await bot.send_message(chat_id=msg.chat.id,
                               text=f'{final_text}\n (Источник: {url.replace("https://", " ")})',
                               disable_web_page_preview=True, reply_markup=BotKeyboards.get_news_keyboard(msg),
                               parse_mode="html")
        for c in range(len(video_url)):
            await bot.send_message(chat_id=msg.chat.id, text=video_url[c])
    else:
        await bot.send_media_group(chat_id=msg.chat.id, media=media)
else:
    if b == 0:
        await bot.send_message(chat_id=msg.chat.id,
                               text=f'{final_text}\n (Источник: {url.replace("https://", " ")})',
                               disable_web_page_preview=True, reply_markup=BotKeyboards.get_news_keyboard(msg),
                               parse_mode="html")
    else:
        await bot.send_message(chat_id=msg.chat.id,
                               text=f'{final_text}\n (Источник: {url.replace("https://", " ")})',
                               disable_web_page_preview=True, reply_markup=BotKeyboards.get_news_keyboard(msg),
                               parse_mode="html")
        await bot.send_media_group(chat_id=msg.chat.id, media=media)
    if len(video_url) > 0:
        c = 0
        for c in range(len(video_url)):
            await bot.send_message(chat_id=msg.chat.id, text=video_url[c])
print(news["response"]["items"][0])