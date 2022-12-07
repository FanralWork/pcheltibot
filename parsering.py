import requests
import random
from bs4 import BeautifulSoup as b
import json

post_text = []
href_media = []
global title
title = []
global media

def parser_of_jokes(url):
    r = requests.get(url)
    soup = b(r.text,'html.parser')
    anekdots = soup.find_all('div',class_='text')
    return [c.text for c in anekdots]

def parser_of_news(url):
    r=requests.get(url)
    html = b(r.content, 'html.parser')
    content = html.find_all("div", class_="wall_item")
    for con_text in content:
        post_text = con_text.find_all("div", class_="pi_text")
        title.append(post_text[0].text)
    with open("news.json", "w", encoding="utf-8") as write_file:
        json.dump(title, write_file, ensure_ascii=None)
    for img in content:
        #post_img = img.find_all("a", class_="MediaGrid")
        print(img)
        #href_media = (f'https://vk.com{post_img[0]["href"]}')
        #print(href_media)
        #media.append(href_media[0].text)
    '''with open("media.json", "w", encoding="utf-8") as write_file:
        json.dump(media, write_file, ensure_ascii=None)'''
parser_of_news("https://vk.com/rhymes")