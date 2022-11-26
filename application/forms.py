from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

class CryptoForm(FlaskForm):
    name = StringField('Cryptocurrency', validators=[InputRequired(message="This field cannot be empty.")])
    submit = SubmitField('Add')