from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, FileField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired

characteristics = list(range(0, 100))


class ItemForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()], render_kw={'placeholder': 'Название'})
    description = TextAreaField('Описание', validators=[DataRequired()], render_kw={'placeholder': 'Описание'})
    criterion = SelectMultipleField(
        'Выберите характеристики',
        choices=[(char, char) for char in characteristics],
        validators=[DataRequired()])
    image = FileField('Загрузите изображение', render_kw={"placeholder": "Изображение блюда"})
    submit = SubmitField('Добавить')
