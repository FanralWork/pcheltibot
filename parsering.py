import os
import requests
import random
from bs4 import BeautifulSoup as b
import json
import config
import shutil
import asyncio

token_vk = config.Token_vk

def parser_vk(group_name):
    url = f"https://api.vk.com/method/wall.get?domain={group_name}&count=100&access_token={token_vk}&v=5.131"
    req = requests.get(url)
    src = req.json()

    if os.path.exists(f"groups/{group_name}"):
        None
    else:
        os.mkdir(f"groups/{group_name}")

    with open (f"groups/{group_name}/{group_name}.json", "w", encoding="utf-8") as file:
        json.dump(src, file, ensure_ascii=False)
# parser_vk("kvantorium62")

def add_new_id_of_news(group_name, post_id):
    with open (f"id/{group_name}_id.txt", "a", encoding="utf-8") as file:
        file.write(f'\n{post_id},')
        file.close()