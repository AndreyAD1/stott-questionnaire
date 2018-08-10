from jinja2 import Environment, FileSystemLoader
from livereload import Server
import json
from os.path import join


def render_main_page(jinja_environment):
    template = jinja_environment.get_template('index.html')
    index_html = template.render()
    index_filepath = join('static', 'index.html')
    with open(index_filepath, 'w', encoding='utf-8') as index_file:
        index_file.write(index_html)


def render_person_info_page(jinja_environment):
    template = jinja_environment.get_template('person_info.html')
    person_info_html = template.render()
    person_info_filepath = join('static', 'person_info.html')
    with open(person_info_filepath, 'w') as person_file:
        person_file.write(person_info_html)


def load_questions_and_items():
    with open('items.json', 'r', encoding='utf-8') as item_file:
        items_json = json.load(item_file)
    return items_json


def render_question_pages(jinja_environment, items):
    template = jinja_environment.get_template('_questions.html')
    for subitem_number, subitem in enumerate(items):
        if subitem_number != len(items) - 1:
            next_page_filename = '{}.html'.format(subitem_number + 1)
        else:
            next_page_filename = 'result.html'
        question_html_page = template.render(
            page_content=subitem,
            next_page_filename=next_page_filename
        )
        question_page_filename = '{}.html'.format(subitem_number)
        question_page_filepath = join('static', question_page_filename)
        with open(question_page_filepath, 'w') as question_file:
            question_file.write(question_html_page)


def render_result_page(jinja_environment):
    template = jinja_environment.get_template('result.html')
    result_html = template.render()
    result_filepath = join('static', 'result.html')
    with open(result_filepath, 'w') as result_file:
        result_file.write(result_html)


def render_site():
    questions_and_items = load_questions_and_items()
    env = Environment(loader=FileSystemLoader('templates/'))
    render_main_page(env)
    render_person_info_page(env)
    render_question_pages(env, questions_and_items)
    render_result_page(env)


if __name__ == '__main__':
    render_site()
    server = Server()
    server.watch('templates/', render_site)
    server.watch('static/css/', render_site)
    server.serve(root='static/')
