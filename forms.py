from flask_wtf import Form
from wtforms import StringField, TextField, IntegerField, SubmitField, SelectField, validators, PasswordField

class CreateMailbox(Form):
    first_name = TextField('First Name')
    last_name = TextField('Last Name')
    display_name = TextField('Display Name')
    username = TextField('Username')
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
