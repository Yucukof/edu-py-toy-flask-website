from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField
from wtforms.validators import DataRequired


class ResponseForm(FlaskForm):
    id = IntegerField(DataRequired(message="Une réponse est obligatoire"))
    value = BooleanField(DataRequired(message="Une réponse est obligatoire"))
