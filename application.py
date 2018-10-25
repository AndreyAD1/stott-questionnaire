from flask import Flask


application = Flask(__name__)
application.config[
    'SQLALCHEMY_DATABASE_URI'
] = 'postgresql://stott:stott@localhost/stott_questionnaire'
application.config['SQLALCHEMY_ECHO'] = False
application.secret_key = 'SECRET_KEY'
application.config.update(ENV='development', DEBUG=True)
