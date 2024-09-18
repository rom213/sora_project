from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class ResetRequestForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired()])
    submit = SubmitField(label="Reset Password", validators=[DataRequired()])


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message="La contraseña debe tener al menos 8 caracteres."),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Las contraseñas deben coincidir."),
        ],
    )
    submit = SubmitField("Change Password")
