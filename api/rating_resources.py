from flask_restful import Resource
from data import db_session
from data.feedback import Feedback
from data.item import Item
from flask import Response
import dataclasses
import json

@dataclasses.dataclass
class NumberRating(Resource):
    '''Класс для получения процентного распределения оценок продукта'''
    def get(self, item_id):
        '''Метод для получения процента каждой оценки (от 1 до 5) для данного продукта'''
        db_sess = db_session.create_session()
        reviews = db_sess.query(Feedback).filter(Feedback.item_id == item_id).all()
        count, count1, count2, count3, count4, count5 = 0, 0, 0, 0, 0, 0
        
        for review in reviews:
            if str(review.evaluation) == '1':
                count1 += 1
                count += 1
            elif str(review.evaluation) == '2':
                count2 += 1
                count += 1
            elif str(review.evaluation) == '3':
                count3 += 1
                count += 1
            elif str(review.evaluation) == '4':
                count4 += 1
                count += 1
            elif str(review.evaluation) == '5':
                count5 += 1
                count += 1
        
        if count == 0:
            count = 1
        
        number_rating = {
            5: str(round((count5 / count) * 100)),
            4: str(round((count4 / count) * 100)),
            3: str(round((count3 / count) * 100)),
            2: str(round((count2 / count) * 100)),
            1: str(round((count1 / count) * 100))
        }
        res = json.dumps(number_rating, ensure_ascii=False)
        db_sess.close()
        return Response(res, content_type='application/json; charset=utf-8')
    
@dataclasses.dataclass
class AverageRating(Resource):
    '''Класс для получения средней оценки продукта'''
    def get(self, item_id):
        '''Метод для вычисления средней оценки для данного продукта'''
        db_sess = db_session.create_session()
        request_info_review = db_sess.query(Feedback).filter(Feedback.item_id == item_id)
        info_item = [int(review.evaluation) for review in request_info_review]
        
        average = {
            'average': round(sum(info_item) / len(info_item), 1)
        }
        
        res = json.dumps(average, ensure_ascii=False)
        db_sess.close()
        return Response(res, content_type='application/json; charset=utf-8')
        