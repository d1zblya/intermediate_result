from __main__ import app
from forms.reviewForm import ReviewForm
from flask import render_template, redirect
from wtforms import StringField
from wtforms.validators import DataRequired


@app.route('/review', methods=['GET', 'POST'])
def review_page():
    form = ReviewForm()

    item = {
        "id": '1',
        "name": "Медиаторы Dunlop",
        "description": "Самые лучшие медиаторы на всей планете, сделаны из исклюзивного материала Tortex, толщина 0.88мм. Медиаторы обладают наилучшей износостойкостью и удобным захватом",
        "rating": 4.9,
        "stars": 5,
        "criterion": ["Аккумулятор", "Великолепность", "Экран"]
            }

    

    return render_template(
        'review.html',
        form=form,
        item=item
        )