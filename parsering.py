import requests
import random
from bs4 import BeautifulSoup as b
import json

post_text = []
post_media = []
post_video = []
post_img = []
href_video = []
href_photo = []
global title
title = []
global media
media = []

def parser_of_jokes(url):
    r = requests.get(url)
    soup = b(r.text,'html.parser')
    anekdots = soup.find_all('div',class_='text')
    return [c.text for c in anekdots]

def parser_of_news(url):
    title = []
    media = []
    r=requests.get(url)
    html = b(r.content, 'html.parser')
    content = html.find_all("div", class_="wall_item")
    for con_text in content:
        post_text = con_text.find_all("div", class_="pi_text")
        title.append(post_text[0].text)
    with open("news.json", "w", encoding="utf-8") as write_file:
        json.dump(title, write_file, ensure_ascii=None)
    for img in content:
        post_video = img.find_all("a",class_="thumb_link")
        post_photo = img.find_all("a", class_="MediaGrid__interactive")
        if len(post_video) > 0:
            href_video = (f'https://vk.com{post_video[0]["href"]}')
            #print(href_video)
            media.append(href_video)
        if len(post_photo) > 0:
            href_photo = (f'https://vk.com{post_photo[0]["href"]}')
            #print(href_photo)
            media.append(href_photo)
    print('Media: ', media)
        #media.append(href_media[0].text)
    with open("media.json", "w", encoding="utf-8") as write_file:
        json.dump(media, write_file, ensure_ascii=None)
#parser_of_news("https://vk.com/rhymes")