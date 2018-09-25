from flask import render_template, request, session
import json
from database import (
    application,
    add_person_to_database,
    add_symptoms_to_database,
    add_aptitudes_to_database,
    get_symptoms_from_database,
    get_aptitudes_from_database
)
from get_results import get_points_per_symptom_complex, get_aptitude_names


FIRST_FORM_PAGE = 1
FIRST_APTITUDE_PAGE = 17
TOTAL_NUM_OF_FORM_PAGES = 18
RESULT_PAGE = 19


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
    if page_number == FIRST_FORM_PAGE:
        age = int(request.form['age'])
        sex = request.form['sex']
        grade_number = int(request.form['grade'])
        person_info_id = add_person_to_database(age, sex, grade_number)
        session['person_info_id'] = person_info_id
        session['symptom_list'] = []
        session['aptitude_list'] = []
    if FIRST_FORM_PAGE < page_number <= FIRST_APTITUDE_PAGE:
        input_symptoms = request.form.keys()
        for input_symptom in input_symptoms:
            session['symptom_list'].append(input_symptom)
            session.modified = True
    if page_number > FIRST_APTITUDE_PAGE:
        input_aptitudes = request.form.keys()
        for aptitude in input_aptitudes:
            session['aptitude_list'].append(aptitude)
            session.modified = True
    if page_number < RESULT_PAGE:
        symptom_index = page_number - 1
        symptom_complex = symptom_list[symptom_index]
        next_page_name = page_number + 1
        return render_template(
                '_questions.html',
                page_content=symptom_complex,
                page_number=page_number,
                total_page_number=TOTAL_NUM_OF_FORM_PAGES,
                next_page_number=next_page_name
            )
    if page_number == RESULT_PAGE:
        add_symptoms_to_database(
            session['person_info_id'],
            session['symptom_list']
        )
        add_aptitudes_to_database(
            session['person_info_id'],
            session['aptitude_list']
        )
        matched_symptoms = get_symptoms_from_database(
            session['person_info_id']
        )
        aptitude_numbers = get_aptitudes_from_database(
            session['person_info_id']
        )
        symptom_scores = get_points_per_symptom_complex(
            symptom_list,
            matched_symptoms
        )
        aptitude_names = get_aptitude_names(symptom_list, aptitude_numbers)
        return render_template(
            'result.html',
            symptom_scores=symptom_scores,
            aptitudes=aptitude_names
        )


if __name__ == '__main__':
    application.run()