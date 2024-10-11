from __main__ import app
from forms.user import RegisterForm
from flask import render_template, redirect, request
from data import db_session
from data.user import User


def check_password(psw):
    digits = '1234567890'
    upper_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower_letters = 'abcdefghijklmnopqrstuvwxyz'
    symbols = '!@#$%^&*()-+'
    acceptable = digits + upper_letters + lower_letters + symbols
    
    password = set(psw)
    
    if any(char not in acceptable for char in password):
        return 'Недопустимый символ.'
    elif len(password) < 7:
        return f'Слишком маленький пароль, увеличить на {7 - len(password)} символов'
    else:
        recommendations = []
        
        for what, message in ((digits, 'цифру'), 
                              (upper_letters, 'заглавную букву'), 
                              (lower_letters, 'строчную букву'), 
                              (symbols, 'спец. символ')):
            if all(char not in what for char in password):
                recommendations.append(f'добавить 1 {message}')
        if recommendations:
            return f'Слабый пароль, рекомендации: {", ".join(recommendations)}'
        else:
            return 'Пароль сильный'


@app.route('/registration', methods=['GET', 'POST'])
def registration_page():
    'Обработка регистрации'
    form = RegisterForm()

    if request.method == 'POST':
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message='Пароли не совпадают')
        recommendations = check_password(form.password.data)
        if recommendations != 'Пароль сильный':
            return render_template(
                'registration.html',
                form=form,
                message=recommendations # 'Слишком короткий пароль! Сделайте пароль от 5 символов'
            )
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message='Такой пользователь уже есть')
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template(
        'registration.html',
        form=form,
        message='ок'
    )