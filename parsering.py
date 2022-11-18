import requests
import random
from bs4 import BeautifulSoup as b
import json

URL = 'https://www.anekdot.ru/random/anekdot/'

def parser_of_jokes(url):
    r = requests.get(url)
    soup = b(r.text,'html.parser')
    anekdots = soup.find_all('div',class_='text')
    return [c.text for c in anekdots]

list_of_jokes_ed = parser_of_jokes(URL)
list_of_jokes=random.shuffle(list_of_jokes_ed)


  #random.shuffle(f)
'''
x = parser_of_jokes(URL)

with open('jokes.json', 'r+') as f:
    f.write(json.dumps(x, ensure_ascii = False))'''
#for i in range(len(x)):
#    print(x[i])
#    with open('jokes.json', 'r+') as f:
#        json.dumps([{i:x[i]}], separators=(',', ':'))
#print(x)