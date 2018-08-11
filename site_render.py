from jinja2 import Environment, FileSystemLoader
from livereload import Server
import json
from os.path import join


def render_pages_without_variables(jinja_environment):
    page_name_list = ['index.html', 'person_info.html']
    for page_name in page_name_list:
        template = jinja_environment.get_template(page_name)
        page_html = template.render()
        page_filepath = join('static', page_name)
        with open(page_filepath, 'w', encoding='utf-8') as page_file:
            page_file.write(page_html)


def load_questions_and_items():
    with open('items.json', 'r', encoding='utf-8') as item_file:
        items_json = json.load(item_file)
    return items_json


def render_question_pages(jinja_environment, items):
    template = jinja_environment.get_template('_questions.html')
    for subitem_number, subitem in enumerate(items):
        if subitem_number != len(items) - 1:
            next_page_filename = '{}.html'.format(subitem_number + 1)
        if subitem_number == len(items) - 1:
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
    render_pages_without_variables(env)
    render_question_pages(env, questions_and_items)
    render_result_page(env)


if __name__ == '__main__':
    render_site()
    server = Server()
    server.watch('templates/', render_site)
    server.watch('static/css/', render_site)
    server.serve(root='static/')
