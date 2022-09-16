import telebot
import config

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(content_types=['text'])
def start(message):
    bot.send_message(message.chat.id, 'Hi')

@bot.message_handler(content_types=['text'])
def Answer(message):
    if message.text == 'Чел ты':
        bot.send_message(message.chat.id, 'Сам такой')

bot.polling(none_stop=True)