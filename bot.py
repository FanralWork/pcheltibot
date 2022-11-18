import telebot
import config
import parsering
import random
from telebot import types

bot = telebot.TeleBot(config.TOKEN)

URL = 'https://www.anekdot.ru/random/anekdot/'

@bot.message_handler(commands=['start'])
def welcome(message):
    #keybord
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Чел ты")
    item2 = types.KeyboardButton("Расскажи анекдот")

    markup1.add(item1, item2)

    #Hello
    bot.send_message(message.chat.id, "Приветствую, {0.first_name}!\nЯ - <b>{1.first_name}</b>, развлекательно-новостной бот.".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup1)

@bot.message_handler(content_types=['text'])
def Answer(message):
    if message.text == 'Чел ты':
        markup1 = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Не понял", callback_data='not_understand')
        item2 = types.InlineKeyboardButton("Ты это про себя?", callback_data='about_about')

        markup1.add(item1, item2)

        bot.send_message(message.chat.id, 'Сам такой', reply_markup=markup1)
    elif message.text == 'Расскажи анекдот':
        joke_list = parsering.parser_of_jokes(URL)
        random.shuffle(joke_list)
        bot.send_message(message.chat.id, f'{joke_list[0]}')
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
    else:
        bot.send_message(message.chat.id, 'Я не знаю такую команду')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'not_understand':
                bot.send_message(call.message.chat.id, 'Забей')
            elif call.data == 'about_about':
                bot.send_message(call.message.chat.id, 'Да')

            # remote inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Сам такой",
                                  reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Ладно")

    except Exception as e:
        print(repr(e))

bot.polling(none_stop=True)