from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Adresse e-mail", validators=[DataRequired(), Email()])
    submit = SubmitField("Envoyer le lien de réinitialisation")

class ResetPasswordForm(FlaskForm):
    motdepasse = PasswordField("Nouveau mot de passe", validators=[DataRequired()])
    submit = SubmitField("Réinitialiser")
