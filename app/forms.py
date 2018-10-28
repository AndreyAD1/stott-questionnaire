from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField
from wtforms.validators import DataRequired


class PersonInfoForm(FlaskForm):
    age = IntegerField('Age', validators=[DataRequired()])
    sex = RadioField('Sex', validators=[DataRequired()])
    grade = IntegerField('Grade', validators=[DataRequired()])
    family_type = RadioField('Family_type')
    child_number = IntegerField('Child_number')
    order_number = IntegerField('Order_number')
    family_history = StringField('Family_history')
