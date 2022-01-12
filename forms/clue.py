from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import Length, DataRequired


class ClueForm(FlaskForm):
    text = StringField("Indice",
                       validators=[
                           DataRequired(),
                           Length(min=1,
                                  max=255,
                                  message="Ton indice doit avoir une longueur comprise entre %(min)d et %(max)d "
                                          "caractères")])