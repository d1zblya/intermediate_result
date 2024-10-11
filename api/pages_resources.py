from flask_restful import Resource
from data import db_session
from data.item import Item
from data.user import User
from data.feedback import Feedback
from flask import jsonify, Response
import dataclasses
import json
from api.reviews_resources import parse_criterions

@dataclasses.dataclass
class ProductPage(Resource):
    '''Класс для работы с отображением страницы продуктов'''
    def get(self):
        '''Метод для получения всех продуктов'''
        db_sess = db_session.create_session()
        product_request = db_sess.query(Item).all()
        product = [
            {
                'id': str(item.id),
                'name_of_item': item.name_of_item,
                'description': item.description,
                'rating': item.rating,
                'stars': round(item.rating)
            }
            for item in product_request
        ]
        res = json.dumps(
            {
                'products': product
            },
            ensure_ascii=False
        )
        db_sess.close()
        return Response(res, content_type='application/json; charset=utf-8')
    
@dataclasses.dataclass
class ReviewsPage(Resource):
    '''Класс для работы с отображением отзывов о продукте'''
    def get(self, item_id):
        '''Метод для получения информации о продукте и его отзывах по id продукта'''
        db_sess = db_session.create_session()
        request_item_info = db_sess.query(Item).filter(Item.id == item_id).first()
        if not request_item_info:
            return {"error": "Item not found"}

        request_item_reviews = db_sess.query(User, Feedback).join(User, Feedback.user_id == User.id).filter(Feedback.item_id == item_id).all()
        
        db_sess = db_session.create_session()
        request_info_review = db_sess.query(Feedback).filter(Feedback.item_id == item_id)
        info_item = [int(review.evaluation) for review in request_info_review]
        
        # intermediate_result = [info.criterions for user, info in request_item_reviews]
        # result = parse_criterions(intermediate_result)
        
        reviews_list = [
            {
                'user_id': int(user.id),
                'username': user.name,
                'advantage': review.advantage,
                'disadvantage': review.disadvantage,
                'text_feedback': review.text_feedback,
                'evaluation': review.evaluation,
                'date': review.date_of_creation,
                'criterion': review.criterions
            }
            for user, review in request_item_reviews
        ]
        if len(info_item) == 0:
            info_item.append(0)
        item_info = {
            'id': str(request_item_info.id),
            'name': request_item_info.name_of_item,
            'description': request_item_info.description,
            'rating': round(sum(info_item) / len(info_item), 1),
            'stars': round(sum(info_item) / len(info_item)),
            'reviews': len(reviews_list)
        }
        
        # for info, crit in zip(reviews_list, result):
        #     info['criterion'] = crit
        res = json.dumps(
            {
                'item_info': item_info,
                'all_reviews': reviews_list
            },
            ensure_ascii=False    
        )
        db_sess.close()
        return Response(res, content_type='application/json; charset=utf-8')
        
        