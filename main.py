import json
import logging
from config import API_TOKEN
from config import mydb
from aiogram import Bot, Dispatcher, executor, types
from buttons import *


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

g_id = None
user_answers = {}
questions = []
gifs = []
current_question = 0

def reinit_used_variables():
    global g_id, user_answers, questions, gifs, current_question
    g_id = None
    user_answers = {}
    questions = []
    gifs = []
    current_question = 0


@dp.message_handler(commands=['start', 'help'])
@dp.message_handler(text="Пройти другие тесты 🤩")
async def send_welcome(message: types.CallbackQuery):

    await message.answer(
        "Добро пожаловать в MeChecker.\nMeChecker поможет Вам определить уровень тревоги, наличие депрессии, "
        "а также даст несколько советов о том, как привести дела в порядок. \nПомните, что оффлайн врача не заменит"
        " ни один онлайн бот, поэтому обязательно проконсультируйтесь с психологом или психотерапевтом.", reply_markup=ReplyKeyboardRemove())

    await message.answer_sticker("https://i.pinimg.com/originals/2f/87/31/2f8731b100b9e121962f72fb712c9799.gif", "",
                                 reply_markup=button_start)


@dp.callback_query_handler(text_contains='start')
@dp.callback_query_handler(text_contains='change_test')
async def process_callback_start(call: types.CallbackQuery):
    await call.answer(cache_time=500)
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
    await call.message.edit_reply_markup(reply_markup='')


def set_id(p_id: int):
    global g_id
    g_id = p_id


def init_user_answers(answers):
    for a in answers:
        user_answers[a] = 0


@dp.callback_query_handler(text_contains="btn")
async def process_callback_test(call: types.CallbackQuery):
    """"Ловим какой тест был выбран и
    выводим описание"""
    await call.answer(cache_time=500)
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    mycursor = mydb.cursor()
    id = callback_data.replace("action:btn", "")
    mycursor.execute(f"SELECT description FROM chatbot_test.categories WHERE id={id};")
    myresult = ''.join(mycursor.fetchone())
    set_button_pick_options()
    set_id(id)
    await call.message.answer(myresult, reply_markup=button_pick_options)
    await call.message.edit_reply_markup(reply_markup='')


"""///////////////////////////////////////////////////////////////////////"""
@dp.callback_query_handler(text_contains="go_test")
async def process_callback_start_test(call: types.CallbackQuery):
    await call.answer(cache_time=500)
    await call.message.edit_reply_markup(reply_markup='')
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT answer FROM chatbot_test.answers WHERE answer_category_id={g_id};")
    myresult = mycursor.fetchall()
    answers_arr = []
    for x in myresult:
        x = ''.join(x)
        answers_arr.append(x)

    set_reply_keyboard(answers_arr)
    init_user_answers(answers_arr)
    await get_questions(g_id)

    await call.message.answer(show_question(), reply_markup=answers_buttons)
    await call.message.answer_sticker(gifs[current_question], "")


def show_question():
    return f"{current_question + 1} из {len(questions)}.\n{questions[current_question]}"


@dp.message_handler()
async def process_answer(msg: types.Message):
    global categories_buttons_count, current_buttons_number, is_options_buttons_shown, categories_buttons
    global button_pick_options, answers_buttons, start_again_button
    if msg.text in user_answers.keys():
        global current_question
        if current_question < len(questions)-1:
            user_answers[msg.text] += 1
            current_question += 1
            await msg.answer(show_question())
            await msg.answer_sticker(gifs[current_question], "")
        else:
            reinit_used_variables()

            await msg.answer("Конец теста!", reply_markup=start_again_button)
            # вывести результаты
            # забить все писпользованные переменные

    else:
        await msg.answer("Вы не выбрали один из предложенных ответов!")


async def get_questions(category_id: int):
    global questions, gifs
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT qustion, gif_address FROM chatbot_test.questions WHERE category_id={category_id};")
    myresult = mycursor.fetchall()

    for x in myresult:
        x = ''.join(x)
        gif_start = x.find("http") # в одной строке и вопрос и адрес, поэтому ищу начало адреса картинки
        gif_address = x[gif_start:] # срез адреса
        x = x[:gif_start] # срез от начала вопроса до адреса картинки

        questions.append(x)
        gifs.append(gif_address)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
