from app import application


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