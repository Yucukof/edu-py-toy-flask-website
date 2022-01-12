import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp


class LoginForm(FlaskForm):
    username = StringField('Utilisateur',
                           validators=[InputRequired(message="Ce champ est obligatoire"),
                                       Length(min=1,
                                              message="Le nom d'utilisateur ne peut pas être vide.")
                                       ]
                           )
    password = PasswordField('Mot de passe',
                             validators=[InputRequired(message="Ce champ est obligatoire"),
                                         Length(min=1, message="Le mot de passe ne peut pas être vide.")
                                         ]
                             )
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    username = StringField('Utilisateur',
                           validators=[InputRequired(message="Ce champ est obligatoire"),
                                       Regexp(flags=re.IGNORECASE,
                                              regex='[A-Za-z0-9]+',
                                              message="Le nom d'utilisateur doit contenir uniquement des caractères "
                                                      "alphanumériques"),
                                       Length(min=5,
                                              max=20,
                                              message="Le nom d'utilisateur doit avoir une taille entre %(min)d et %("
                                                      "max)d caractères.")
                                       ]
                           )
    password = PasswordField('Mot de passe',
                             validators=[InputRequired(message="Ce champ est obligatoire"),
                                         EqualTo('confirm',
                                                 message='Les deux mots de passe ne correspondent pas.'),
                                         Length(min=8,
                                                max=100,
                                                message="Le mot de passe doit avoir une taille entre %(min)d et %("
                                                        "max)d caractères.")
                                         ]
                             )
    confirm = PasswordField('Répéter le mot de passe',
                            validators=[InputRequired(message="Ce champ est obligatoire"),
                                        EqualTo('password',
                                                message='Les deux mots de passe ne correspondent pas.'),
                                        Length(min=8,
                                               max=100,
                                               message="Le mot de passe doit avoir une taille entre %(min)d et %("
                                                       "max)d caractères.")
                                        ]
                            )
    submit = SubmitField('Register')
