import base64
from flask import render_template, session, request
from app import application, symptom_list, aptitude_list, csrf
from app.db_models import (
    add_person_to_database,
    add_symptoms_to_database,
    add_aptitudes_to_database,
    get_symptoms_from_database,
    get_aptitudes_from_database
)
from app.constants import (
    FIRST_FORM_PAGE,
    FIRST_APTITUDE_PAGE,
    TOTAL_NUM_OF_FORM_PAGES,
    RESULT_PAGE
)
from app.get_results import (
    get_points_per_symptom_complex,
    format_aptitude_names
)
from app.figure import get_result_figure


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


@application.route('/questions/result_criteria')
def result_criteria():
    return render_template(
        'result_criteria.html',
        page_title='Инструкция по заполнению анкеты'
    )


@application.route('/questions/<number_of_symptom_complex>', methods=['POST'])
def questions_and_result(number_of_symptom_complex):
    page_number = int(number_of_symptom_complex)
    _process_user_input(page_number, request)

    if page_number < RESULT_PAGE:
        return _get_next_form_page(page_number)

    if page_number == RESULT_PAGE:
        person_info_id = session['person_info_id']
        if not session['info_saved_in_database']:
            add_symptoms_to_database(person_info_id, session['symptom_list'])
            add_aptitudes_to_database(person_info_id, session['aptitude_list'])
            session['info_saved_in_database'] = True
        return _get_result_page(person_info_id)

    return render_template('index.html', page_title='Главная')


@application.route('/questions/result')
def render_result_page():
    person_info_id = session.get('person_info_id', None)
    if person_info_id is None:
        return render_template('index.html', page_title='Главная')
    return _get_result_page(person_info_id)


def _get_input_info(input_dict):
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


def _add_checked_items_to_session(input_items: dict, items_type: str):
    for item in input_items:
        if item == 'csrf_token':
            continue

        if item == 'другое':
            item = input_items[item]
            if not item:
                continue

        if item not in session[items_type]:
            session[items_type].append(item)
            session.modified = True


def _process_person_info_form(request):
    input_info = _get_input_info(request.form)
    person_info_id = add_person_to_database(**input_info)
    session['person_info_id'] = person_info_id
    session['symptom_list'] = []
    session['aptitude_list'] = []
    session['info_saved_in_database'] = False


def _process_user_input(page_number, request):
    if page_number == FIRST_FORM_PAGE:
        _process_person_info_form(request)

    if FIRST_FORM_PAGE < page_number <= FIRST_APTITUDE_PAGE:
        input_symptoms = request.form
        _add_checked_items_to_session(input_symptoms, 'symptom_list')

    if page_number > FIRST_APTITUDE_PAGE:
        input_aptitudes = request.form
        _add_checked_items_to_session(input_aptitudes, 'aptitude_list')


def _get_next_form_page(page_number):
    if page_number < FIRST_APTITUDE_PAGE:
        template_name = 'questions.html'
        page_content = symptom_list[page_number - 1]
    else:
        template_name = 'aptitudes.html'
        page_content = aptitude_list[page_number - FIRST_APTITUDE_PAGE]
    next_page_name = page_number + 1
    return render_template(
        template_name,
        page_content=page_content,
        page_number=page_number,
        total_page_number=TOTAL_NUM_OF_FORM_PAGES,
        next_page_number=next_page_name
    )


def _get_result_page(person_info_id):
    matched_symptoms = get_symptoms_from_database(person_info_id)
    matched_aptitudes = get_aptitudes_from_database(person_info_id)
    symptom_scores = get_points_per_symptom_complex(
        symptom_list,
        matched_symptoms
    )
    formatted_aptitudes = format_aptitude_names(matched_aptitudes)
    buffered_image = get_result_figure(symptom_scores)
    decoded_image = base64.b64encode(buffered_image.getvalue()).decode(
        'utf-8'
    )
    return render_template(
        'result.html',
        symptom_scores=symptom_scores,
        aptitudes=formatted_aptitudes,
        image=str(decoded_image)
    )