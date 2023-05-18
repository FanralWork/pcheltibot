import os
import requests
import random
from bs4 import BeautifulSoup as b
import json
import config

token_vk = config.Token_vk
post_text = []
post_media = []
post_video = []
post_img = []
href_video = []
href_photo = []
title = ""
global text
text = {}
global media
media = {}
global content
content = {"common":{},"kvantorium":{}}
src = []
req = []

def parser_of_jokes(url):
    c = []
    r = requests.get(url)
    soup = b(r.text,'html.parser')
    anekdots = soup.find_all('div',class_='text')
    #print(type(anekdots))
    #print("anekdots: ", anekdots)
    with open("jokes.json", "w", encoding="utf-8") as file:
        json.dump([c.text for c in anekdots], file, ensure_ascii=None)
    #return [c.text for c in anekdots]
#parser_of_jokes('https://www.anekdot.ru/random/anekdot/')

def parser_of_news(url):
    #print(url)
    text = {}
    media = {}
    r=requests.get(url)
    html = b(r.content, 'html.parser')
    content_n = html.find_all("div", class_="wall_item")
    i = 0
    for con_text in content_n:
        title = ""
        post_text = con_text.find_all("div", class_="pi_text")
        title = post_text[0].text
        #print(title)
        #print(i)
        text[i] = title
        i = i + 1
    #with open("news.json", "w", encoding="utf-8") as write_file:
        #json.dump(title, write_file, ensure_ascii=None)
    i = 0
    for img in content_n:
        href_photo = []
        href_video = []
        post_video = img.find_all("a",class_="thumb_link")
        post_photo = img.find_all("a", class_="MediaGrid__interactive")
        if len(post_video) > 0:
            c=0
            while c < len(post_video):
                href_video.append(f'https://vk.com{post_video[c]["href"]}')
                media[i] = href_video
                c+=1
        #print(href_video)
        if len(post_photo) > 0:
            c = 0
            while c < len(post_photo):
                href_photo.append(f'https://vk.com{post_photo[c]["href"]}')
                media[i] = href_photo
                c += 1
        i = i + 1
        #print(href_photo)
    #print('Media: ', media, '\nText: ',  text)
        #media.append(href_media[0].text)
    #with open("media.json", "w", encoding="utf-8") as write_file:
        #json.dump(media, write_file, ensure_ascii=None)
    #if url == "ttps://vk.com/rhymes":
    i =0
    a = {}
    while i < 5:
        a[i] = text[i],media[i]
        i +=1
    #print("a: ", a)
    if url == "https://vk.com/rhymes":
        news = {}
        with open("news.json", "r", encoding="utf-8") as read_file:
            news = json.load(read_file)
        print(news)
        content["common"] = a
        content["kvantorium"] = news["kvantorium"]
        print("Content: ",content)
    with open("news.json", "w", encoding="utf-8") as file:
        json.dump(content, file, ensure_ascii=None)
    if url == "https://vk.com/kvantorium62":
        news = {}
        with open("news.json", "r", encoding="utf-8") as read_file:
            news = json.load(read_file)
        print(news)
        content["common"] = news["common"]
        content["kvantorium"] = a
        print("Content: ",content)
    with open("news.json", "w", encoding="utf-8") as file:
        json.dump(content, file, ensure_ascii=None)
#parser_of_news("https://vk.com/kvantorium62")

def parser_vk(group_name):
    url = f"https://api.vk.com/method/wall.get?domain={group_name}&count=100&access_token={token_vk}&v=5.131"
    req = requests.get(url)
    src = req.json()

    if os.path.exists(f"{group_name}"):
        None
    else:
        os.mkdir(group_name)

    with open (f"{group_name}/{group_name}.json", "w", encoding="utf-8") as file:
        json.dump(src, file, ensure_ascii=False)

#parser_vk("kvantorium62")

    # fresh_posts_id = []
    # post = src["response"]["items"]
    #
    # for fresh_posts_id in post:
    #     fresh_posts_id = fresh_posts_id["id"]
    #     fresh_posts_id.append(fresh_posts_id)
    #
    # if not os.path.exists(f"{group_name}/exist_post_{group_name}.txt"):
    #     print("Файла с ID постов не существует, создаём файл!")
    #     with open(f"{group_name}/exist_post_{group_name}.txt", "w") as file:
    #         for item in fresh_posts_id:
    #             file.write(str(item) + "\n")
    # else:
    #     print("Файл с ID постов найден, начинаем выборку свежих постов!")
# def parser_vk_video(video_access_key, video_post_id, video_owner_id):
#     #video_get_url = f"https://api.vk.com/method/video.get?videos={video_owner_id}_{video_post_id}_{video_access_key}&access_token={token_vk}&v=5.131"
#     video_get_url = f"https://api.vk.com/method/video.get?videos={video_owner_id}_{video_post_id}_{video_access_key}&access_token={token_vk}&v=5.131"
#     req = requests.get(video_get_url)
#     res = req.json()
#     #print(res)
#     video_url = res["response"]["items"][0]["player"]
#     print(video_url)
#     return video_url

#parser_vk_video("9197df9387f52d49d3", "456360218", "-28905875")'''