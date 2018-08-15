from flask import Flask, render_template, request
from site_render import load_questions_and_items


application = Flask(__name__)
application.config.update(ENV='development', DEBUG=True)


@application.route('/')
def index():
    return render_template('index.html', page_title='Главная')


@application.route('/person_info')
def person_info():
    return render_template(
        'person_info.html',
        page_title='Информация об обследуемом'
    )


@application.route('/questions/<item_num>', methods=['POST'])
def questions(item_num):
    item_list = load_questions_and_items()
    subitem = item_list[int(item_num) - 1]
    total_page_number = len(item_list)
    page_number = int(item_num)
    next_page_number = int(item_num) + 1
    return render_template(
            '_questions.html',
            page_content=subitem,
            page_number=page_number,
            total_page_number=total_page_number,
            next_page_number=next_page_number
        )


if __name__ == '__main__':
    application.run()