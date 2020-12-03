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
        print(f"\n{answers_obj[answers[i]]}")
        total_grade += answers_obj[answers[i]] * grades[i] # количество ответов конкретного типа * бал за один такой ответ

    return total_grade




