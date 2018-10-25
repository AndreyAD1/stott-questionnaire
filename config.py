class Config(object):
    SECRET_KEY = 'SECRET_KEY'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://stott:stott@localhost/stott_questionnaire'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEVELOPMENT = True
