import json
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect


application = Flask(__name__)
application.config.from_object(Config)
db = SQLAlchemy(application)
migrate = Migrate(application, db)
csrf = CSRFProtect(application)


if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler(
    'logs/questionnaire.log',
    maxBytes=10240,
    backupCount=10
)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
application.logger.addHandler(file_handler)
application.logger.setLevel(logging.INFO)
application.logger.info('Stott questionnaire starts')


with open('symptoms.json', 'r', encoding='utf-8') as symptom_file:
    symptom_list = json.load(symptom_file)
with open('aptitudes.json', 'r', encoding='utf-8') as aptitude_file:
    aptitude_list = json.load(aptitude_file)


from app import routes, db_models
