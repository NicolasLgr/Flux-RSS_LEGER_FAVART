from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import PasswordInput
from feedparser import *

class Inscription(FlaskForm):
    user = StringField('Nom utilisateur ', validators=[DataRequired(), Length(min=3, max=20)])
    password = StringField('Mot de passe ', validators=[DataRequired()], widget=PasswordInput(hide_value=True))
    pass

class Connexion(FlaskForm):
    user = StringField('Nom utilisateur ', validators=[DataRequired(), Length(min=3, max=20)])
    password = StringField('Mot de passe', widget=PasswordInput(hide_value=True))
    pass

class AjoutFlux(FlaskForm):
    lien = StringField('Lien du flux ', validators=[DataRequired()])
    pass
