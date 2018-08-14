from flask import Flask, render_template


application = Flask(__name__)


@application.route('/')
def index():
    return render_template('index.html', page_title='Главная')


@application.route('/person_info')
def person_info():
    return render_template(
        'person_info.html',
        page_title='Информация об обследуемом'
    )


if __name__ == '__main__':
    application.run()