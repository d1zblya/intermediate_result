from __main__ import app
from forms.user import ResetPasswordForm
from flask import render_template, redirect
from data import db_session
from data.user import User
from flask_login import current_user
from pages.registration import check_password

@app.route('/passwordreset', methods=['GET', 'POST'])
def passwordreset_page():
    """Обработка смены пароля"""
    form = ResetPasswordForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == current_user.email).first()
        if not user.check_password(form.old_password.data):
            return render_template('passwordreset.html',
                                   form=form,
                                   message='Текущий пароль не совпадает с новым')
        if form.new_password.data != form.repeat_password.data:
            return render_template(
                'passwordreset.html',
                form=form,
                message='Новые пароли не совпадают'
            )
            
        recommendations = check_password(form.new_password.data)
        if recommendations != 'Пароль сильный':
            return render_template(
                'passwordreset.html',
                form=form,
                message=recommendations
            )
        
        user.hashed_password = ''
        
        user = db_sess.query(User).filter(User.email == current_user.email).first()
        user.set_password(form.new_password.data)
        db_sess.commit()
        return redirect('/lcab')
    
    return render_template(
        'passwordreset.html',
            form=form,
    )