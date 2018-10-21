import base64
import json
from flask import render_template, request, session
from flask_wtf.csrf import CSRFProtect
from database import (
    application,
    add_person_to_database,
    add_symptoms_to_database,
    add_aptitudes_to_database,
    get_symptoms_from_database,
    get_aptitudes_from_database
)
from get_results import get_points_per_symptom_complex, format_aptitude_names
from figure import get_result_figure


FIRST_FORM_PAGE = 1
FIRST_APTITUDE_PAGE = 17
TOTAL_NUM_OF_FORM_PAGES = 18
RESULT_PAGE = 19


application.secret_key = 'SECRET_KEY'
csrf = CSRFProtect(application)
application.config.update(ENV='development', DEBUG=True)

with open('symptoms.json', 'r', encoding='utf-8') as symptom_file:
    symptom_list = json.load(symptom_file)
with open('aptitudes.json', 'r', encoding='utf-8') as aptitude_file:
    aptitude_list = json.load(aptitude_file)


@application.route('/')
def index():
    return render_template('index.html', page_title='Главная')


@application.route('/person_info')
def person_info():
    return render_template(
        'person_info.html',
        page_title='Информация об обследуемом'
    )


@application.route('/questions/instruction')
def instruction():
    return render_template(
        'instruction.html',
        page_title='Инструкция по заполнению анкеты'
    )


def get_input_info(input_dict):
    argument_dict = {}
    for key, value in input_dict.items():
        if key == 'csrf_token':
            continue
        if not value:
            value = None
            argument_dict[key] = value
            continue
        if key in ['age', 'grade', 'child_number', 'order_number']:
            value = int(value)
        argument_dict[key] = value
    return argument_dict


def add_checked_items_to_session(input_items: dict, items_type: str):
    for item in input_items:
        if item == 'другое':
            item = input_items[item]
            if not item:
                continue
        if item not in session[items_type] and item != 'csrf_token':
            session[items_type].append(item)
            session.modified = True


@application.route('/questions/<number_of_symptom_complex>', methods=['POST'])
def questions_and_result(number_of_symptom_complex):
    page_number = int(number_of_symptom_complex)
    if page_number == FIRST_FORM_PAGE:
        input_info = get_input_info(request.form)
        person_info_id = add_person_to_database(**input_info)
        session['person_info_id'] = person_info_id
        session['symptom_list'] = []
        session['aptitude_list'] = []
        session['info_saved_in_database'] = False
    if FIRST_FORM_PAGE < page_number <= FIRST_APTITUDE_PAGE:
        input_symptoms = request.form
        add_checked_items_to_session(input_symptoms, 'symptom_list')
    if page_number > FIRST_APTITUDE_PAGE:
        input_aptitudes = request.form
        add_checked_items_to_session(input_aptitudes, 'aptitude_list')
    if page_number < FIRST_APTITUDE_PAGE:
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
    if FIRST_APTITUDE_PAGE <= page_number < RESULT_PAGE:
        next_page_name = page_number + 1
        aptitude_page_index = page_number - FIRST_APTITUDE_PAGE
        aptitudes = aptitude_list[aptitude_page_index]
        return render_template(
                '_aptitudes.html',
                page_content=aptitudes,
                page_number=page_number,
                total_page_number=TOTAL_NUM_OF_FORM_PAGES,
                next_page_number=next_page_name
            )
    if page_number == RESULT_PAGE:
        if not session['info_saved_in_database']:
            add_symptoms_to_database(
                session['person_info_id'],
                session['symptom_list']
            )
            add_aptitudes_to_database(
                session['person_info_id'],
                session['aptitude_list']
            )
            session['info_saved_in_database'] = True
        matched_symptoms = get_symptoms_from_database(
            session['person_info_id']
        )
        matched_aptitudes = get_aptitudes_from_database(
            session['person_info_id']
        )
        symptom_scores = get_points_per_symptom_complex(
            symptom_list,
            matched_symptoms
        )
        formatted_aptitudes = format_aptitude_names(matched_aptitudes)
        buffered_image = get_result_figure(symptom_scores)
        decoded_image = base64.b64encode((buffered_image.getvalue())).decode('utf-8')
        return render_template(
            'result.html',
            symptom_scores=symptom_scores,
            aptitudes=formatted_aptitudes,
            image=str(decoded_image)
        )


if __name__ == '__main__':
    application.run()