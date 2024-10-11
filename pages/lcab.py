from __main__ import app
from flask import render_template, redirect, flash, url_for, request
import aiohttp
from flask_login import current_user

from forms.item import ItemForm


@app.route("/userlcab")
async def lcab_page():
    if current_user.status == 'user':
        session = aiohttp.ClientSession()
        result_user_info = await session.get(f'http://127.0.0.1:5000/api/user/info/{current_user.id}')
        user = await result_user_info.json()
        result_rank = await session.get(f'http://127.0.0.1:5000/api/user/rank/{current_user.id}')
        rank_rise = await result_rank.json()
        result_reviews = await session.get(f'http://127.0.0.1:5000/api/reviews/user/{current_user.id}')
        reviews = await result_reviews.json()
        
        session.close()

        return render_template(
            "lcab_user.html",
            user=user,
            reviews=reviews['user_reviews'],
            rank=rank_rise['rank'],
            rise=rank_rise['rise']
        )
    elif current_user.status == 'seller':
        form = ItemForm()
        
        if request.method == 'POST':
            session = aiohttp.ClientSession()
            form_data = {
                'name': form.name.data,
                'description': form.description.data,
                'criterion': form.criterion.data,  # Список характеристик
            }
            
            # Обработка файла (если требуется отправить изображение)
            image_file = form.image.data
            if image_file:
                form_data['image'] = image_file.read()  # Пример, как можно передать изображение
            
            # Отправляем данные на API для создания нового товара
            async with session.post(f'http://127.0.0.1:5000/api/seller/add_item/{current_user.id}', json=form_data) as response:
                result = await response.json()
            
            session.close()
            
            if result['success']:
                flash('Товар успешно добавлен!', 'success')
            else:
                flash('Ошибка при добавлении товара!', 'danger')
            
            return redirect(url_for('lcab_page'))
        
        session = aiohttp.ClientSession()
        requst_seller_info = await session.get(f'http://127.0.0.1:5000/api/seller/info/{current_user.id}')
        seller_info = await requst_seller_info.json()
        requst_count_products = await session.get(f'http://127.0.0.1:5000/api/seller/count-products/{current_user.id}')
        count_products = await requst_count_products.json()
        requst_seller_items = await session.get(f'http://127.0.0.1:5000/api/seller/items/{current_user.id}')
        seller_items = await requst_seller_items.json()
        
        seller_info['count_products'] = count_products['count']
        seller_info['status'] = 'Продавец'
        
        return render_template(
            "lcab_seller.html",
            user=seller_info,
            items=seller_items,
            form=form
        )


@app.route("/lcabseller")
def lcab_seller_page():
    form = ItemForm()
    user = {
        "name": "ЗАЛУПКИН",
        "email": "cqweqwe@qwe.ru",
        "count_products": 52,
        "status": 'Продавец на озоне'
    }
    items = [
        {"id": '1',
         "name": "Медиаторы Dunlop",
         "description": "Самые лучшие медиаторы на всей планете, сделаны из исклюзивного материала Tortex, толщина 0.88мм. Медиаторы обладают наилучшей износостойкостью и удобным захватом",
         "rating": 4.9,
         "stars": 5,
         "reviews": 10,
         "reviews_rating": {5: "90", 4: "4", 3: "1", 2: "1", 1: "2"}},
        {"id": '2',
         "name": "Медиаторы Dunlop",
         "description": "Самые лучшие медиаторы на всей планете, сделаны из исклюзивного материала Tortex, толщина 0.88мм. Медиаторы обладают наилучшей износостойкостью и удобным захватом",
         "rating": 4.7,
         "stars": 5,
         "reviews": 10,
         "reviews_rating": {5: "90", 4: "4", 3: "1", 2: "1", 1: "2"}
         },
        {"id": '3',
         "name": "Медиаторы Dunlop",
         "description": "Самые лучшие медиаторы на всей планете, сделаны из исклюзивного материала Tortex, толщина 0.88мм. Медиаторы обладают наилучшей износостойкостью и удобным захватом",
         "rating": 4.8,
         "stars": 5,
         "reviews": 10,
         "reviews_rating": {5: "78", 4: "5", 3: "5", 2: "2", 1: "2"}
         }
    ]
    return render_template(
        "lcab_seller.html",
        user=user,
        items=items,
        form=form
    )
