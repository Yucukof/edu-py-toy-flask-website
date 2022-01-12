from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Length, NumberRange, DataRequired, InputRequired

from models import category


class RiddleForm(FlaskForm):
    name = StringField('Nom',
                       validators=[DataRequired(message="Ce champ est obligatoire"),
                                   Length(min=1,
                                          max=255,
                                          message='Le nom de ton énigme doit être compris entre %(min)d et %('
                                                  'max)d caractères. Keep it short & simple!')
                                   ]
                       )

    riddle = StringField('Énigme',
                         validators=[DataRequired(message="Ce champ est obligatoire"),
                                     Length(min=10,
                                            max=255,
                                            message='Le texte de ton énigme doit être compris entre %(min)d et %('
                                                    'max)d caractères. Raconte ta vie !')
                                     ]
                         )

    solution = BooleanField('Solution',
                            validators=[InputRequired("Ce champ est obligatoire")]
                            )

    difficulty = IntegerField('Difficulté',
                              validators=[NumberRange(min=1,
                                                      max=5,
                                                      message="La difficulté de ton énigme doit être comprise entre "
                                                              "%(min)d & et %(max)d.")
                                          ]
                              )

    explanation = StringField('Explication:',
                              validators=[Length(min=0,
                                                 max=255,
                                                 message='Ton explication ne peut pas faire plus de %(max)d '
                                                         'caractères. Sois plus concis !')
                                          ]
                              )

    category = QuerySelectField("Category"
                                , query_factory=category.get_all
                                , allow_blank=True
                                )

    submit = SubmitField('Envoyer')
