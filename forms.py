from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired

class ResetPasswordForm(FlaskForm):
    motdepasse = PasswordField("Nouveau mot de passe", validators=[DataRequired()])
    submit = SubmitField("Réinitialiser")
