from aiogram import Bot, executor, Dispatcher, types
import config

token = config.TOKEN

bot = Bot(token)
dp = Dispatcher(bot=bot)

@dp.message_handler(commands=["start"])
async def send_message(msg: types.Message):
    bot_name = await bot.get_me()
    await msg.answer(f"Приветствую, {msg.from_user.full_name}!\nЯ - <b>{bot_name.first_name}</b>, развлекательно-новостной бот.", parse_mode="html")
    await msg.delete()

@dp.message_handler()
async def send_echo(msg: types.Message):
    await msg.reply(msg.text)

if __name__ == "__main__":
    executor.start_polling(dp)