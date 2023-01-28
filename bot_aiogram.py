from aiogram import Bot, executor, Dispatcher, types
import config

token = config.TOKEN

bot = Bot(token)
dp = Dispatcher(bot=bot)

async def on_startup(_):
    print("Bot is active!")

@dp.message_handler(commands=["start"])
async def send_message(msg: types.Message):
    bot_name = await bot.get_me()
    await msg.answer(f"Приветствую, {msg.from_user.full_name}!\nЯ - <b>{bot_name.first_name}</b>, развлекательно-новостной бот.", parse_mode="html")
    await bot.send_sticker(msg.from_user.id, sticker="CAACAgIAAxkBAAEHfLhj1TfnDTXgju-hIIhQ7ssUdAZAdAACwRIAAvXQth0OkELw6I25My0E")
    await msg.delete()

@dp.message_handler()
async def send_echo(msg: types.Message):
    await msg.reply(msg.text)

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)