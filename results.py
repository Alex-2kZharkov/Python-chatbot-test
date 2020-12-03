from config import mydb
import matplotlib.pyplot as plt
import numpy as np

def get_answers_grades(category_id):
    answers = []
    grades = []

    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT answer,emoji, grade FROM chatbot_test.answers WHERE answer_category_id={category_id};")
    myresult = mycursor.fetchall()

    for item in myresult:
        answers.append(f"{item[0]}{item[1]}")
        grades.append(item[2])

    return {"answers": answers, "grades": grades}


def count_answers_grade(category_id, answers_obj):

    answers_n_grades = get_answers_grades(category_id)
    answers = answers_n_grades["answers"]
    grades = answers_n_grades["grades"]
    total_grade = 0

    for i in range(len(answers)):
        total_grade += answers_obj[answers[i]] * grades[i] # количество ответов конкретного типа * бал за один такой ответ

    return total_grade


def define_recomendation(category_id, total_grade):

    mycursor = mydb.cursor()
    mycursor.execute(f"select categories_n_grades.id, categories_n_grades.recomendation_text, grades_scope.grade, categories_n_grades.gif from categories_n_grades  INNER JOIN grades_scope ON categories_n_grades.grades_id=grades_scope.id where categories_n_grades.categories_grades_id={category_id};")
    myresult = mycursor.fetchall()
    grade_limit = 0
    flag = True
    obj = None

    for item in myresult:
        if grade_limit < int(item[2]):
            grade_limit = int(item[2])

        if flag and total_grade <= item[2]:
            flag = False
            obj = {
                "recom_id": item[0],
                "recommendation": item[1],
                "gif": item[3]
            }
    obj["grade_limit"] = grade_limit
    return obj

def save_user_results(id_telegram, recom_id, result):
    mycursor = mydb.cursor()
    mycursor.execute(f"INSERT INTO chatbot_test.users (idTelegram, user_cat_grades_id, result, date) VALUES({id_telegram}, {recom_id}, {result}, curdate())")
    mydb.commit()


def draw_pie_chart(current_grade, grade_limit, category_title):

    y = np.array([grade_limit - current_grade, current_grade])
    mylabels = [f"Все баллы: {grade_limit}", f"Набранный балл: {current_grade}"]

    plt.pie(y, labels=mylabels, startangle = 90,colors=["#0E49B5", "#54E346"])
    plt.legend(title=category_title, loc='upper left', bbox_to_anchor=(-0.15, 0.67, 0.5, 0.5))
    plt.savefig('single_test_result.png')


def draw_line_graph(all_grades, all_dates, category_title):
    Year = [30, 40, 60, 20]
    Unemployment_Rate = ['01-12-2020', '02-12-2020', '12-12-2020', '31-12-2020']

    plt.plot(Unemployment_Rate, Year, color='#0E49B5', marker='o')
    plt.title('Зависимость результатов теста от даты', fontsize=18)
    plt.xlabel('Дата', fontsize=16)
    plt.ylabel('Результат теста', fontsize=16)
    plt.grid(True)
    plt.show()