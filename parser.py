import requests
from bs4 import BeautifulSoup as b

URL = 'https://lenta.ru/'
def parser(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    news = soup.find_all('div', class_='last24')
    return [c.text for c in news]
print(parser(URL ))