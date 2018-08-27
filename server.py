from flask import Flask, render_template, request
import json
from database import (
    add_person_to_database,
    add_behavioral_disorder_symptoms,
    add_person_aptitudes
)


application = Flask(__name__)
application.config.update(ENV='development', DEBUG=True)
with open('items.json', 'r', encoding='utf-8') as item_file:
    item_list = json.load(item_file)


@application.route('/')
def index():
    return render_template('index.html', page_title='Главная')


@application.route('/person_info')
def person_info():
    return render_template(
        'person_info.html',
        page_title='Информация об обследуемом'
    )


@application.route('/questions/<number_of_symptom_complex>', methods=['POST'])
def questions_and_result(number_of_symptom_complex):
    print(request.form)
    page_number = int(number_of_symptom_complex)
    if page_number <= len(item_list):
        if page_number == 1:
            age = int(request.form['age'])
            sex = request.form['sex']
            grade_number = int(request.form['grade'])
            add_person_to_database(age, sex, grade_number)
        if 1 < page_number <= 16:
            add_behavioral_disorder_symptoms()
        if page_number > 16:
            add_person_aptitudes()
        item_index = page_number - 1
        subitem = item_list[item_index]
        total_page_number = len(item_list)
        next_page_name = page_number + 1
        return render_template(
                '_questions.html',
                page_content=subitem,
                page_number=page_number,
                total_page_number=total_page_number,
                next_page_number=next_page_name
            )
    if page_number > len(item_list):
        return render_template('result.html')


if __name__ == '__main__':
    application.run()