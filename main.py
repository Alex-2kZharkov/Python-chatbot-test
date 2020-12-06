import json
import logging
from config import API_TOKEN
from config import mydb
from aiogram import Bot, Dispatcher, executor, types
from buttons import *
from results import *
from PIL import Image
import requests

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

g_id = None
user_answers = {}
questions = []
gifs = []
current_question = 0
global_reply_keyboard = None
total_grade = None
grade_information = None

def reinit_used_variables():
    global g_id, user_answers, questions, gifs, current_question, global_reply_keyboard, total_grade, grade_information
    g_id = None
    user_answers = {}
    questions = []
    gifs = []
    current_question = 0
    global_reply_keyboard = None
    total_grade = None
    grade_information = None


@dp.message_handler(commands=['start', 'help'])
@dp.message_handler(text="Пройти другие тесты 🤩")
async def send_welcome(message: types.CallbackQuery):
    reinit_used_variables()
    await message.answer(
        "Добро пожаловать в MeChecker.\nMeChecker поможет Вам определить уровень тревоги, наличие депрессии, "
        "а также даст несколько советов о том, как привести дела в порядок. Помните, что оффлайн врача не заменит"
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
    global global_reply_keyboard

    await call.answer(cache_time=500)
    await call.message.edit_reply_markup(reply_markup='')
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT answer, emoji FROM chatbot_test.answers WHERE answer_category_id={g_id};")
    myresult = mycursor.fetchall()
    answers_arr = []
    for x in myresult:
        x = ''.join(x)
        answers_arr.append(x)

    global_reply_keyboard = set_reply_keyboard(answers_arr)
    init_user_answers(answers_arr)
    get_questions(g_id)

    await call.message.answer(show_question(), reply_markup=global_reply_keyboard)
    await call.message.answer_sticker(gifs[current_question], "")


def show_question():
    return f"{current_question + 1} из {len(questions)}.\n{questions[current_question]}"


@dp.message_handler()
async def process_answer(msg: types.Message):

    global categories_buttons_count, current_buttons_number, is_options_buttons_shown, categories_buttons
    global button_pick_options, answers_buttons, start_again_button, total_grade, grade_information

    if msg.text in user_answers.keys():
        global current_question

        user_answers[msg.text] += 1

        if current_question < len(questions)-1:
            current_question += 1
            await msg.answer(show_question())
            await msg.answer_sticker(gifs[current_question], "")
        else:

            total_grade = count_answers_grade(g_id, user_answers)
            grade_information = define_recomendation(g_id, total_grade)
            save_user_results(int(msg["from"]["id"]), g_id, int(total_grade), int(grade_information["recom_id"]))

            subcategories = get_subcategories(g_id)
            category_title = get_category_title(g_id)


            draw_pie_chart(grade_information['grade_limit'] , total_grade, subcategories["titles"], subcategories["grades"], category_title)


            obj = get_all_result_by_category(int(msg["from"]["id"]), g_id)
            draw_line_graph(obj["results"], obj["dates"], category_title)
            get_data_for_complex_chart(int(msg["from"]["id"]))

            string = f"Помните, что чем ниже количество набранных баллов" \
                  f", тем меньше уровень того или инного растройства.\nВы набрали {total_grade} из {grade_information['grade_limit']} баллов. \n" \
                  f"Таким образом, y Вас {grade_information['recommendation']}"

            await msg.answer(string, reply_markup=start_again_button)
            await msg.answer_sticker(grade_information["gif"], "")

            with open('single_test_result.png', 'rb') as photo:
                await msg.answer_photo(photo, caption="Графическая интерпретация результатов текущего теста")

            res_string = "Графическая интерпретация всех результатов выбранного теста"

            if len(obj["results"]) < 2:
                res_string += "(в данный момент тест пройден один раз, поэтому на графике показана только начальная точка)"

            with open('line_graph.png', 'rb') as photo:
                await msg.answer_photo(photo, caption=res_string)

            with open('complex_pi_chart.png', 'rb') as photo:
                await msg.answer_photo(photo, caption="Графическая интерпретация общего количества тестов")


    else:
        await msg.answer("Я Вас не понимаю🙄")


def get_data_for_complex_chart(id_telegram):
    mycursor = mydb.cursor()
    mycursor.execute(f"select categories.category, grades_scope.grade_title, COUNT(grades_scope.grade_title) as count, categories.rgb from users "
        f"INNER JOIN categories_n_grades ON users.user_cat_grades_id = categories_n_grades.id "
        f"INNER JOIN categories ON categories_n_grades.categories_grades_id = categories.id "
        f"INNER JOIN grades_scope ON categories_n_grades.grades_id = grades_scope.id "
        f"where users.idTelegram = '706466022' "
        f"GROUP BY categories.category, grades_scope.grade_title, categories.rgb  ORDER BY categories.category;")

    myresult = mycursor.fetchall()
    total_times = 0
    category_titles_array = []
    category_titles_counts = []
    category_titles_obj = []
    sub_category_numbers = []
    grade_titles = []
    grades = []
    colors = []

    for row in myresult: #разделяет данные
        category_titles_obj.append(row[0])
        grade_titles.append(row[1])
        grades.append(row[2])
        total_times += int(row[2])
        colors.append(row[3])

    category_titles_obj = dict.fromkeys(category_titles_obj)
    colors = list(dict.fromkeys(colors))

    for property in category_titles_obj:
        count = 0
        for row in myresult:
            if property == row[0]:
                count +=1
        sub_category_numbers.append(count)

    for property in category_titles_obj: #считает количество прохождений для каждой категории
        for row in myresult:
            if property == row[0]:
                if category_titles_obj[property] is None:
                    category_titles_obj[property] = 0 + row[2]
                else:
                    category_titles_obj[property] += row[2]

    for property in category_titles_obj: #разделили на массив категорий и массив количества каждой из них
        category_titles_array.append(property)
        category_titles_counts.append(category_titles_obj[property])

    colors = recalculate_colors(colors) #пересчитывает цифры rgb по пропорции и получает массив кортежей-tuple
    draw_complex_pie_chart(category_titles_array, category_titles_counts, grade_titles, grades, colors, sub_category_numbers, total_times)


def recalculate_colors(colors):
    for i in range(len(colors)):
        a_list = colors[i].split(",")
        colors[i] = list(map(int, a_list))

    for i in range(len(colors)):
        temp_array = []
        for item in colors[i]:
            temp_array.append(round(float(item / 255), 2))
        colors[i] = tuple(temp_array)

    return colors


def get_all_result_by_category(id_telegram, g_id):
    dates = []
    results = []

    mycursor = mydb.cursor()
    mycursor.execute(f"select users.result, users.date from users "
                     f"INNER JOIN categories_n_grades ON users.user_cat_grades_id = categories_n_grades.id "
                     f"where categories_n_grades.categories_grades_id = {g_id} and users.idTelegram = {id_telegram} ORDER  BY  users.date")
    myresult = mycursor.fetchall()

    for x in myresult:
        results.append(x[0])
        dates.append(x[1].strftime("%d-%m-%Y"))

    return {
        "results": results,
        "dates": dates
    }

def get_questions(category_id: int):
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

def get_category_title(id):
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT category FROM chatbot_test.categories where id={g_id}")
    category_title = mycursor.fetchone()
    return ''.join(category_title)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
