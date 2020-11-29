import json
import logging
from config import API_TOKEN
from config import mydb
from aiogram import Bot, Dispatcher, executor, types
from buttons import button_start


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.CallbackQuery):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    print(message)
    await message.answer(
        "Добро пожаловать в MeChecker.\nMeChecker поможет Вам определить уровень тревоги, наличие депрессии, "
        "а также даст несколько советов о том, как привести дела в порядок. \nПомните, что оффлайн врача не заменит"
        " ни один онлайн бот, поэтому обязательно проконсультируйтесь с психологом или психотерапевтом.")

    await message.answer_sticker("https://media0.giphy.com/media/5s4Jc4DqpjsJO/giphy.gif", "", reply_markup=button_start)


@dp.callback_query_handler(text_contains='start')
async def process_callback_button1(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    mycursor = mydb.cursor()
    mycursor.execute("SELECT category FROM chatbot_test.categories;")
    myresult = mycursor.fetchall()
    categories_str = "Выберите один из следующих тестов:"
    i = 1
    for x in myresult:
        x = ''.join(x)
        categories_str += f"\n{i}. {x}"
        i+=1
    await call.message.answer(categories_str)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
    
# updates = requests.get(API_link + "/getUpdates?offset=-1").json()
#
# print(updates)
