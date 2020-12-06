from fpdf import FPDF
from config import mydb
from datetime import datetime
from config import SIMPLE_PIE_CHART
from config import COMPLEX_PIE_CHART
from main import get_all_result_by_category
from results import draw_line_graph

def create_pdf(id_telegram, total_grade, grade_limit, recomendation):
    cur_date = datetime.now()

    string = f"Помните, что чем ниже количество набранных баллов" \
             f",тем меньше уровень того или инного растройства.\nВы набрали {total_grade} из {grade_limit} баллов. \n" \
             f"Таким образом, y Вас {recomendation}"

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVuSerif', '', '/Users/alex/Library/Fonts/DejaVuSerif.ttf', uni=True)
    pdf.add_font('DejaVuSerif-Bold', '', '/Users/alex/Library/Fonts/DejaVuSerif-Bold.ttf', uni=True)

    pdf.set_font('DejaVuSerif-Bold', '', 16)
    pdf.cell(40, 10, f"{cur_date.strftime('%m/%d/%Y, %H:%M')}",ln=1)

    pdf.set_font("DejaVuSerif", "", 14)
    pdf.multi_cell(180, 8, txt=string)

    pdf.set_font("DejaVuSerif", "", 14)
    pdf.multi_cell(150, 9, f"\nНиже приведены графики, которые помогут Вам лучше понять и увидеть результаты текущего и предыдуших тестов")

    pdf.image(f"{SIMPLE_PIE_CHART}.png", x=5, y=110, w=220, h=120)


    pdf.set_font("DejaVuSerif", "", 14)
    pdf.set_y(230)
    pdf.multi_cell(170, 9,f"Вышеизображенный круговой график демонстрирует зависимость полученного балла от предельной величины баллов. "
                          f"Иначе говоря, посмотрев на него Вы поймете: насколько всё хорошо или плохо")

    pdf.add_page()
    pdf.set_font("DejaVuSerif", "", 14)
    pdf.multi_cell(180, 8, txt="Нижеприведенный комплексный график показывает разнообразие тестов, которые пользователь проходил "
                               "за всё время использования программы MeChecker, и результатов, которые были получены по "
                               "каждому из них. Он позволит Вам оценить эмоциональное состояние, в котором Вы преимущественно находились"
                               "и находитесь прямо сейчас")

    pdf.image(f"{COMPLEX_PIE_CHART}.png", x=5, y=55, w=200, h=100)

    mycursor = mydb.cursor()
    mycursor.execute(f"select categories.id, categories.category from users "
                    f"INNER JOIN categories_n_grades ON users.user_cat_grades_id = categories_n_grades.id "
                    f"INNER JOIN categories ON categories_n_grades.categories_grades_id = categories.id "
                    f"where users.idTelegram = {id_telegram} "
                    f"group by categories.id, categories.category;")
    myresult = mycursor.fetchall()

    categories_object = {}
    for item in myresult:
        categories_object[item[1]] = item[0]

    print(categories_object)

    for property in categories_object:

        obj = get_all_result_by_category(id_telegram, categories_object[property])
        draw_line_graph(obj["results"], obj["dates"], property)

        pdf.add_page()
        pdf.set_font("DejaVuSerif", "", 14)
        pdf.multi_cell(180, 8,
                       txt=f"Нижеприведенный график показывает зависимость всех результатов, полученных в ходе прохождения теста - '{property}', "
                           f"от времени прохождения теста.\nБлагодаря ему легко визуализировать"
                           f" динамику психологического состояния человека. Приглядитесь к нему внимательно, вспомните недавние события, "
                           f"и Вы поймете, что улучшило Ваше психологическое состояние, а что - нет. Придерживайтесь этой тактики"
                           f", потому что именно она поможет Вам в долгосрочной перспективе!")

        pdf.image(f"{property}.png", x=5, y=100, w=200, h=150)


    pdf.output(f"results{cur_date.date()}.pdf", "F")
    return f"results{cur_date.date()}.pdf"
