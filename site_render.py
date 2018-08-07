from jinja2 import Environment, FileSystemLoader
from livereload import Server


def render_main_page(jinja_environment):
    template = jinja_environment.get_template('index.html')
    index_html = template.render()
    with open('static/index.html', 'w', encoding='utf-8') as index_file:
        index_file.write(index_html)


def render_person_info_page(jinja_environment):
    template = jinja_environment.get_template('person_info.html')
    person_info_html = template.render()
    with open('static/person_info.html', 'w') as person_file:
        person_file.write(person_info_html)


def render_site():
    env = Environment(loader=FileSystemLoader('templates/'))
    render_main_page(env)
    render_person_info_page(env)


if __name__ == '__main__':
    render_site()
    server = Server()
    server.watch('templates/', render_site)
    server.watch('static/css/', render_site)
    server.serve(root='static/')
