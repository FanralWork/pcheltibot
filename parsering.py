import requests
import random
from bs4 import BeautifulSoup as b
import json

def parser_of_jokes(url):
    r = requests.get(url)
    soup = b(r.text,'html.parser')
    anekdots = soup.find_all('div',class_='text')
    return [c.text for c in anekdots]

def parser_of_news(url):
    r=requests.get(url)
    html = b(r.content, 'html.parser')
    content = html.find_all("div", class_="wall_item")
    for material in content:
        post_text= material.find_all("div", class_="pi_text")
    return post_text