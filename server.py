from flask import render_template, request, session
import json
from database import (
    application,
    add_person_to_database,
    add_behavioral_disorder_symptoms,
    add_person_aptitudes
)


application.secret_key = 'SECRET_KEY'
application.config.update(ENV='development', DEBUG=True)
with open('symptoms.json', 'r', encoding='utf-8') as symptom_file:
    symptom_list = json.load(symptom_file)


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
    page_number = int(number_of_symptom_complex)
    if page_number <= len(symptom_list):
        if page_number == 1:
            age = int(request.form['age'])
            sex = request.form['sex']
            grade_number = int(request.form['grade'])
            person_info_id = add_person_to_database(age, sex, grade_number)
            session['person_info_id'] = person_info_id
        if 1 < page_number <= 16:
            add_behavioral_disorder_symptoms(
                session['person_info_id'],
                request.form
            )
        if page_number > 16:
            add_person_aptitudes()
        symptom_index = page_number - 1
        symptom_complex = symptom_list[symptom_index]
        total_page_number = len(symptom_list)
        next_page_name = page_number + 1
        return render_template(
                '_questions.html',
                page_content=symptom_complex,
                page_number=page_number,
                total_page_number=total_page_number,
                next_page_number=next_page_name
            )
    if page_number > len(symptom_list):
        return render_template('result.html')


if __name__ == '__main__':
    application.run()