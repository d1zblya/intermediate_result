from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, NumberRange


class ReviewForm(FlaskForm):
    rating = IntegerField('Рейтинг', validators=[DataRequired()])
    advantages = StringField('Достоинства', validators=[DataRequired()], render_kw={'placeholder': 'Достоинства'})
    disadvantages = StringField('Недостатки', validators=[DataRequired()], render_kw={'placeholder': 'Недостатки'})
    criterion1 = IntegerField(validators=[InputRequired(), NumberRange(min=1, max=5)])
    criterion2 = IntegerField(validators=[InputRequired(), NumberRange(min=1, max=5)])
    criterion3 = IntegerField(validators=[InputRequired(), NumberRange(min=1, max=5)])
    review = TextAreaField('Ваш отзыв', validators=[DataRequired()], render_kw={'placeholder': 'Комментарий'})
    submit = SubmitField('Отправить')
