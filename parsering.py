import requests
import random
from bs4 import BeautifulSoup as b
import json

post_text = []
href_media = []

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
        print(post_text)
        with open("news.json", "a",  encoding="utf-8") as write_file:
            json.dump(post_text[0].text, write_file, ensure_ascii=None)
    for img in content:
        post_img = img.find_all("a", class_="thumb_link")
        href_media = (f'https://vk.com/{post_img[0]["href"]}')
    return post_text
parser_of_news("https://vk.com/rhymes")