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
                          f"Он также показывает характеристики психологического состояния человека")

    pdf.add_page()
    pdf.set_font("DejaVuSerif", "", 14)
    pdf.multi_cell(180, 8, txt="Нижеприведенный комплексный график показывает разнообразие тестов, которые пользователь проходил"
                               "за всё время испорльзования программы MeChecker, и результатов, которые были получены по "
                               "каждому из них. ")

    pdf.image(f"{COMPLEX_PIE_CHART}.png", x=5, y=50, w=200, h=100)

    mycursor = mydb.cursor()
    mycursor.execute(f"select categories.id, categories.category from users "
                    f"INNER JOIN categories_n_grades ON users.user_cat_grades_id = categories_n_grades.id "
                    f"INNER JOIN categories ON categories_n_grades.categories_grades_id = categories.id "
                    f"where users.idTelegram = {id_telegram} "
                    f"group by categories.id, categories.category;")
    myresult = mycursor.fetchall()

    for item in myresult:

    #obj = get_all_result_by_category(int(msg["from"]["id"]), g_id)
    #draw_line_graph(obj["results"], obj["dates"], category_title)

    pdf.output(f"results{cur_date.date()}.pdf", "F")



