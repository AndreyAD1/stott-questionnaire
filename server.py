from flask import Flask, render_template, request
import json


application = Flask(__name__)
application.config.update(ENV='development', DEBUG=True)
with open('items.json', 'r', encoding='utf-8') as item_file:
    item_list = json.load(item_file)



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
def questions_and_result(item_num):
    print(request.form)
    page_number = int(item_num)
    if page_number <= len(item_list):
        item_index = page_number - 1
        subitem = item_list[item_index]
        total_page_number = len(item_list)
        next_page_name = page_number + 1
        return render_template(
                '_questions.html',
                page_content=subitem,
                page_number=page_number,
                total_page_number=total_page_number,
                next_page_number=next_page_name
            )
    if page_number > len(item_list):
        return render_template('result.html')


if __name__ == '__main__':
    application.run()