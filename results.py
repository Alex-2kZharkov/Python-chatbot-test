from config import mydb
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

    try:
        mycursor = mydb.cursor()
        mycursor.callproc('save_user_procedure', [id_telegram, recom_id, result])
        mydb.commit()

    except mydb.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def draw_pie_chart(current_grade, grade_limit, category_title):

    y = np.array([grade_limit - current_grade, current_grade])
    mylabels = [f"Все баллы: {grade_limit}", f"Набранный балл: {current_grade}"]

    plt.pie(y, labels=mylabels, startangle = 90,colors=["#0E49B5", "#54E346"])
    plt.legend(title=category_title, loc='upper left', bbox_to_anchor=(-0.15, 0.67, 0.5, 0.5))
    plt.savefig('single_test_result.png')
    plt.close()


def draw_line_graph(all_grades, all_dates, category_title):

    plt.figure(figsize=(15, 13))
    plt.plot(all_dates, all_grades, color='#52057b', marker='o', linewidth=3)
    plt.xticks(all_dates, rotation=40, ha='right')
    plt.title(f"{category_title}", fontsize=24)
    plt.xlabel('Дата', fontsize=20)
    plt.ylabel('Результат теста', fontsize=20)
    plt.grid(True)
    plt.savefig('line_graph.png')
    plt.close()


def draw_groupped_chart(all_grades, all_categories):
    # Make data: I have 3 groups and 7 subgroups
    group_names = ['groupA', 'groupB', 'groupC']
    group_size = [12, 11, 30]
    subgroup_names = ['A1', 'A2', 'A.3', 'B.1', 'B.2', 'C.1', 'C.2', 'C.3',
                      'C.4', 'C.5']
    subgroup_names2 = ['Слабовыраженная социофобия: 12', ' выраженная социофобия', 'Умеренный депрессивный эпизод: 13',
                      'социофобия отсутствует', 'социофобия отсутствует', 'социофобия отсутствует',
                      'социофобия отсутствует',
                      'социофобия отсутствует', 'социофобия отсутствует', 'социофобия отсутствует']
    subgroup_size = [4, 3, 5, 6, 5, 10, 5, 5, 4, 6]

    a, b, c = [plt.cm.Blues, plt.cm.Reds, plt.cm.Greens]

    # First Ring (outside)
    fig, ax = plt.subplots()

    ax.axis('equal')
    mypie, _ = ax.pie(group_size, radius=1.3, labels=group_names, textprops={'fontsize': 12}, labeldistance=1.02, colors=
    [a(0.6), b(0.6), c(0.6)])
    plt.setp(mypie, width=0.3, edgecolor='white')

    # Second Ring (Inside)
    mypie2, _ = ax.pie(subgroup_size, radius=1.3 - 0.3,
                       labels=subgroup_names, labeldistance=0.7, colors=[a(0.5), a(0.4),
                                                                         a(0.3), b(0.5), b(0.4), c(0.6), c(0.5), c(0.4),
                                                                         c(0.3), c(0.2)])
    plt.setp(mypie2, width=0.45, edgecolor='white')


    plt.legend(loc=(0.75, 0.8))
    handles, labels = ax.get_legend_handles_labels()
    plt.subplots_adjust(left=-0.35)
    ax.legend(handles[3:], subgroup_names2, loc=(0.78, 0.75),title="Пройдено тестов: 12",title_fontsize=15, prop={"size": 10})

    fig = plt.gcf()
    fig.set_size_inches(16, 9)

    plt.show()
    plt.savefig('complex_pi_chart.png', dpi=150)