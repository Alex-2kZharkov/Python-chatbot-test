from config import mydb

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

