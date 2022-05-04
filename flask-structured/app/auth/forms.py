from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired('email can not be empty'),
                                    Length(1, 64),
                                    Email()])
    username = StringField('Username',
                           validators=[
                               DataRequired(),
                               Length(1, 64),
                               Regexp(
                                   '^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                   'Usernames must have only letters, number, dots or underscores')
                           ])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired('Password can not be empty'),
                                 EqualTo('password2', message='Password must be match')
                             ])
    password2 = PasswordField('Password2', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Email already registered')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(), Length(1, 64)])
    new_password = PasswordField('New Password',
                                 validators=[
                                     DataRequired(),
                                     Length(1, 64),
                                     EqualTo('new_password2', message='New password must be match.')
                                 ])
    new_password2 = PasswordField('New Password', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Change Password')


class SendResetMailForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired('email can not be empty'),
                                    Length(1, 64),
                                    Email()])
    submit = SubmitField('Send Email')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        '请输入新密码', validators=[DataRequired('email can not be empty'),
                              Length(1, 64)
                              ])
    password2 = PasswordField('再次输入新密码',
                              validators=[
                                  DataRequired('email can not be empty'),
                                  EqualTo('password'),
                                  Length(1, 64)
                              ])
    submit = SubmitField('Confirm')


class EditProfileForm(FlaskForm):
    name = StringField('Your name', validators=[DataRequired('Your name can not be empty') ,
                                                Length(1, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')
