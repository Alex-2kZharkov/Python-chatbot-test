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

def get_subcategories(category_id): # для простой круговой диаграммы нужны подкатегории и их оценки
    mycursor = mydb.cursor()
    mycursor.execute(f"select grades_scope.grade_title, grades_scope.grade from categories_n_grades "
        f"INNER JOIN grades_scope ON categories_n_grades.grades_id = grades_scope.id "
        f"where categories_n_grades.categories_grades_id ={category_id};")
    myresult = mycursor.fetchall()
    titles = []
    grades = []

    for item in myresult:
        titles.append(item[0])
        grades.append(item[1])

    return {
        "titles": titles,
        "grades": grades
    }


def reformat_grades(grades): #сделать строки с оценками типо 0-15, 15-30 и тд

    result_array = []
    str = None
    for i in range(len(grades)):
        if i == 0:
            str = f"0 - {grades[i]}"
        else:
            str = f"{grades[i - 1]} - {grades[i]}"
        result_array.append(str)

    return result_array

def draw_pie_chart(grade_limit, current_grade, subgroup_names2, subgroup_size, category_title):


    colors = [(1, 0.71, 0), (0, 0.59, 0.95)] # синий и жедтый цвета
    group_names = [f"Все баллы: {grade_limit}", f"Набранный балл: {current_grade}"]

    subgroup_names = reformat_grades(subgroup_size)
    sub_colors = []
    legend_labels = []

    average_opacity = round(float(1 / (len(subgroup_size) + 1)), 2)
    current_opacity = average_opacity

    for j in range(len(subgroup_size)): #оттенки цветов
        sub_colors.insert(0 , (1, 0.6, 0) + (round(1 - current_opacity, 2),))
        current_opacity += average_opacity

    for i in range(len(subgroup_names2)): #склеивает заголовок + баллы
        legend_labels.append(f"{subgroup_names2[i]}: {subgroup_names[i]}")


    for i in range(len(subgroup_size) - 1, 0, -1): #нужно минусовать предыдущий баллы, типо 60-30, 30-25 и тд
        if i > 0:
            subgroup_size[i] = subgroup_size[i] - subgroup_size[i - 1]

    # First Ring (outside)
    fig, ax = plt.subplots()
    ax.axis('equal')

    mypie, _ = ax.pie([grade_limit-current_grade, current_grade], radius=1.3, labels=group_names, textprops={'fontsize': 12}, labeldistance=1.03,
                      colors=colors, startangle=90)
    plt.setp(mypie, width=0.35, edgecolor='white')

    # Second Ring (Inside)
    mypie2, _ = ax.pie(subgroup_size, radius=1.3 - 0.35, labels=subgroup_names, labeldistance=0.7, textprops = dict(rotation_mode = 'anchor', va='center', ha='center'), colors=sub_colors, startangle=90, counterclock=False)
    plt.setp(mypie2, width=0.45, edgecolor='white')

    plt.legend(loc=(0.75, 0.8))
    handles, labels = ax.get_legend_handles_labels()
    plt.subplots_adjust(left=-0.30)
    ax.legend(handles[2:], legend_labels, loc=(0.72, 0.90), title=category_title,
              title_fontsize=13, prop={"size": 12})

    fig = plt.gcf()
    fig.set_size_inches(15, 8)

    plt.show()
    plt.savefig('single_test_result.png', dpi=150)


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


def draw_complex_pie_chart(group_names, group_size, subgroup_names2, subgroup_size, colors, sub_category_numbers,  total_times):
    # Make data: I have 3 groups and 7 subgroups

    subgroup_names = []
    for i in range(len(subgroup_names2)):
        subgroup_names.append(" ")

    sub_colors = calculate_sub_colors(sub_category_numbers, colors)
    group_names = break_category_titles(group_names)


    for i in range(len(group_names)): #добавить количество тестов
        group_names[i] = group_names[i][0: ] + f": {group_size[i]}"


    for i in range(len(subgroup_names2)):
        subgroup_names2[i] = subgroup_names2[i][0: ] + f": {subgroup_size[i]}"

    # First Ring (outside)
    fig, ax = plt.subplots()
    ax.axis('equal')

    mypie, _ = ax.pie(group_size, radius=1.3, labels=group_names, textprops={'fontsize': 12}, labeldistance=1.03, colors=colors)
    plt.setp(mypie, width=0.3, edgecolor='white')

    # Second Ring (Inside)
    mypie2, _ = ax.pie(subgroup_size, radius=1.3 - 0.3, labels=subgroup_names, labeldistance=0.7, colors=sub_colors)
    plt.setp(mypie2, width=0.45, edgecolor='white')


    plt.legend(loc=(0.75, 0.8))
    handles, labels = ax.get_legend_handles_labels()
    plt.subplots_adjust(left=-0.10)
    ax.legend(handles[3:], subgroup_names2, loc=(0.87, 0.78),title=f"Пройдено тестов: {total_times}",title_fontsize=15, prop={"size": 12})

    fig = plt.gcf()
    fig.set_size_inches(17, 9)

    plt.show()
    plt.savefig('complex_pi_chart.png', dpi=150)


def break_category_titles(category_titles): #разбивает категорию на две строки, если она длиннее 4 слов

    for i in range(len(category_titles)):
        counter = 0
        for j in range(len(category_titles[i])):

            if category_titles[i][j] == " ":
                counter += 1

            if counter == 4:
                category_titles[i] = category_titles[i][0: j] + "\n" + category_titles[i][j:]
                break

    return category_titles


def calculate_sub_colors(group_size, colors): #создается масссив кортежей с цветами подкругов
    sub_colors = []

    for i in range(len(colors)):

        average_opacity = round(float(1 / (group_size[i] + 1)), 2)
        current_opacity = average_opacity

        for j in range(group_size[i]):
            if j < group_size[i]:
                sub_colors.append(colors[i] + (round(1 - current_opacity, 2),))
                current_opacity += average_opacity

    return sub_colors

