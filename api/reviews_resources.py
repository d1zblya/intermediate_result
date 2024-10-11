from flask_restful import Resource
from data import db_session
from data.feedback import Feedback
from data.user import User
from flask import jsonify, Response, request
import dataclasses
import json
from flask_login import current_user
from datetime import datetime

def parse_criterions(string_lst):
    result = []
    for string in string_lst:
        criterions_dict = {}
        pairs = string.split(';')
        for pair in pairs:
            key, value = pair.split('-')
            criterions_dict[key] = value
        result.append(criterions_dict)
    return result


@dataclasses.dataclass
class CommonReview(Resource):
    '''Класс для получения всех отзывов'''
    def get(self):
        '''Метод для получения списка всех отзывов'''
        db_sess = db_session.create_session()
        all_rewiews = db_sess.query(User, Feedback).join(User, Feedback.user_id == User.id).all()
        rewiews = [
            {
                'username': user.name,
                'evaluation': rew.evaluation,
                'date': rew.date_of_creation,
                'text': rew.text_feedback
            }
            for user, rew in all_rewiews
        ]
        res = json.dumps(
            {
                'all_rewiews': rewiews
            },
            ensure_ascii=False         
        )
        db_sess.close()
        return Response(res, content_type='application/json; charset=utf-8')
    
    def post(self):
        '''Метод для добавления нового отзыва'''
        db_sess = db_session.create_session()
        info = request.json()
        print(info)
        new_review = Feedback(
            
        )
        
        db_sess.add(new_review)
        db_sess.commit()
        db_sess.close()
        
@dataclasses.dataclass
class DetailReview(Resource):
    '''Класс для работы с конкретным отзывом'''
    def get(self, review_id):
        '''Метод для получения отзыва по его ID'''
        db_sess = db_session.create_session()
        review_request = db_sess.query(User, Feedback).join(User, Feedback.user_id == User.id).filter(Feedback.id == review_id).first()
        if review_request is None:
            return jsonify({'error': 'Not found'}), 404
        user, rew = review_request
        review = [
            {
                'username': user.name,
                'evaluation': rew.evaluation,
                'date': rew.date_of_creation,
                'text': rew.text_feedback
            }
        ]
        res = json.dumps(
            {
                'review': review
            },
            ensure_ascii=False        
        )
        db_sess.close()
        return Response(res, content_type='application/json; charset=utf-8')
    
    def put(self, review_id):
        '''Метод для обновления информации об отзыве (не реализован)'''
        pass
    
    def delete(self, review_id):
        '''Метод для удаления отзыва (не реализован)'''
        pass
    
@dataclasses.dataclass
class GetUserReviews(Resource):
    '''Класс для получения всех отзывов пользователя'''
    def get(self, current_user_id):
        '''Метод для получения списка отзывов, оставленных текущим пользователем'''
        db_sess = db_session.create_session()
        user_reviews_request = db_sess.query(Feedback).filter(Feedback.user_id == current_user_id).all()
        # intermediate_result = [info.criterions for info in user_reviews_request]
        # result = parse_criterions(intermediate_result)
        user_reviews = [
            {
                'evaluation': int(info.evaluation),
                'date': info.date_of_creation,
                'criterion': info.criterions,
                'advantage': info.advantage,
                'disadvantage': info.disadvantage,
                'text': info.text_feedback
            }
            for info in user_reviews_request
            # for info, crit in zip(user_reviews_request, result)
        ]
        res = json.dumps(
            {
                'user_reviews': user_reviews
            },
            ensure_ascii=False    
        )
        db_sess.close()
        return Response(res, content_type='application/json; charset=utf-8')
    
@dataclasses.dataclass
class WriteReview(Resource):
    '''Класс для добавления или редактирования отзывов'''
    def get(self):
        '''Метод для получения формы или шаблона для добавления отзыва (не реализован)'''
        pass
    
    def post(self):
        '''Метод для отправки нового отзыва (не реализован)'''
        data = request.json

        required_fields = ['rating', 'advantages', 'disadvantages', 'review', 'criterion1', 'criterion2', 'criterion3']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Все поля обязательны"})

        rating = data.get('rating')
        if not (1 <= rating <= 5):
            return jsonify({"error": "Рейтинг должен быть от 1 до 5"})
        
        db_sess = db_session.create_session()
        feedback = Feedback(
            user_id=data.get('user_id'),
            item_id=data.get('item_id'),
            evaluation=rating,
            advantage=data.get('advantages'),
            disadvantage=data.get('disadvantages'),
            text_feedback=data.get('review'),
            criterions=json.dumps({
                "criterion1": data.get('criterion1'),
                "criterion2": data.get('criterion2'),
                "criterion3": data.get('criterion3')
            }),
            date_of_creation=datetime.now().isoformat()
        )

        try:
            db_sess.add(feedback)
            db_sess.commit()
        except Exception as e:
            db_sess.rollback()  # Отменяем изменения, если произошла ошибка
            print(f"Ошибка при сохранении в базу данных: {e}")
        finally:
            db_sess.close()

        return jsonify({"message": "Отзыв успешно добавлен"})
