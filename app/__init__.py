import json
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


with open('symptoms.json', 'r', encoding='utf-8') as symptom_file:
    symptom_list = json.load(symptom_file)
with open('aptitudes.json', 'r', encoding='utf-8') as aptitude_file:
    aptitude_list = json.load(aptitude_file)


from app import routes, db_models
