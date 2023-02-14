import string
from aiogram import Bot, executor, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
import config
import parsering
import json
import os

URL_jokes = 'https://www.anekdot.ru/random/anekdot/'

token = config.TOKEN

bot = Bot(token)
dp = Dispatcher(bot=bot)

keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True)
Button1 = KeyboardButton('Расскажи анекдот')
#Button2 = KeyboardButton('Фото')
keyboard1.add(Button1)

inlinekeyboard1 = InlineKeyboardMarkup()
inlinebutton1 = InlineKeyboardButton(text='❤️', callback_data='bettercallsaul')
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

@dp.message_handler()
async def send_joke(msg: types.Message):
    if msg.text == 'Расскажи анекдот':
        jokes = []
        with open("jokes.json", "r", encoding="utf-8") as read_file:
            jokes = json.load(read_file)
        if len(jokes) == 0:
            parsering.parser_of_jokes(URL_jokes)
            with open("jokes.json", "r", encoding="utf-8") as read_file:
                jokes = json.load(read_file)
        #print(jokes)
        with open('BEST_MAT_EVER.txt', 'r', encoding='utf-8') as f_ck:
            f_ck_list = set([i.rstrip() for i in f_ck])
        if {i.casefold().translate(str.maketrans('','', string.punctuation)) for i in jokes[0].split(' ')}\
            .intersection(f_ck_list):
            
            await bot.send_message(chat_id=msg.chat.id, text=f'{jokes[0]}\n (Источник: {URL_jokes.replace("https://", " ")})', disable_web_page_preview=True, reply_markup=keyboard1)
        del jokes[0]
        with open("jokes.json", "w", encoding="utf-8") as file:
            json.dump(jokes, file, ensure_ascii=None)


@dp.callback_query_handler()
async def message_callback(callback: types.CallbackQuery):
    if callback.data == 'bettercallsaul':
        await callback.answer('Ладно')


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)