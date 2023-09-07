from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp


class RegistrationForm(FlaskForm):
    firstname = StringField('Firstname')
    lastname = StringField('Lastname')
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8),
                                                     Regexp('(?=.*[a-z])(?=.*[0-9])',
                                                            message="Пароль должен состоять и букв и цифр")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])