import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://stott:stott@localhost/stott_questionnaire'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEVELOPMENT = True
