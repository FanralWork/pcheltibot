import string
from aiogram import Bot, executor, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
import config
import parsering
import json
import os

URL_jokes = 'https://www.anekdot.ru/random/anekdot/'
URL_rhymes = 'rhymes'

token = config.TOKEN
token_vk = config.Token_vk

bot = Bot(token)
dp = Dispatcher(bot=bot)

keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True)
Button1 = KeyboardButton('Расскажи анекдот')
Button2 = KeyboardButton('Новости')
keyboard1.add(Button1,Button2)

inlinekeyboard1 = InlineKeyboardMarkup()
inlinebutton1 = InlineKeyboardButton(text='❤', callback_data='bettercallsaul')
inlinekeyboard1.add(inlinebutton1)

async def on_startup(_):
    print("Bot is active!")

@dp.message_handler(commands=["start"])
async def send_message(msg: types.Message):
    bot_name = await bot.get_me()
    await msg.answer(f"Приветствую, {msg.from_user.full_name}!\nЯ - <b>{bot_name.first_name}</b>, развлекательно-новостной бот.",
                     parse_mode="html", reply_markup=keyboard1)
    await bot.send_sticker(msg.from_user.id, sticker="CAACAgIAAxkBAAEHfLhj1TfnDTXgju-hIIhQ7ssUdAZAdAACwRIAAvXQth0OkELw6I25My0E")
    await msg.delete()

@dp.message_handler(text=['Расскажи анекдот'])
async def send_joke(msg: types.Message):
    try:
        if msg.text == 'Расскажи анекдот':
            jokes = []
            with open("jokes.json", "r", encoding="utf-8") as read_file:
                jokes = json.load(read_file)
            if len(jokes) == 0:
                parsering.parser_of_jokes(URL_jokes)
                with open("jokes.json", "r", encoding="utf-8") as read_file:
                    jokes = json.load(read_file)
            #print(jokes)
            with open('BEST_MAT_EVER.txt', 'r', encoding='Windows-1251') as f_ck:
                f_ck_list = set([a.rstrip().casefold() for a in f_ck])
            jokes_split = []
            jokes_censured = []
            '''if {i.casefold().translate(str.maketrans('','', string.punctuation)) for i in jokes[0].split(' ')}\
                .intersection(f_ck_list): '''
            for i in jokes[0].split(' '):
                #print(type(jokes_split))
                jokes_split.append(i)
                #print(jokes_split)
            for b in range(0, len(jokes_split)):
                if jokes_split[b].translate(str.maketrans('','', string.punctuation)).casefold() in f_ck_list:
                    #print(len(jokes_split[b]))
                    jokes_split[b] = f'<tg-spoiler>{jokes_split[b][0]}{(len(jokes_split[b]) - 2) * "*"}{jokes_split[b][len(jokes_split[b])-1]}</tg-spoiler>'
                jokes_censured.append(jokes_split[b])
            final_text = ' '.join(jokes_censured)
            #await bot.send_message(chat_id=msg.chat.id, text=f'<tg-spoiler>{final_text}\n (Источник: {URL_jokes.replace("https://", " ")})</tg-spoiler>', disable_web_page_preview=True, reply_markup=keyboard1, parse_mode="html")
            await bot.send_message(chat_id=msg.chat.id, text=f'{final_text}\n (Источник: {URL_jokes.replace("https://", " ")})', disable_web_page_preview=True, reply_markup=keyboard1, parse_mode="html")
            del jokes[0]
            with open("jokes.json", "w", encoding="utf-8") as file:
                json.dump(jokes, file, ensure_ascii=None)
    except Exception as e:
        print('User: ', msg.from_user.id, f'\nError: ', repr(e))
        await bot.send_message(msg.chat.id, 'Произошла ошибка. Попробуйте ещё раз...', reply_markup=keyboard1)
        await bot.send_sticker(msg.from_user.id,
                               sticker="CAACAgIAAxkBAAEIF29kDIAYLLLdvNARmO2dnMzNCZzzNAACkiMAAmv4yEiZGesZWjzE7S8E")
        del jokes[0]

@dp.message_handler(text=['Новости'])
async def send_news(msg: types.Message):
    #try:
    news = []
    with open("rhymes/rhymes.json", "r", encoding="utf-8") as read_file:
        news = json.load(read_file)
    if len(news["response"]["items"]) == 0:
        parsering.parser_vk(URL_rhymes)
        with open("rhymes/rhymes.json", "r", encoding="utf-8") as read_file:
            news = json.load(read_file)
    #print(jokes)
    with open('BEST_MAT_EVER.txt', 'r', encoding='Windows-1251') as f_ck:
        f_ck_list = set([a.rstrip().casefold() for a in f_ck])
    news_split = []
    news_censured = []
    '''if {i.casefold().translate(str.maketrans('','', string.punctuation)) for i in jokes[0].split(' ')}\
        .intersection(f_ck_list): '''
    for i in news["response"]["items"][0]["text"].split(' '):
        #print(type(jokes_split))
        news_split.append(i)
        #print(jokes_split)
    for b in range(0, len(news_split)):
        if news_split[b].translate(str.maketrans('','', string.punctuation)).casefold() in f_ck_list:
            #print(len(jokes_split[b]))
            news_split[b] = f'<tg-spoiler>{news_split[b][0]}{(len(news_split[b]) - 2) * "*"}{news_split[b][len(news_split[b])-1]}</tg-spoiler>'
        news_censured.append(news_split[b])
    final_text = ' '.join(news_censured)
    #await bot.send_message(chat_id=msg.chat.id, text=f'<tg-spoiler>{final_text}\n (Источник: {URL_jokes.replace("https://", " ")})</tg-spoiler>', disable_web_page_preview=True, reply_markup=keyboard1, parse_mode="html")
    #await bot.send_message(chat_id=msg.chat.id, text=f'{final_text}\n (Источник: {URL_rhymes.replace("https://", " ")})', disable_web_page_preview=True, reply_markup=keyboard1, parse_mode="html")
    a = 0
    media = {}
    video_url = []
    #print(len(news["response"]["items"][0]["attachments"]))
    for a in range(len(news["response"]["items"][0]["attachments"])):
        if news["response"]["items"][0]["attachments"][a]["type"] == "photo":
            print(news["response"]["items"][0]["attachments"][a]["photo"]["sizes"][-1])
            media.update({a: news["response"]["items"][0]["attachments"][a]["photo"]["sizes"][-1]["url"]})
        if news["response"]["items"][0]["attachments"][a]["type"] == "video":
            video_access_key = news["response"]["items"][0]["attachments"][a]["video"]["access_key"]
            video_post_id = news["response"]["items"][0]["attachments"][a]["video"]["id"]
            video_owner_id = news["response"]["items"][0]["attachments"][a]["video"]["owner_id"]
            video_url.append(parsering.parser_vk_video(video_access_key, video_post_id, video_owner_id))
            media.update({a: video_url[-1]})

    #print(len(media))
    #print(media)
    if len(media) > 1:
        await bot.send_media_group(chat_id=msg.chat.id, media= media)
    else:
        if len(video_url) > 0:
            await bot.send_video(chat_id=msg.chat.id, video=video_url[0])
        else:
            await bot.send_photo(chat_id=msg.chat.id, caption=f'{final_text}\n (Источник: {URL_rhymes.replace("https://", " ")})', photo=media[0], reply_markup=keyboard1, parse_mode="html")
        #await bot.send_photo(chat_id=msg.chat.id, photo=media[0])
    del news["response"]["items"][0]
    with open("rhymes/rhymes.json", "w", encoding="utf-8") as file:
        json.dump(news, file, ensure_ascii=None)


    """except Exception as e:
        print('User: ', msg.from_user.id, f'\nError: ', repr(e))
        await bot.send_message(msg.chat.id, 'Произошла ошибка. Попробуйте ещё раз...', reply_markup=keyboard1)
        await bot.send_sticker(msg.from_user.id, sticker="CAACAgIAAxkBAAEIF29kDIAYLLLdvNARmO2dnMzNCZzzNAACkiMAAmv4yEiZGesZWjzE7S8E")
        del news["response"]["items"][0]"""

@dp.callback_query_handler()
async def message_callback(callback: types.CallbackQuery):
    if callback.data == 'bettercallsaul':
        await callback.answer('Ладно')


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)