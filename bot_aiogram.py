import string
from aiogram import Bot, executor, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
import config
import parsering
import json
import os

URL_jokes = 'https://www.anekdot.ru/random/anekdot/'
URL_rhymes = 'rhymes'
URL_kvantorium62 = 'kvantorium62'

token = config.TOKEN
token_vk = config.Token_vk

bot = Bot(token)
dp = Dispatcher(bot=bot)

keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True)
Button1 = KeyboardButton('Расскажи анекдот')
Button2 = KeyboardButton('Новости')
keyboard1.add(Button1,Button2)

keyboard2 = ReplyKeyboardMarkup(resize_keyboard=True)
Button3 = KeyboardButton('Общие')
Button4 = KeyboardButton('Кванториума')
Button5 = KeyboardButton('Назад')
keyboard2.insert(Button3)
keyboard2.insert(Button4)
keyboard2.row(Button5)

# inlinekeyboard1 = InlineKeyboardMarkup(resize_keyboard=True)
# inlinebutton1 = InlineKeyboardButton(text='Общие', callback_data='common')
# inlinebutton2 = InlineKeyboardButton(text='Кванториума', callback_data='kvantorium')
# inlinekeyboard1.add(inlinebutton1, inlinebutton2)

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

@dp.message_handler(text=['Новости', 'Общие', 'Кванториума'])
async def send_news(msg: types.Message):
    # print(msg.text)
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
            b = 0
            #media = {}
            media = types.MediaGroup()
            video_url = []
            #print(len(news["response"]["items"][0]["attachments"]))
            for a in range(len(news["response"]["items"][0]["attachments"])):
                if news["response"]["items"][0]["attachments"][a]["type"] == "photo":
                    #print(news["response"]["items"][0]["attachments"][a]["photo"]["sizes"][-1])
                    #media.update({a: news["response"]["items"][0]["attachments"][a]["photo"]["sizes"][-1]["url"]})
                    media.attach_photo(news["response"]["items"][0]["attachments"][a]["photo"]["sizes"][-1]["url"],
                                       f'{final_text}\n (Источник: {url.replace("https://", " ")})', parse_mode="html")
                    b=b+1

                    if len(final_text) > 4096:
                        for x in range(0, len(final_text), 4096):
                            await bot.send_message(chat_id=msg.chat.id,
                                                   text=f'{final_text[x:x + 4096]}\n (Источник: {url.replace("https://", " ")})',
                                                   disable_web_page_preview=True, reply_markup=keyboard2,
                                                   parse_mode="html")
                            #bot.send_message(message.chat.id, info[x:x + 4096])
                    else:
                        #bot.send_message(message.chat.id, info)
                        await bot.send_message(chat_id=msg.chat.id,
                                               text=f'{final_text}\n (Источник: {url.replace("https://", " ")})',
                                               disable_web_page_preview=True, reply_markup=keyboard2, parse_mode="html")

                if news["response"]["items"][0]["attachments"][a]["type"] == "video":
                    #video_access_key = news["response"]["items"][0]["attachments"][a]["video"]["access_key"]
                    video_post_id = news["response"]["items"][0]["attachments"][a]["video"]["id"]
                    video_owner_id = news["response"]["items"][0]["attachments"][a]["video"]["owner_id"]
                    #video_url.append(parsering.parser_vk_video(video_access_key, video_post_id, video_owner_id))
                    #media.update({a: video_url[-1]})
                    # media.attach_video(video_url[-1],
                    #                    f'{final_text}\n (Источник: {URL_rhymes.replace("https://", " ")})', parse_mode="html")
                    video_url.append(f"https://vk.com/video{video_owner_id}_{video_post_id}")
            #print(len(media))
            #print(media)
            #print(type(media))
            #if len(media) > 1:
            #print("send album")
            #print(media)
            #print(b)
            print(len(final_text))
            if b == 1:
                # await bot.send_message(chat_id=msg.chat.id,
                #                        text="https://vk.com/video_ext.php?oid=-28905875&id=456360218&hash=98575d50f515edb4&__ref=vk.api&api_hash=1679693691f3435aac022163a276_GQYDMNZVGI4TMNA",
                #                        reply_markup=keyboard1, parse_mode="html")
                if len(video_url) > 0:
                    c=0
                    #if len(final_text) > 4096:
                    if len(final_text) > 4096:
                        for x in range(0, len(final_text), 4096):
                            await bot.send_message(chat_id=msg.chat.id,
                                                   text=f'{final_text[x:x + 4096]}\n (Источник: {url.replace("https://", " ")})',
                                                   disable_web_page_preview=True, reply_markup=keyboard2,
                                                   parse_mode="html")
                            #bot.send_message(message.chat.id, info[x:x + 4096])
                    else:
                        #bot.send_message(message.chat.id, info)
                        await bot.send_message(chat_id=msg.chat.id,
                                               text=f'{final_text}\n (Источник: {url.replace("https://", " ")})',
                                               disable_web_page_preview=True, reply_markup=keyboard2, parse_mode="html")
                    for c in range(len(video_url)):
                        await bot.send_message(chat_id=msg.chat.id, text=video_url[c])
                else:
                    await bot.send_media_group(chat_id=msg.chat.id, media=media)
            else:
                if b == 0:
                    if len(final_text) > 4096:
                        for x in range(0, len(final_text), 4096):
                            await bot.send_message(chat_id=msg.chat.id,
                                                   text=f'{final_text[x:x + 4096]}\n (Источник: {url.replace("https://", " ")})',
                                                   disable_web_page_preview=True, reply_markup=keyboard2,
                                                   parse_mode="html")
                            # bot.send_message(message.chat.id, info[x:x + 4096])
                    else:
                        # bot.send_message(message.chat.id, info)
                        await bot.send_message(chat_id=msg.chat.id,
                                               text=f'{final_text}\n (Источник: {url.replace("https://", " ")})',
                                               disable_web_page_preview=True, reply_markup=keyboard2, parse_mode="html")
                else:
                    if len(final_text) > 4096:
                        for x in range(0, len(final_text), 4096):
                            await bot.send_message(chat_id=msg.chat.id,
                                                   text=f'{final_text[x:x + 4096]}\n (Источник: {url.replace("https://", " ")})',
                                                   disable_web_page_preview=True, reply_markup=keyboard2,
                                                   parse_mode="html")
                            # bot.send_message(message.chat.id, info[x:x + 4096])
                    else:
                        # bot.send_message(message.chat.id, info)
                        await bot.send_message(chat_id=msg.chat.id,
                                               text=f'{final_text}\n (Источник: {url.replace("https://", " ")})',
                                               disable_web_page_preview=True, reply_markup=keyboard2, parse_mode="html")
                    await bot.send_media_group(chat_id=msg.chat.id, media=media)
                    if len(video_url) > 0:
                        c = 0
                        for c in range(len(video_url)):
                            await bot.send_message(chat_id=msg.chat.id, video=video_url[c])
            '''else:
                if len(video_url) > 0:
                    #await bot.send_video(chat_id=msg.chat.id, video=video_url[0])
                    await bot.send_message(chat_id=msg.chat.id, text="Здесь должно быть видео")
                else:
                    print(media)
                    await bot.send_photo(chat_id=msg.chat.id, caption=f'{final_text}\n (Источник: {URL_rhymes.replace("https://", " ")})', photo=media[0], reply_markup=keyboard1, parse_mode="html")
                #await bot.send_photo(chat_id=msg.chat.id, photo=media[0])'''
            del news["response"]["items"][0]
            with open(f"{url}/{url}.json", "w", encoding="utf-8") as file:
                json.dump(news, file, ensure_ascii=None)


        except Exception as e:
            print('User: ', msg.from_user.id, f'\nError: ', repr(e))
            await bot.send_message(msg.chat.id, 'Произошла ошибка. Попробуйте ещё раз...', reply_markup=keyboard2)
            await bot.send_sticker(msg.from_user.id, sticker="CAACAgIAAxkBAAEIF29kDIAYLLLdvNARmO2dnMzNCZzzNAACkiMAAmv4yEiZGesZWjzE7S8E")
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