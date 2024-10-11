from flask_restful import Resource
from data import db_session
from data.item import Item
from data.user import User
from data.feedback import Feedback
from data.criteria import Criteria
from flask import jsonify, Response
import dataclasses
import json

@dataclasses.dataclass
class CommonItem(Resource):
    '''Класс для работы с моделью Item'''
    def get(self):
        '''Метод для получения всех items из базы данных'''
        db_sess = db_session.create_session()
        items_request = db_sess.query(Item).all()
        
        items = [
            {
                'name_of_item': item.name_of_item,
                'description': item.description,
                'rating': item.rating,
                'price': item.price,
                'feedbacks': item.feedbacks
            }
            for item in items_request
        ]
        res = json.dumps(
            {
                'items': items
            },
            ensure_ascii=False        
        )
        db_sess.close()
        return Response(res, content_type='application/json; charset=utf-8')
    
    def post(self):
        '''Метод для добавления нового item в базу данных'''
        db_sess = db_session.create_session()
        
        new_item = Item() # дописать
        
        db_sess.add(new_item)
        db_sess.commit()
        db_sess.close()
    
@dataclasses.dataclass
class DetailItem(Resource):
    '''Класс для работы с конкретным item по его имени'''
    def get(self, name_of_item):
        '''Метод для получения информации о конкретном item по его имени'''
        db_sess = db_session.create_session()
        item_request = db_sess.query(Item).filter(Item.name_of_item == name_of_item).first()
        if item_request is None:
            return jsonify({'error': 'Not found'}), 404
        item = [
            {
                'name_of_item': item_request.name_of_item,
                'description': item_request.description,
                'rating': item_request.rating,
                'price': item_request.price,
                'feedbacks': item_request.feedbacks
            }
        ]
        res = json.dumps(
            {
                'item': item
            },
            ensure_ascii=False          
        )
        db_sess.close()
        return Response(res, content_type='application/json; charset=utf-8')
    
    def put(self, name_of_item):
        '''Метод для обновления информации о конкретном item'''
        pass
    
    def delete(self, name_of_item):
        '''Метод для удаления конкретного item'''
        pass
    
@dataclasses.dataclass
class SellerItems(Resource):
    '''Класс для работы с items, принадлежащими конкретному продавцу'''
    def get(self, user_id):
        '''Метод для получения всех items продавца по его ID'''
        db_sess = db_session.create_session()
        request_items_info = db_sess.query(Item).filter(Item.user_id == user_id).all()
        if not request_items_info:
            return jsonify({'error': 'Not found'})
        info_items = [
            {
                'id': str(item.id),
                'name': item.name_of_item,
                'description': item.description,
                'rating': item.rating,
                'stars': round(int(item.rating))
            }
            for item in request_items_info
        ]

        db_sess.close()
        return jsonify(info_items)
        
@dataclasses.dataclass
class GetCriterionsProduct(Resource):
    '''Класс для получения критериев оценки продукта или услуги'''
    def get(self, category):
        '''Метод для получения критериев оценки по категории (item или service)'''
        db_sess = db_session.create_session()
        criterions = db_sess.query(Criteria).all()
        if category == 'item':
            crit_string = criterions[0]
            crit_string = crit_string.item
        elif category == 'service':
            crit_string = criterions[0]
            crit_string = crit_string.service
        else:
            return jsonify({'message': 'Bad request'}), 400
        crits = crit_string.split('-')
        res = json.dumps(
            {
                'criterions': crits
            },
            ensure_ascii=False          
        )
        db_sess.close()
        return Response(res, content_type='application/json; charset=utf-8')
        
    
