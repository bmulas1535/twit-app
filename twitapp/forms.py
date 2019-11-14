from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo
from twitapp.models import User

class Registration(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8)
        ]
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )
    submit = SubmitField('Sign Up')


class Login(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired()
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField('Login')
