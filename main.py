import json
import logging
from config import API_TOKEN
from aiogram import Bot, Dispatcher, executor, types


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.update):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    print(message)
    await message.answer(
        "Добро пожаловать в MeChecker. MeChecker поможет Вам определить уровень тревоги, наличие депрессии, "
        "а также даст несколько советов о том, как привести дела в порядок. Помните, что оффлайн врача не заменит"
        " ни один онлайн бот, поэтому обязательно проконсультируйтесь с психологом/психотерапевтом."
        "\nДля старта теста нажмите /starttest")
    await message.answer_sticker("https://media0.giphy.com/media/5s4Jc4DqpjsJO/giphy.gif","")



@dp.message_handler(content_types=[types.ContentType.ANY])
async def echo(message: types.update):
    print("")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
    
# updates = requests.get(API_link + "/getUpdates?offset=-1").json()
#
# print(updates)
