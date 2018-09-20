from jinja2 import Environment, FileSystemLoader
from livereload import Server
import json
from os.path import join


def render_pages_without_variables(jinja_environment, page_list):
    for page in page_list:
        template = jinja_environment.get_template(page['page_name'])
        page_html = template.render(page_title=page['page_title'])
        page_filepath = join('static', page['page_name'])
        with open(page_filepath, 'w', encoding='utf-8') as page_file:
            page_file.write(page_html)


def load_questions_and_items():
    with open('symptoms.json', 'r', encoding='utf-8') as item_file:
        items_json = json.load(item_file)
    return items_json


def render_question_pages(jinja_environment, items):
    template = jinja_environment.get_template('_questions.html')
    for subitem_index, subitem in enumerate(items):
        page_number = subitem_index + 1
        total_page_number = len(items)
        if page_number < total_page_number:
            next_page_filename = '{}.html'.format(page_number + 1)
        if page_number == total_page_number:
            next_page_filename = 'result.html'
        question_html_page = template.render(
            page_content=subitem,
            next_page_filename=next_page_filename,
            page_number=page_number,
            total_page_number=total_page_number
        )
        page_filename = '{}.html'.format(page_number)
        question_page_filepath = join('static', page_filename)
        with open(question_page_filepath, 'w') as question_file:
            question_file.write(question_html_page)


def render_result_page(jinja_environment):
    template = jinja_environment.get_template('result.html')
    result_html = template.render()
    result_filepath = join('static', 'result.html')
    with open(result_filepath, 'w') as result_file:
        result_file.write(result_html)


def render_site():
    pages_without_vatiables = [
        {'page_name': 'index.html', 'page_title': 'Главная'},
        {
            'page_name': 'person_info.html',
            'page_title': 'Информация об обследуемом'
        },
        {'page_name': 'instruction.html', 'page_title': 'Инструкция'}
    ]
    questions_and_items = load_questions_and_items()
    env = Environment(loader=FileSystemLoader('templates/'))
    render_pages_without_variables(env, pages_without_vatiables)
    render_question_pages(env, questions_and_items)
    render_result_page(env)


if __name__ == '__main__':
    render_site()
    server = Server()
    server.watch('templates/', render_site)
    server.watch('static/css/', render_site)
    server.serve(root='static/')
