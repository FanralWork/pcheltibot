import string
from aiogram import Bot, executor, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
import config
import parsering
import json
import os
import random

#URL_jokes = 'https://www.anekdot.ru/random/anekdot/'
#URL_jokes = 'https://www.anekdot.ru/'
URL_facts = 'https://randstuff.ru/fact'
URL_rhymes = 'rhymes'
URL_kvantorium62 = 'kvantorium62'

token = config.TOKEN
#token = config.SPARE_TOKEN
token_vk = config.Token_vk
bot = Bot(token)
dp = Dispatcher(bot=bot)

keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True)
# Button1 = KeyboardButton('Расскажи анекдот')
Button1 = KeyboardButton('Интересный факт')
Button2 = KeyboardButton('Новости')
keyboard1.add(Button1,Button2)

keyboard2 = ReplyKeyboardMarkup(resize_keyboard=True)
Button3 = KeyboardButton('Общие')
Button4 = KeyboardButton('Кванториума')
Button5 = KeyboardButton('Назад')
keyboard2.insert(Button3)
keyboard2.insert(Button4)
keyboard2.row(Button5)

keyboard3 = ReplyKeyboardMarkup(resize_keyboard=True)
Button6 = KeyboardButton('Случайные')
Button7 = KeyboardButton('Лучшие сегодня')
Button8 = KeyboardButton('Назад')
keyboard3.insert(Button6)
keyboard3.insert(Button7)
keyboard3.row(Button8)

async def on_startup(_):
    print("Bot is active!")

@dp.message_handler(commands=["start"])
async def send_message(msg: types.Message):
    bot_name = await bot.get_me()
    await msg.answer(f"Приветствую, {msg.from_user.full_name}!\nЯ - <b>{bot_name.first_name}</b>, развлекательно-новостной бот.",
                     parse_mode="html", reply_markup=keyboard1)
    await bot.send_sticker(msg.from_user.id, sticker="CAACAgIAAxkBAAEHfLhj1TfnDTXgju-hIIhQ7ssUdAZAdAACwRIAAvXQth0OkELw6I25My0E")
    await msg.delete()

@dp.message_handler(text=['Меню','Назад'])
async def menu(msg: types.Message):
    await bot.send_message(chat_id=msg.chat.id,
                           text=f"Функционал: \n - Анекдоты, \n - Новости",
                           disable_web_page_preview=True, reply_markup=keyboard1, parse_mode="html")

@dp.message_handler(text=['Интересный факт'])
async def send_joke(msg: types.Message):
    try:
        if msg.text == 'Интересный факт':
            facts = parsering.parser_facts(URL_facts)
            with open('BEST_MAT_EVER.txt', 'r', encoding='Windows-1251') as f_ck:
                f_ck_list = set([a.rstrip().casefold() for a in f_ck])
            facts_split = []
            facts_censured = []
            for i in facts[0].split(' '):
                facts_split.append(i)
            for b in range(0, len(facts_split)):
                if facts_split[b].translate(str.maketrans('','', string.punctuation)).casefold() in f_ck_list:
                    facts_split[b] = f'<tg-spoiler>{facts_split[b][0]}{(len(facts_split[b]) - 2) * "*"}' \
                                     f'{facts_split[b][len(facts_split[b])-1]}</tg-spoiler>'
                facts_censured.append(facts_split[b])
            final_text = ' '.join(facts_censured)
            await bot.send_message(chat_id=msg.chat.id, text=f'{final_text}\n (Источник: '
                                                             f'{URL_facts.replace("https://", " ")})',
                                   disable_web_page_preview=True, reply_markup=keyboard1, parse_mode="html")

    except Exception as e:
        print('User: ', msg.from_user.id, f'\nError: ', repr(e))
        await bot.send_message(msg.chat.id, f'Произошла ошибка. Попробуйте ещё раз...\nError: {repr(e)}', reply_markup=keyboard1)
        # await bot.send_sticker(msg.from_user.id,
        #                        sticker="CAACAgIAAxkBAAEIF29kDIAYLLLdvNARmO2dnMzNCZzzNAACkiMAAmv4yEiZGesZWjzE7S8E")

@dp.message_handler(text=['Новости', 'Общие', 'Кванториума'])
async def send_news(msg: types.Message):
    url = str
    if msg.text == "Общие":
        url = URL_rhymes
    if msg.text == "Кванториума":
        url = URL_kvantorium62
    if msg.text == "Общие" or msg.text == "Кванториума":
        try:
            news = []
            with open(f"{url}/{url}.json", "r", encoding="utf-8") as read_file:
                news = json.load(read_file)
            if len(news["response"]["items"]) == 0:
                parsering.parser_vk(url)
                with open(f"{url}/{url}.json", "r", encoding="utf-8") as read_file:
                    news = json.load(read_file)
            with open('BEST_MAT_EVER.txt', 'r', encoding='Windows-1251') as f_ck:
                f_ck_list = set([a.rstrip().casefold() for a in f_ck])
            news_split = []
            news_censured = []
            for i in news["response"]["items"][0]["text"].split(' '):
                news_split.append(i)
            for b in range(0, len(news_split)):
                if news_split[b].translate(str.maketrans('','', string.punctuation)).casefold() in f_ck_list:
                    news_split[b] = f'<tg-spoiler>{news_split[b][0]}{(len(news_split[b]) - 2) * "*"}{news_split[b][len(news_split[b])-1]}</tg-spoiler>'
                news_censured.append(news_split[b])
            final_text = ' '.join(news_censured)
            a = 0
            b = 0
            media = types.MediaGroup()
            video_url = []
            caption_photo = final_text
            # print(len(caption_photo))
            for a in range(len(news["response"]["items"][0]["attachments"])):
                if news["response"]["items"][0]["attachments"][a]["type"] == "photo":
                    if len(caption_photo) > 1000:
                        media.attach_photo(news["response"]["items"][0]["attachments"][a]["photo"]["sizes"][-1]["url"],
                                           f'{caption_photo[:900]}...\n (Источник: {url.replace("https://", " ")})')
                    else:
                        media.attach_photo(news["response"]["items"][0]["attachments"][a]["photo"]["sizes"][-1]["url"],
                                           f'{caption_photo}\n (Источник: {url.replace("https://", " ")})',
                                           parse_mode="html")
                    b=b+1
                    # print(f"Media: {media}")
                if news["response"]["items"][0]["attachments"][a]["type"] == "video":
                    video_post_id = news["response"]["items"][0]["attachments"][a]["video"]["id"]
                    video_owner_id = news["response"]["items"][0]["attachments"][a]["video"]["owner_id"]
                    video_url.append(f"https://vk.com/video{video_owner_id}_{video_post_id}")
            if b == 1:
                if len(video_url) > 0:
                    c=0
                    await bot.send_message(chat_id=msg.chat.id,
                                            text=f'{final_text}\n (Источник: {url.replace("https://", " ")})',
                                            disable_web_page_preview=True, reply_markup=keyboard2, parse_mode="html")
                    for c in range(len(video_url)):
                        await bot.send_message(chat_id=msg.chat.id, text=video_url[c])
                else:
                    await bot.send_media_group(chat_id=msg.chat.id, media=media)
            else:
                if b == 0:
                    await bot.send_message(chat_id=msg.chat.id,
                                            text=f'{final_text}\n (Источник: {url.replace("https://", " ")})',
                                            disable_web_page_preview=True, reply_markup=keyboard2, parse_mode="html")
                else:
                    await bot.send_message(chat_id=msg.chat.id,
                                            text=f'{final_text}\n (Источник: {url.replace("https://", " ")})',
                                            disable_web_page_preview=True, reply_markup=keyboard2, parse_mode="html")
                    await bot.send_media_group(chat_id=msg.chat.id, media=media)
                if len(video_url) > 0:
                    c = 0
                    for c in range(len(video_url)):
                        await bot.send_message(chat_id=msg.chat.id, text=video_url[c])
            del news["response"]["items"][0]
            with open(f"{url}/{url}.json", "w", encoding="utf-8") as file:
                json.dump(news, file, ensure_ascii=None)

        except Exception as e:
            print('User: ', msg.from_user.id, f'\nError: ', repr(e))
            await bot.send_message(msg.chat.id, f'Произошла ошибка. Попробуйте ещё раз...\nError: {repr(e)}', reply_markup=keyboard2)
            #await bot.send_sticker(msg.from_user.id, sticker="CAACAgIAAxkBAAEIF29kDIAYLLLdvNARmO2dnMzNCZzzNAACkiMAAmv4yEiZGesZWjzE7S8E")
            del news["response"]["items"][0]
            with open(f"{url}/{url}.json", "w", encoding="utf-8") as file:
                 json.dump(news, file, ensure_ascii=None)

    else:
        await bot.send_message(chat_id=msg.chat.id,
                               text=f"Выберите категорию: \n - Общие, \n - Кванториума",
                               disable_web_page_preview=True, reply_markup=keyboard2, parse_mode="html")

@dp.callback_query_handler()
async def message_callback(callback: types.CallbackQuery):
    print("Callback data")
    if callback.data == 'common':
        send_news('Общие')
        #await callback.answer('Ладно')
    if callback.data == 'kvantorium62':
        send_news('Кванториума')


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)