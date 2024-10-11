from flask_restful import Resource
from data import db_session
from data.feedback import Feedback
from data.item import Item
from data.user import User
from flask import jsonify, Response, request
import dataclasses
import json


@dataclasses.dataclass
class UserInfo(Resource):
    def get(self, user_id):
        db_sess = db_session.create_session()
        user_info = db_sess.query(User).filter(User.id == user_id).first()
        if user_info is None:
            return jsonify({'error': 'Not found'}), 404
        user = {
            'username': user_info.name,
            'email': user_info.email,
            'rank': user_info.rank,
            'rise': 'None',
            'count_feedbacks': user_info.count_feedbacks
        }
        res = json.dumps(user, ensure_ascii=False)
        db_sess.close()
        return Response(res, content_type='application/json; charset=utf-8')
    
@dataclasses.dataclass
class UserRank(Resource):
    def get(self, user_id):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == user_id).first()
        if user is None:
            return jsonify({'error': 'Not found'}), 404
        count_feedbacks = user.count_feedbacks
        if count_feedbacks < 20:
            user.rank = 'Новичок'
            db_sess.commit()
            rank = {
                'rise': 20 - int(count_feedbacks),
                'rank': 'Новичок'
            }
            res = json.dumps(rank, ensure_ascii=False)
            return Response(res, content_type='application/json; charset=utf-8')
        elif 20 <= count_feedbacks < 50:
            user.rank = 'Продвинутый'
            db_sess.commit()
            rank = {
                'rise': 50 - int(count_feedbacks),
                'rank': 'Продвинутый'
            }
            res = json.dumps(rank, ensure_ascii=False)
            return Response(res, content_type='application/json; charset=utf-8')
        elif count_feedbacks >= 50:
            user.rank = 'Эксперт'
            db_sess.commit()
            rank = {
                'rise': 0,
                'rank': 'Эксперт'
            }
            res = json.dumps(rank, ensure_ascii=False)
            return Response(res, content_type='application/json; charset=utf-8')
        
@dataclasses.dataclass
class SelerInfo(Resource):
    def get(self, user_id):
        db_sess = db_session.create_session()
        seller_info = db_sess.query(User).filter(User.id == user_id).first()
        if seller_info is None:
            return jsonify({'error': 'Not found'}), 404
        user = {
            'name': seller_info.name,
            'email': seller_info.email,
            'status': seller_info.status,
            'count_products': seller_info.count_feedbacks
        }
        res = json.dumps(user, ensure_ascii=False)
        db_sess.close()
        return Response(res, content_type='application/json; charset=utf-8')
    
@dataclasses.dataclass
class CountProducts(Resource):
    def get(self, user_id):
        db_sess = db_session.create_session()
        request_info = db_sess.query(Item).filter(Item.user_id == user_id)
        if request_info is None:
            return jsonify({'error': 'Not found'}), 404
        count = len([info.user_id for info in request_info])
        result = {
            'count': count
        }
        res = json.dumps(result, ensure_ascii=False)
        db_sess.close()
        return Response(res, content_type='application/json; charset=utf-8')
    
@dataclasses.dataclass
class SellerAddItem(Resource):
    def post(self, seller_id):
        data = request.get_json()  # Получаем данные из запроса
        db_sess = db_session.create_session()
        new_item = Item(
            name=data['name'],
            description=data['description'],
            criterion=data['criterion'],
            seller_id=seller_id
        )
        # Добавление изображения, если оно есть
        # if 'image' in data:
        #     new_item.image = save_image(data['image'])  # Функция для сохранения изображения
        
        db_sess.add(new_item)
        db_sess.commit()
        db_sess.close()
        
        return jsonify({'success': True}) 
    
        