from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User

class LoginForm(FlaskForm):
    """Simple login form"""

    email = StringField('Email', validators=[DataRequired(), Length(1,64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    """Simple Registration Form"""

    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1,
                           64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                           'Username must have only letters numbers,'
                                       ' dots or underscores')])
    password = PasswordField('Password',validators=[DataRequired(),
                             EqualTo('password2', 'Passwords must match.')])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        """Validate that email field is not already Registered"""

        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email Already Registered.')

    def validate_username(self, field):
        """Validate that Username is not already in use"""

        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

# Add a form to change user passwords


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[
        DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must '
                                                    'match')])
    password2 = PasswordField('Confirm new password', validators=[
        DataRequired()])
    submit = SubmitField('Update Password')