import telebot
import config
import parsering
import random
from telebot import types
import json
import yt_dlp
import os

bot = telebot.TeleBot(config.TOKEN)

URL_jokes = 'https://www.anekdot.ru/random/anekdot/'
URL_common = 'https://vk.com/rhymes'

@bot.message_handler(commands=['start'])
def welcome(message):
    try:
        #keybord
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        #item1 = types.KeyboardButton("Чел ты")
        item2 = types.KeyboardButton("Расскажи анекдот")
        item3 = types.KeyboardButton("Новости")

        markup1.add(item2, item3)

        #Hello
        bot.send_message(message.chat.id, "Приветствую, {0.first_name}!\nЯ - <b>{1.first_name}</b>, развлекательно-новостной бот.".format(message.from_user, bot.get_me()),
                         parse_mode='html', reply_markup=markup1)
    except Exception as e:
        print(repr(e))

@bot.message_handler(content_types=['text'])
def Answer(message):
    try:
        if message.text == 'Чел ты':
            markup1 = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Не понял", callback_data='not_understand')
            item2 = types.InlineKeyboardButton("Ты это про себя?", callback_data='about_about')
            markup1.add(item1, item2)
            bot.send_message(message.chat.id, 'Сам такой', reply_markup=markup1)
        elif message.text == 'Меню' or message.text == 'Назад':
            markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            #item1 = types.KeyboardButton("Чел ты")
            item2 = types.KeyboardButton("Расскажи анекдот")
            item3 = types.KeyboardButton("Новости")
            markup3.add(item2, item3)
            bot.send_message(message.chat.id, f"Мои функции: \n- Расскажи анекдот \n- Новости", reply_markup=markup3)
        elif message.text == 'Расскажи анекдот' or message.text == 'Расскажи ещё шутку':
            markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Назад")
            item2 = types.KeyboardButton("Расскажи ещё шутку")

            markup2.add(item1, item2)

            joke_list = parsering.parser_of_jokes(URL_jokes)
            random.shuffle(joke_list)
            bot.send_message(message.chat.id, f'{joke_list[0]} \n (Источник: {URL_jokes.replace("https://", " ")})', reply_markup=markup2, disable_web_page_preview=True)
            del joke_list[0]
            #for i in range(0,len(joke)):
            #    joke = x[i]
                    #print(joke)
              # rand_int = random.randint(1, len(joke))
               # bot.send_message(message.chat.id,joke[rand_int])
            #if len(parser.list_of_jokes) == 0:
                #parser.apply_jokes
            #else:
                #rand_int=random.randint(1,10)
                #bot.send_message(message.chat.id, parser.list_of_jokes[rand_int])
                #del parser.list_of_jokes[rand_int]
        elif message.text == 'Новости' or message.text == 'Ещё новости':
            markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Назад")
            item2 = types.KeyboardButton("Ещё новости")
            markup2.add(item1, item2)
            with open("news.json", "r", encoding="utf-8") as read_file:
                news_title = json.load(read_file)
            print(len(news_title))
            with open("media.json", "r", encoding="utf-8") as read_file:
                news_media = json.load(read_file)
            print(len(news_media))
            print(news_title["common"][0])
            if len(news_title["common"]) == 0:
                parsering.parser_of_news(URL_common)
                print("Парсинг")
                with open("news.json", "r", encoding="utf-8") as read_file:
                    news_title = json.load(read_file)
                with open("media.json", "r", encoding="utf-8") as read_file:
                    news_media = json.load(read_file)
            bot.send_message(message.chat.id, f'{news_title["common"][0].replace("Показать ещё", " ")} \n- Источник: {URL_common.replace("https://", " ")}', reply_markup=markup2, disable_web_page_preview=True)
            if "video" in news_media[0]:
                try:
                    print(news_media[0])
                    ydl_opts = {'username': '18305212355', 'password': 'pZuwxsOh', 'recode-video': '.mp4'}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        msg = bot.send_message(message.chat.id, "Идёт отправка видео. Подождите...",reply_markup=markup2)
                        ydl.download([news_media[0]])
                        video_name = [_ for _ in os.listdir() if _.endswith(".mp4")]
                        print(video_name)
                        bot.send_video(message.chat.id, video = open(video_name[0], 'rb'), reply_markup=markup2)
                        bot.delete_message(message.chat.id, msg.message_id)
                        os.remove(video_name[0])
                except Exception as e:
                    print('User: ', message.from_user.id, f'\nError: ', repr(e))
                    bot.send_message(message.chat.id, 'Произошла ошибка. Попробуйте ещё раз...',
                                     reply_markup=markup2)
            else:
                bot.send_photo(message.chat.id, f'{news_media[0]}', reply_markup=markup2)
            del news_title["common"][0]
            del news_media[0]
            with open("news.json", "w", encoding="utf-8") as write_file:
                json.dump(news_title, write_file, ensure_ascii=None)
            with open("media.json", "w", encoding="utf-8") as write_file:
                json.dump(news_media, write_file, ensure_ascii=None)
        else:
            bot.send_message(message.chat.id, 'Я не знаю такую команду')
    except Exception as e:
        print('User: ', message.from_user.id, f'\nError: ', repr(e))

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        '''if call.data == 'delete':
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)'''
        if call.data == 'not_understand':
            bot.send_message(call.message.chat.id, 'Забей')
        elif call.data == 'about_about':
            bot.send_message(call.message.chat.id, 'Да')

        # remote inline buttons
        if call.data == 'not_understand' or call.data == 'about_about':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Сам такой",
                                  reply_markup=None)

            #show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Ладно")

    except Exception as e:
        print(repr(e))

bot.polling(none_stop=True)