from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import validators

class NameForm(FlaskForm):
    name = StringField('What is your name?',[validators.DataRequired()])
    submit = SubmitField('Submit')