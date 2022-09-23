import telebot
import config

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    #keybord
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Чел ты")

    markup1.add(item1)

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
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Чел ты",
                                  reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Ладно")

    except Exception as e:
        print(repr(e))

bot.polling(none_stop=True)