import json
import logging
from config import API_TOKEN
from config import mydb
from aiogram import Bot, Dispatcher, executor, types
from buttons import *


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
async def process_callback_start(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    mycursor = mydb.cursor()
    mycursor.execute("SELECT id, category FROM chatbot_test.categories;")
    myresult = mycursor.fetchall()
    ids = []
    categories_str = "Выберите один из следующих тестов:"
    i = 1
    for x in myresult:
        ids.append(x[0])
        x = ''.join(x[1])
        categories_str += f"\n{i}. {x}"
        i += 1
    setButtonsCount(len(ids))
    set_categories_buttons_count(ids)
    await call.message.answer(categories_str, reply_markup=categories_buttons)


@dp.callback_query_handler(text_contains="btn")
async def process_callback_test(call: types.CallbackQuery):
    """"Ловим какой тест был выбран и
    выводим описание"""
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    mycursor = mydb.cursor()
    id = callback_data.replace("action:btn", "")
    mycursor.execute(f"SELECT description FROM chatbot_test.categories WHERE id={id};")
    myresult = ''.join(mycursor.fetchone())
    set_button_pick_options()
    await call.message.answer(myresult, reply_markup=button_pick_options)
    #show_qustion(id)


async def show_qustion(category_id: int):
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT qustion FROM chatbot_test.questions WHERE category_id={id};")
    myresult = mycursor.fetchall()
    i = 1
    qustions = []
    for x in myresult:
        x = ''.join(x)
        qustions.append(f"\n{i}. {x}")
        i += 1


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
