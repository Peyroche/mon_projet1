from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Adresse e-mail", validators=[DataRequired(), Email()])
    submit = SubmitField("Envoyer le lien de réinitialisation")
