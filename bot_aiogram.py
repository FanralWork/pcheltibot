import string
from aiogram import Bot, executor, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
import config
import parsering
import json
import os
import random
import sqlite3
import datetime
import requests
from db import BotDB
from keyboards import BotKeyboards
import asyncio
import shutil

# URL_jokes = 'https://www.anekdot.ru/random/anekdot/'
# URL_jokes = 'https://www.anekdot.ru/'
# URL_facts = 'https://randstuff.ru/fact'
# URL_rhymes = 'rhymes'
URL_kvantorium62 = 'kvantorium62'

token = config.TOKEN
# token = config.SPARE_TOKEN
# token_vk = config.Token_vk
chat_id = config.CHAT_ID
storage = MemoryStorage()
bot = Bot(token)
dp = Dispatcher(bot=bot, storage=storage)


class ProfileStatesGroup(StatesGroup):
    group_name1 = State()
    group_name2 = State()
    group_name3 = State()


BotDB = BotDB("DB.db")
BotKeyboards = BotKeyboards("DB.db")


async def on_startup(_):
    print("Bot is active!")


async def new_user(msg):
    if BotDB.user_exists(msg.from_user.id) == False:
        BotDB.add_user(msg)
        print("Новый пользователь")


@dp.message_handler(commands=["start"])
async def send_message(msg: types.Message):
    bot_name = await bot.get_me()
    await msg.answer(
        f"Приветствую, {msg.from_user.full_name}!\nЯ - <b>{bot_name.first_name}</b>, развлекательно-новостной бот.",
        parse_mode="html", reply_markup=BotKeyboards.get_news_keyboard(msg))
    await bot.send_sticker(msg.from_user.id,
                           sticker="CAACAgIAAxkBAAEHfLhj1TfnDTXgju-hIIhQ7ssUdAZAdAACwRIAAvXQth0OkELw6I25My0E")
    await msg.delete()
    await new_user(msg)


@dp.message_handler()
async def send_news(msg: types.Message):
    await new_user(msg)

    async def send_content(url):
        try:
            news = []
            if not (os.path.exists(f"groups/{url}/{url}.json")):
                parsering.parser_vk(url)
            with open(f"groups/{url}/{url}.json", "r", encoding="utf-8") as read_file:
                news = json.load(read_file)
            if len(news["response"]["items"]) == 0:
                parsering.parser_vk(url)
                with open(f"groups/{url}/{url}.json", "r", encoding="utf-8") as read_file:
                    news = json.load(read_file)
            with open('BEST_MAT_EVER.txt', 'r', encoding='Windows-1251') as f_ck:
                f_ck_list = set([a.rstrip().casefold() for a in f_ck])
            news_split = []
            news_censured = []
            for i in news["response"]["items"][0]["text"].split(' '):
                news_split.append(i)
            if "copy_history" in news["response"]["items"][0]:
                news_split.append("\n")
                for i in news["response"]["items"][0]["copy_history"][0]["text"].split(' '):
                    news_split.append(i)
            for b in range(0, len(news_split)):
                if news_split[b].translate(str.maketrans('', '', string.punctuation)).casefold() in f_ck_list:
                    news_split[
                        b] = f'<tg-spoiler>{news_split[b][0]}{(len(news_split[b]) - 2) * "*"}{news_split[b][len(news_split[b]) - 1]}</tg-spoiler>'
                news_censured.append(news_split[b])
            final_text = ' '.join(news_censured)
            media = types.MediaGroup()
            video_url = []
            global y
            y = 0
            global media_len
            media_len = 0
            global txt
            txt = ""
            global caption_photo
            caption_photo = final_text[:850]
            print("\n", final_text)

            for a in range(len(news["response"]["items"][0]["attachments"])):
                if news["response"]["items"][0]["attachments"][a]["type"] == "video":
                    txt = txt + '\n' + f'https://vk.com/video{news["response"]["items"][0]["attachments"][a]["video"]["owner_id"]}_{news["response"]["items"][0]["attachments"][a]["video"]["id"]}'
                if news["response"]["items"][0]["attachments"][a]["type"] == "photo":
                    y += 1

            if len(news["response"]["items"][0]["attachments"]) == 0:
                if "copy_history" in news["response"]["items"][0]:
                    for q in range(len(news["response"]["items"][0]["copy_history"][0]["attachments"])):
                        if news["response"]["items"][0]["copy_history"][0]["attachments"][q]["type"] == "video":
                            txt = txt + '\n' + f'https://vk.com/video{news["response"]["items"][0]["copy_history"][0]["attachments"][q]["video"]["owner_id"]}_{news["response"]["items"][0]["copy_history"][0]["attachments"][q]["video"]["id"]}'
                        if news["response"]["items"][0]["copy_history"][0]["attachments"][q]["type"] == "photo":
                            y += 1

                    if len(news["response"]["items"][0]["copy_history"][0]["attachments"]) == 0:
                        await bot.send_message(chat_id=msg.chat.id, text=f'{final_text}\n'
                                                                         f'(Источник: https://vk.com/wall{news["response"]["items"][0]["from_id"]}_{news["response"]["items"][0]["id"]})')

                    for q in range(len(news["response"]["items"][0]["copy_history"][0]["attachments"])):
                        if len(news["response"]["items"][0]["copy_history"][0]["attachments"]) == 1:
                            if news["response"]["items"][0]["copy_history"][0]["attachments"][q]["type"] == "photo":
                                await bot.send_photo(chat_id=msg.chat.id,
                                                     photo=
                                                     news["response"]["items"][0]["copy_history"][0]["attachments"][q][
                                                         "photo"]["sizes"][
                                                         -1]["url"],
                                                     caption=f'{caption_photo}\n'
                                                             f'(Источник: https://vk.com/wall{news["response"]["items"][0]["from_id"]}_{news["response"]["items"][0]["id"]})')
                            if news["response"]["items"][0]["copy_history"][0]["attachments"][q]["type"] == "video":
                                video_post_id = news["response"]["items"][0]["copy_history"][0]["attachments"][q]["video"][
                                    "id"]
                                video_owner_id = news["response"]["items"][0]["copy_history"][0]["attachments"][q]["video"][
                                    "owner_id"]
                                await bot.send_message(chat_id=msg.chat.id,
                                                       text=f'https://vk.com/video{video_owner_id}_{video_post_id}'
                                                            f'\n{caption_photo}\n'
                                                            f'(Источник: https://vk.com/wall{news["response"]["items"][0]["from_id"]}_{news["response"]["items"][0]["id"]})')
                            if news["response"]["items"][0]["copy_history"][0]["attachments"][q]["type"] != "video" and \
                                    news["response"]["items"][0]["copy_history"][0]["attachments"][q]["type"] != "photo":
                                await bot.send_message(chat_id=msg.chat.id, text=f'\n{caption_photo}\n'
                                                                                 f'(Источник: https://vk.com/wall{news["response"]["items"][0]["from_id"]}_{news["response"]["items"][0]["id"]})')

                        if len(news["response"]["items"][0]["copy_history"][0]["attachments"]) > 1:
                            # print(y)
                            if y == 0:
                                await bot.send_message(chat_id=msg.chat.id,
                                                       text=f'{txt}'
                                                            f'{caption_photo}\n'
                                                            f'(Источник: https://vk.com/wall{news["response"]["items"][0]["from_id"]}_{news["response"]["items"][0]["id"]})')
                            if y == 1:
                                if news["response"]["items"][0]["copy_history"][0]["attachments"][q]["type"] == "photo":
                                    media.attach_photo(
                                        news["response"]["items"][0]["copy_history"][0]["attachments"][q]["photo"]["sizes"][-1]["url"],
                                        f'{txt} \n {caption_photo}\n ((Источник: https://vk.com/wall{news["response"]["items"][0]["from_id"]}_{news["response"]["items"][0]["id"]})')
                                    media_len = media_len + 1
                            if y > 1:
                                # print(media_len)
                                if media_len == 0:
                                    if news["response"]["items"][0]["copy_history"][0]["attachments"][q]["type"] == "photo":
                                        # print(media_len)
                                        # print(txt + "\n" + caption_photo)
                                        media.attach_photo(
                                            news["response"]["items"][0]["copy_history"][0]["attachments"][q]["photo"]["sizes"][-1]["url"],
                                            f'{txt} \n {caption_photo}\n (Источник: https://vk.com/wall{news["response"]["items"][0]["from_id"]}_{news["response"]["items"][0]["id"]})')
                                        media_len = media_len + 1
                                if media_len > 0 and media_len < 10:
                                    print(media_len)
                                    if news["response"]["items"][0]["copy_history"][0]["attachments"][q]["type"] == "photo":
                                        media.attach_photo(
                                            news["response"]["items"][0]["copy_history"][0]["attachments"][q]["photo"]["sizes"][-1]["url"])
                                        media_len = media_len + 1
                else:
                    await bot.send_message(chat_id=msg.chat.id, text=f'{final_text}\n'
                                                                     f'(Источник: https://vk.com/wall{news["response"]["items"][0]["from_id"]}_{news["response"]["items"][0]["id"]})')

            for a in range(len(news["response"]["items"][0]["attachments"])):
                if len(news["response"]["items"][0]["attachments"]) == 1:
                    if news["response"]["items"][0]["attachments"][a]["type"] == "photo":
                        await bot.send_photo(chat_id=msg.chat.id,
                                             photo=news["response"]["items"][0]["attachments"][a]["photo"]["sizes"][-1][
                                                 "url"],
                                             caption=f'{caption_photo}\n'
                                                     f'(Источник: https://vk.com/wall{news["response"]["items"][0]["from_id"]}_{news["response"]["items"][0]["id"]})')
                    if news["response"]["items"][0]["attachments"][a]["type"] == "video":
                        video_post_id = news["response"]["items"][0]["attachments"][a]["video"]["id"]
                        video_owner_id = news["response"]["items"][0]["attachments"][a]["video"]["owner_id"]
                        await bot.send_message(chat_id=msg.chat.id,
                                               text=f'https://vk.com/video{video_owner_id}_{video_post_id}'
                                                    f'\n{caption_photo}\n'
                                                    f'(Источник: https://vk.com/wall{news["response"]["items"][0]["from_id"]}_{news["response"]["items"][0]["id"]})')
                    if news["response"]["items"][0]["attachments"][a]["type"] != "video" and \
                            news["response"]["items"][0]["attachments"][a]["type"] != "photo":
                        await bot.send_message(chat_id=msg.chat.id, text=f'\n{caption_photo}\n'
                                                                         f'(Источник: https://vk.com/wall{news["response"]["items"][0]["from_id"]}_{news["response"]["items"][0]["id"]})')

                if len(news["response"]["items"][0]["attachments"]) > 1:
                    # print(y)
                    if y == 0:
                        await bot.send_message(chat_id=msg.chat.id,
                                               text=f'{txt}'
                                                    f'{caption_photo}\n'
                                                    f'(Источник: https://vk.com/wall{news["response"]["items"][0]["from_id"]}_{news["response"]["items"][0]["id"]})')
                    if y == 1:
                        if news["response"]["items"][0]["attachments"][a]["type"] == "photo":
                            media.attach_photo(
                                news["response"]["items"][0]["attachments"][a]["photo"]["sizes"][-1]["url"],
                                f'{txt} \n {caption_photo}\n ((Источник: https://vk.com/wall{news["response"]["items"][0]["from_id"]}_{news["response"]["items"][0]["id"]})')
                            media_len = media_len + 1
                    if y > 1:
                        # print(media_len)
                        if media_len == 0:
                            if news["response"]["items"][0]["attachments"][a]["type"] == "photo":
                                # print(media_len)
                                # print(txt + "\n" + caption_photo)
                                media.attach_photo(
                                    news["response"]["items"][0]["attachments"][a]["photo"]["sizes"][-1]["url"],
                                    f'{txt} \n {caption_photo}\n (Источник: https://vk.com/wall{news["response"]["items"][0]["from_id"]}_{news["response"]["items"][0]["id"]})')
                                media_len = media_len + 1
                        if media_len > 0 and media_len < 10:
                            print(media_len)
                            if news["response"]["items"][0]["attachments"][a]["type"] == "photo":
                                media.attach_photo(
                                    news["response"]["items"][0]["attachments"][a]["photo"]["sizes"][-1]["url"])
                                media_len = media_len + 1

            # print("len(news):", len(news["response"]["items"][0]["attachments"]))
            # print("y:", y)
            # print("media:", media)
            # print("media_len:", media_len)
            if media_len > 0:
                await bot.send_media_group(chat_id=msg.chat.id, media=media)

            del news["response"]["items"][0]
            with open(f"groups/{url}/{url}.json", "w", encoding="utf-8") as file:
                json.dump(news, file, ensure_ascii=None)

        except Exception as e:
            #print('User: ', msg.from_user.id, f'\nError: ', repr(e))
            await bot.send_message(msg.chat.id, f'Произошла ошибка. Попробуйте ещё раз...\nError: {repr(e)}',
                                   reply_markup=BotKeyboards.get_news_keyboard(msg))
            # await bot.send_sticker(msg.from_user.id, sticker="CAACAgIAAxkBAAEIF29kDIAYLLLdvNARmO2dnMzNCZzzNAACkiMAAmv4yEiZGesZWjzE7S8E")
            del news["response"]["items"][0]
            with open(f"groups/{url}/{url}.json", "w", encoding="utf-8") as file:
                json.dump(news, file, ensure_ascii=None)

    async def group_setting(msg: types.Message):
        await bot.send_message(msg.chat.id, f'Настройка групп. Выберите настраиваемую ячейку, которую хотите изменить',
                               reply_markup=BotKeyboards.get_settings_inline_keyboard(msg))

    groups = []
    user_groups = BotDB.check_user_group(msg)
    group1 = user_groups[5]
    group2 = user_groups[6]
    group3 = user_groups[7]
    groups.append(group1)
    groups.append(group2)
    groups.append(group3)

    groups_names = []
    for i in groups:
        if not (i == None):
            groups_names.append(i.replace("https://vk.com/", ""))
    # print(groups_names)

    url = str
    if msg.text == "Новости Кванториума":
        await send_content(URL_kvantorium62)
    if not (group1) == None:
        if msg.text == group1.replace("https://vk.com/", ""):
            await send_content(group1.replace("https://vk.com/", ""))
    if not (group2) == None:
        if msg.text == group2.replace("https://vk.com/", ""):
            await send_content(group2.replace("https://vk.com/", ""))
    if not (group3) == None:
        if msg.text == group3.replace("https://vk.com/", ""):
            await send_content(group3.replace("https://vk.com/", ""))
    if msg.text == "Новости" or msg.text == "Назад":
        func_txt = "Новости из: \n - Кванториума,"
        if len(groups_names) >= 1:
            func_txt = func_txt + "\n - " + groups_names[0] + ","
        if len(groups_names) >= 2:
            func_txt = func_txt + "\n - " + groups_names[1] + ","
        if len(groups_names) == 3:
            func_txt = func_txt + "\n - " + groups_names[2] + ","
        await bot.send_message(chat_id=msg.chat.id,
                               text=func_txt,
                               disable_web_page_preview=True, reply_markup=BotKeyboards.get_news_keyboard(msg),
                               parse_mode="html")

    if msg.text == "Добавить группу" or msg.text == "Настроить группы":
        await group_setting(msg)


@dp.message_handler(state=ProfileStatesGroup.group_name1)
async def add_group(msg: types.Message, state: FSMContext):
    vk = 'https://vk.com/'
    user_groups = BotDB.check_user_group(msg)
    group1 = user_groups[5]
    group2 = user_groups[6]
    group3 = user_groups[7]
    if msg.text == 'Назад':
        await state.finish()
        await send_news(msg)
    else:
        try:
            if vk in msg.text and (requests.get(msg.text).status_code == 200) and (msg.text != group1) and (
                    msg.text != group2) and (msg.text != group3):
                BotDB.update_user_group("user_group1", msg)
                user_groups = BotDB.check_user_group(msg)
                group1 = user_groups[5]
                group2 = user_groups[6]
                group3 = user_groups[7]
                await msg.answer('Группа сохранена!', reply_markup=BotKeyboards.get_news_keyboard(msg),
                                 parse_mode="html")
                await state.finish()
            else:
                await msg.answer("Неверный URl. Поробуйте ещё раз", reply_markup=BotKeyboards.get_cancel_keyboard(),
                                 parse_mode="html")
        except Exception as e:
            print('User: ', msg.from_user.id, f'\nError: ', repr(e))
            await bot.send_message(msg.chat.id, f'Произошла ошибка. Попробуйте ещё раз...\nError: {repr(e)}',
                                   reply_markup=BotKeyboards.get_news_keyboard(msg), parse_mode="html")


@dp.message_handler(state=ProfileStatesGroup.group_name2)
async def add_group(msg: types.Message, state: FSMContext):
    vk = 'https://vk.com/'
    user_groups = BotDB.check_user_group(msg)
    group1 = user_groups[5]
    group2 = user_groups[6]
    group3 = user_groups[7]
    if msg.text == 'Назад':
        await state.finish()
        await send_news(msg)
    else:
        try:
            if vk in msg.text and (requests.get(msg.text).status_code == 200) and (msg.text != group1) and (
                    msg.text != group2) and (msg.text != group3):
                BotDB.update_user_group("user_group2", msg)
                user_groups = BotDB.check_user_group(msg)
                group1 = user_groups[5]
                group2 = user_groups[6]
                group3 = user_groups[7]
                await msg.answer('Группа сохранена!', reply_markup=BotKeyboards.get_news_keyboard(msg),
                                 parse_mode="html")
                await state.finish()
            else:
                await msg.answer("Неверный URl. Поробуйте ещё раз", reply_markup=BotKeyboards.get_cancel_keyboard(),
                                 parse_mode="html")
        except Exception as e:
            # print('User: ', msg.from_user.id, f'\nError: ', repr(e))
            await bot.send_message(msg.chat.id, f'Произошла ошибка. Попробуйте ещё раз...\nError: {repr(e)}',
                                   reply_markup=BotKeyboards.get_news_keyboard(msg), parse_mode="html")


@dp.message_handler(state=ProfileStatesGroup.group_name3)
async def add_group(msg: types.Message, state: FSMContext):
    vk = 'https://vk.com/'
    user_groups = BotDB.check_user_group(msg)
    group1 = user_groups[5]
    group2 = user_groups[6]
    group3 = user_groups[7]
    if msg.text == 'Назад':
        await state.finish()
        await send_news(msg)
    else:
        try:
            if vk in msg.text and (requests.get(msg.text).status_code == 200) and (msg.text != group1) and (
                    msg.text != group2) and (msg.text != group3):
                BotDB.update_user_group("user_group3", msg)
                user_groups = BotDB.check_user_group(msg)
                group1 = user_groups[5]
                group2 = user_groups[6]
                group3 = user_groups[7]
                await msg.answer('Группа сохранена!', reply_markup=BotKeyboards.get_news_keyboard(msg),
                                 parse_mode="html")
                await state.finish()
            else:
                await msg.answer("Неверный URl. Поробуйте ещё раз", reply_markup=BotKeyboards.get_cancel_keyboard(),
                                 parse_mode="html")
        except Exception as e:
            # print('User: ', msg.from_user.id, f'\nError: ', repr(e))
            await bot.send_message(msg.chat.id, f'Произошла ошибка. Попробуйте ещё раз...\nError: {repr(e)}',
                                   reply_markup=BotKeyboards.get_news_keyboard(msg), parse_mode="html")


@dp.callback_query_handler()
async def message_callback(callback: types.CallbackQuery):
    # print("Callback data")
    # if callback.data == 'common':
    #     send_news('Общие')
    #     #await callback.answer('Ладно')
    # if callback.data == 'kvantorium62':
    #     send_news('Кванториума')
    if callback.data == 'user_group1':
        await callback.message.answer(
            "Отправьте ссылку на группу (в формате \"https://vk.com/***\"), которую хотите парсить. ")
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        await ProfileStatesGroup.group_name1.set()
    if callback.data == 'user_group2':
        await callback.message.answer(
            "Отправьте ссылку на группу (в формате \"https://vk.com/***\"), которую хотите парсить. ")
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        await ProfileStatesGroup.group_name2.set()
    if callback.data == 'user_group3':
        await callback.message.answer(
            "Отправьте ссылку на группу (в формате \"https://vk.com/***\"), которую хотите парсить. ")
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        await ProfileStatesGroup.group_name3.set()

async def check_publishing(delay_time):
    while True:
        url = "kvantorium62"
        news = []

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

        parsering.parser_vk(url)
        with open(f"groups/{url}/{url}.json", "r", encoding="utf-8") as read_file:
            news = json.load(read_file)
        # print(news)
        if not(os.path.exists(f"id/{url}_id.txt")):
            os.mkdir(f"id")
        with open(f"id/{url}_id.txt", "r", encoding="utf-8") as file:
            ids = file.read()
            file.close()
        # print(ids)

        for i in range(len(news["response"]["items"])):
            # print(str(news["response"]["items"][i]["id"]) in ids)
            if not(str(news["response"]["items"][i]["id"]) in ids):
                print(news["response"]["items"][i]["id"])
                print("Поста ещё не было")
                parsering.add_new_id_of_news(url, news["response"]["items"][i]["id"])
                try:
                    await publish_post_in_channel(chat_id, news["response"]["items"][i]["id"])
                except Exception as e:
                    await asyncio.sleep(60)
                    await publish_post_in_channel(chat_id, news["response"]["items"][i]["id"])
                await asyncio.sleep(5)
        print("Новых постов пока нет!")
        await asyncio.sleep(delay_time)

async def publish_post_in_channel(chat_id, post_id):
    # try:
    news = []
    item_id = int
    url = "kvantorium62"
    with open(f"groups/{url}/{url}.json", "r", encoding="utf-8") as read_file:
        news = json.load(read_file)
    with open('BEST_MAT_EVER.txt', 'r', encoding='Windows-1251') as f_ck:
        f_ck_list = set([a.rstrip().casefold() for a in f_ck])
    news_split = []
    news_censured = []

    for n in range(len(news["response"]["items"])):
        if str(post_id) in str(news["response"]["items"][n]["id"]):
            print("Нашлось")
            item_id = n


    for i in news["response"]["items"][item_id]["text"].split(' '):
        news_split.append(i)
    if "copy_history" in news["response"]["items"][item_id]:
        news_split.append("\n")
        for i in news["response"]["items"][item_id]["copy_history"][0]["text"].split(' '):
            news_split.append(i)
    for b in range(0, len(news_split)):
        if news_split[b].translate(str.maketrans('', '', string.punctuation)).casefold() in f_ck_list:
            news_split[
                b] = f'<tg-spoiler>{news_split[b][0]}{(len(news_split[b]) - 2) * "*"}{news_split[b][len(news_split[b]) - 1]}</tg-spoiler>'
        news_censured.append(news_split[b])
    final_text = ' '.join(news_censured)
    media = types.MediaGroup()
    video_url = []
    global y
    y = 0
    global media_len
    media_len = 0
    global txt
    txt = ""
    global caption_photo
    caption_photo = final_text[:850]
    # print("\n", final_text)

    for a in range(len(news["response"]["items"][item_id]["attachments"])):
        if news["response"]["items"][item_id]["attachments"][a]["type"] == "video":
            txt = txt + '\n' + f'https://vk.com/video{news["response"]["items"][item_id]["attachments"][a]["video"]["owner_id"]}_{news["response"]["items"][item_id]["attachments"][a]["video"]["id"]}'
        if news["response"]["items"][item_id]["attachments"][a]["type"] == "photo":
            y += 1

    if len(news["response"]["items"][item_id]["attachments"]) == 0:
        if "copy_history" in news["response"]["items"][item_id]:
            for q in range(len(news["response"]["items"][item_id]["copy_history"][0]["attachments"])):
                if news["response"]["items"][item_id]["copy_history"][0]["attachments"][q]["type"] == "video":
                    txt = txt + '\n' + f'https://vk.com/video{news["response"]["items"][item_id]["copy_history"][0]["attachments"][q]["video"]["owner_id"]}_{news["response"]["items"][item_id]["copy_history"][0]["attachments"][q]["video"]["id"]}'
                if news["response"]["items"][item_id]["copy_history"][0]["attachments"][q]["type"] == "photo":
                    y += 1

            if len(news["response"]["items"][item_id]["copy_history"][0]["attachments"]) == 0:
                await bot.send_message(chat_id, text=f'{final_text}\n'
                                                                 f'(Источник: https://vk.com/wall{news["response"]["items"][item_id]["from_id"]}_{news["response"]["items"][0]["id"]})')

            for q in range(len(news["response"]["items"][item_id]["copy_history"][0]["attachments"])):
                if len(news["response"]["items"][item_id]["copy_history"][0]["attachments"]) == 1:
                    if news["response"]["items"][item_id]["copy_history"][0]["attachments"][q]["type"] == "photo":
                        await bot.send_photo(chat_id,
                                             photo=
                                             news["response"]["items"][item_id]["copy_history"][0]["attachments"][q][
                                                 "photo"]["sizes"][
                                                 -1]["url"],
                                             caption=f'{caption_photo}\n'
                                                     f'(Источник: https://vk.com/wall{news["response"]["items"][item_id]["from_id"]}_{news["response"]["items"][0]["id"]})')
                    if news["response"]["items"][item_id]["copy_history"][0]["attachments"][q]["type"] == "video":
                        video_post_id = news["response"]["items"][item_id]["copy_history"][0]["attachments"][q]["video"][
                            "id"]
                        video_owner_id = news["response"]["items"][item_id]["copy_history"][0]["attachments"][q]["video"][
                            "owner_id"]
                        await bot.send_message(chat_id,
                                               text=f'https://vk.com/video{video_owner_id}_{video_post_id}'
                                                    f'\n{caption_photo}\n'
                                                    f'(Источник: https://vk.com/wall{news["response"]["items"][item_id]["from_id"]}_{news["response"]["items"][0]["id"]})')
                    if news["response"]["items"][item_id]["copy_history"][0]["attachments"][q]["type"] != "video" and \
                            news["response"]["items"][item_id]["copy_history"][0]["attachments"][q]["type"] != "photo":
                        await bot.send_message(chat_id, text=f'\n{caption_photo}\n'
                                                                         f'(Источник: https://vk.com/wall{news["response"]["items"][item_id]["from_id"]}_{news["response"]["items"][item_id]["id"]})')

                if len(news["response"]["items"][item_id]["copy_history"][0]["attachments"]) > 1:
                    # print(y)
                    if y == 0:
                        await bot.send_message(chat_id,
                                               text=f'{txt}'
                                                    f'{caption_photo}\n'
                                                    f'(Источник: https://vk.com/wall{news["response"]["items"][item_id]["from_id"]}_{news["response"]["items"][0]["id"]})')
                    if y == 1:
                        if news["response"]["items"][item_id]["copy_history"][0]["attachments"][q]["type"] == "photo":
                            media.attach_photo(
                                news["response"]["items"][item_id]["copy_history"][0]["attachments"][q]["photo"]["sizes"][
                                    -1]["url"],
                                f'{txt} \n {caption_photo}\n ((Источник: https://vk.com/wall{news["response"]["items"][item_id]["from_id"]}_{news["response"]["items"][item_id]["id"]})')
                            media_len = media_len + 1
                    if y > 1:
                        # print(media_len)
                        if media_len == 0:
                            if news["response"]["items"][item_id]["copy_history"][0]["attachments"][q]["type"] == "photo":
                                # print(media_len)
                                # print(txt + "\n" + caption_photo)
                                media.attach_photo(
                                    news["response"]["items"][item_id]["copy_history"][0]["attachments"][q]["photo"][
                                        "sizes"][-1]["url"],
                                    f'{txt} \n {caption_photo}\n (Источник: https://vk.com/wall{news["response"]["items"][item_id]["from_id"]}_{news["response"]["items"][0]["id"]})')
                                media_len = media_len + 1
                        if media_len > 0 and media_len < 10:
                            # print(media_len)
                            if news["response"]["items"][item_id]["copy_history"][0]["attachments"][q]["type"] == "photo":
                                media.attach_photo(
                                    news["response"]["items"][item_id]["copy_history"][0]["attachments"][q]["photo"][
                                        "sizes"][-1]["url"])
                                media_len = media_len + 1
        else:
            await bot.send_message(chat_id, text=f'{final_text}\n'
                                                             f'(Источник: https://vk.com/wall{news["response"]["items"][item_id]["from_id"]}_{news["response"]["items"][0]["id"]})')

    for a in range(len(news["response"]["items"][item_id]["attachments"])):
        if len(news["response"]["items"][item_id]["attachments"]) == 1:
            if news["response"]["items"][item_id]["attachments"][a]["type"] == "photo":
                await bot.send_photo(chat_id,
                                     photo=news["response"]["items"][item_id]["attachments"][a]["photo"]["sizes"][-1][
                                         "url"],
                                     caption=f'{caption_photo}\n'
                                             f'(Источник: https://vk.com/wall{news["response"]["items"][item_id]["from_id"]}_{news["response"]["items"][item_id]["id"]})')
            if news["response"]["items"][0]["attachments"][a]["type"] == "video":
                video_post_id = news["response"]["items"][item_id]["attachments"][a]["video"]["id"]
                video_owner_id = news["response"]["items"][item_id]["attachments"][a]["video"]["owner_id"]
                await bot.send_message(chat_id,
                                       text=f'https://vk.com/video{video_owner_id}_{video_post_id}'
                                            f'\n{caption_photo}\n'
                                            f'(Источник: https://vk.com/wall{news["response"]["items"][item_id]["from_id"]}_{news["response"]["items"][item_id]["id"]})')
            if news["response"]["items"][item_id]["attachments"][a]["type"] != "video" and \
                    news["response"]["items"][item_id]["attachments"][a]["type"] != "photo":
                await bot.send_message(chat_id, text=f'\n{caption_photo}\n'
                                                                 f'(Источник: https://vk.com/wall{news["response"]["items"][item_id]["from_id"]}_{news["response"]["items"][item_id]["id"]})')

        if len(news["response"]["items"][item_id]["attachments"]) > 1:
            # print(y)
            if y == 0:
                await bot.send_message(chat_id,
                                       text=f'{txt}'
                                            f'{caption_photo}\n'
                                            f'(Источник: https://vk.com/wall{news["response"]["items"][item_id]["from_id"]}_{news["response"]["items"][item_id]["id"]})')
            if y == 1:
                if news["response"]["items"][item_id]["attachments"][a]["type"] == "photo":
                    media.attach_photo(
                        news["response"]["items"][item_id]["attachments"][a]["photo"]["sizes"][-1]["url"],
                        f'{txt} \n {caption_photo}\n ((Источник: https://vk.com/wall{news["response"]["items"][item_id]["from_id"]}_{news["response"]["items"][item_id]["id"]})')
                    media_len = media_len + 1
            if y > 1:
                # print(media_len)
                if media_len == 0:
                    if news["response"]["items"][item_id]["attachments"][a]["type"] == "photo":
                        # print(media_len)
                        # print(txt + "\n" + caption_photo)
                        media.attach_photo(
                            news["response"]["items"][item_id]["attachments"][a]["photo"]["sizes"][-1]["url"],
                            f'{txt} \n {caption_photo}\n (Источник: https://vk.com/wall{news["response"]["items"][item_id]["from_id"]}_{news["response"]["items"][item_id]["id"]})')
                        media_len = media_len + 1
                if media_len > 0 and media_len < 10:
                    # print(media_len)
                    if news["response"]["items"][item_id]["attachments"][a]["type"] == "photo":
                        media.attach_photo(
                            news["response"]["items"][item_id]["attachments"][a]["photo"]["sizes"][-1]["url"])
                        media_len = media_len + 1

    # print("len(news):", len(news["response"]["items"][0]["attachments"]))
    # print("y:", y)
    # print("media:", media)
    # print("media_len:", media_len)
    if media_len > 0:
        await bot.send_media_group(chat_id, media=media)

    del news["response"]["items"][item_id]
    with open(f"groups/{url}/{url}.json", "w", encoding="utf-8") as file:
        json.dump(news, file, ensure_ascii=None)

    # except Exception as e:
    #     # print('User: ', msg.from_user.id, f'\nError: ', repr(e))
    #     print(f'\nError: {repr(e)}')
    #     await bot.send_message(chat_id, f'Произошла ошибка. Попробуйте ещё раз...\nError: {repr(e)}')
    #     # await bot.send_sticker(msg.from_user.id, sticker="CAACAgIAAxkBAAEIF29kDIAYLLLdvNARmO2dnMzNCZzzNAACkiMAAmv4yEiZGesZWjzE7S8E")
    #     del news["response"]["items"][0]
    #     with open(f"groups/{url}/{url}.json", "w", encoding="utf-8") as file:
    #         json.dump(news, file, ensure_ascii=None)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # loop.create_task(parsering.delete_groups(3600))
    # loop.create_task(publish_post_in_channel(chat_id))
    task = loop.create_task(check_publishing(3600))
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
