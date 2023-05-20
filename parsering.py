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
# parser_vk("fanral")

async def delete_groups(delay_time):
    while True:
        await asyncio.sleep(delay_time)
        folder = f'{os.getcwd()}/groups/'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
