from __main__ import app
from flask import render_template, redirect, flash, request
import aiohttp
from flask_login import current_user

from forms.reviewForm import ReviewForm


@app.route('/reviews/', defaults={'item_id': 'all'}, methods=['GET', 'POST'])
@app.route('/reviews/<item_id>', methods=['GET', 'POST'])
async def reviews_page(item_id):
    """Обработка страницы отзывов"""

    form = ReviewForm()
    session = aiohttp.ClientSession()
    
    request_criteria = await session.get(f'http://127.0.0.1:5000/api/item/criterions/{item_id}')
    criteria = await request_criteria.json()
    
    if request.method == 'POST':
        print("Форма валидна")
        advantages = form.advantages.data
        disadvantages = form.disadvantages.data
        review = form.review.data
        rating = form.rating.data
        criterion1 = form.criterion1.data
        criterion2 = form.criterion2.data
        criterion3 = form.criterion3.data
        
        criterions = {}
        for key, value in request.form.items():
            if key.startswith('criterion_value_'):
                criterion_number = key.split('_')[-1]
                criterion_name = request.form.get(f'criterion_name_{criterion_number}')
                criterions[criterion_name] = int(value)

        print(criterions)

        await session.post('http://127.0.0.1:5000/api/review', json={
            'user_id': current_user.id,
            'item_id': item_id,
            'advantages': advantages,
            'disadvantages': disadvantages,
            'review': review,
            'rating': rating,
            'criterion1': criterion1,
            'criterion2': criterion2,
            'criterion3': criterion3
        }) 
    
    
    request_stars_rating = await session.get(f'http://127.0.0.1:5000/api/rating/count/{item_id}')
    stars = await request_stars_rating.json()
    
    request_reviews = await session.get(f'http://127.0.0.1:5000/api/page/review/{item_id}')
    reviews_list = await request_reviews.json()
    
    item = reviews_list['item_info']
    reviews = reviews_list['all_reviews']
    
    item['reviews_rating'] = stars
    
    return render_template(
        'reviews.html',
        reviews=reviews,
        item=item,
        criteria=criteria,
        form=form
    )