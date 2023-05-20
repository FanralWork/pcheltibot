import sqlite3
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from db import BotDB

class BotKeyboards:
    def __init__(self, db_file):
        self.BotDB = BotDB(db_file)

    def get_news_keyboard(self, msg):
        user_groups = self.BotDB.check_user_group(msg)
        group1 = user_groups[5]
        group2 = user_groups[6]
        group3 = user_groups[7]

        news_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        Button1 = KeyboardButton('Новости Кванториума')
        if not (group1) == None:
            Button2 = KeyboardButton(group1.replace("https://vk.com/", ""))
        else:
            Button2 = KeyboardButton("Добавить группу")
        if not (group2) == None:
            Button3 = KeyboardButton(group2.replace("https://vk.com/", ""))
        else:
            Button3 = KeyboardButton("Добавить группу")
        if not (group3) == None:
            Button4 = KeyboardButton(group3.replace("https://vk.com/", ""))
        else:
            Button4 = KeyboardButton("Добавить группу")
        Button5 = KeyboardButton('Настроить группы')
        Button6 = KeyboardButton('Назад')
        news_keyboard.add(Button1)
        news_keyboard.add(Button2)
        news_keyboard.insert(Button3)
        news_keyboard.insert(Button4)
        news_keyboard.row(Button5)
        news_keyboard.row(Button6)
        return news_keyboard

    def get_settings_inline_keyboard(self, msg):
        user_groups = self.BotDB.check_user_group(msg)
        group1 = user_groups[5]
        group2 = user_groups[6]
        group3 = user_groups[7]

        setting_inline_keyboard = InlineKeyboardMarkup()
        if not (group1) == None:
            Button6 = InlineKeyboardButton(group1.replace("https://vk.com/", ""), callback_data='user_group1')
        else:
            Button6 = InlineKeyboardButton("Свободная ячейка", callback_data='user_group1')
        setting_inline_keyboard.row(Button6)
        if not (group2) == None:
            Button6 = InlineKeyboardButton(group2.replace("https://vk.com/", ""), callback_data='user_group2')
        else:
            Button6 = InlineKeyboardButton("Свободная ячейка", callback_data='user_group2')
        setting_inline_keyboard.row(Button6)
        if not (group3) == None:
            Button6 = InlineKeyboardButton(group3.replace("https://vk.com/", ""), callback_data='user_group3')
        else:
            Button6 = InlineKeyboardButton("Свободная ячейка", callback_data='user_group3')
        setting_inline_keyboard.row(Button6)
        return setting_inline_keyboard

    def get_cancel_keyboard(self):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        Button1 = KeyboardButton('Назад')
        keyboard.add(Button1)
        return keyboard