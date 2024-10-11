from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.fields.choices import RadioField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    '''Форма регистрации пользователя'''
    role = RadioField('Роль', choices=[('user', 'Пользователь'), ('seller', 'Продавец')], default='user')
    name = StringField('Имя', validators=[DataRequired()], render_kw={'placeholder': 'Имя'})
    fullname = StringField('Фамилия', validators=[DataRequired()], render_kw={'placeholder': 'Фамилия'})
    email = StringField('Email', validators=[DataRequired()], render_kw={'placeholder': 'E-mail'})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'placeholder': 'Пароль'})
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()], render_kw={'placeholder': 'Повторите пароль'})
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    '''Форма входа пользователя'''
    email = StringField('Email', validators=[DataRequired()], render_kw={'placeholder': 'E-mail'})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'placeholder': 'Пароль'})
    submit = SubmitField('Войти')
    
class ResetPasswordForm(FlaskForm):
    '''Форма смены пароля'''
    old_password = PasswordField('Текущий пароль', validators=[DataRequired()], render_kw={'placeholder': 'Текущий пароль'})
    new_password = PasswordField('Новый пароль', validators=[DataRequired()], render_kw={'placeholder': 'Новый пароль'})
    repeat_password = PasswordField('Повторите пароль', validators=[DataRequired()], render_kw={'placeholder': 'Повторите пароль'})
    submit = SubmitField('Сменить пароль')
