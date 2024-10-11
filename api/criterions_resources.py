from flask_restful import Resource
from data import db_session
from data.feedback import Feedback
from data.user import User
from data.item import Item
from flask import jsonify, Response, request
import dataclasses
import json

@dataclasses.dataclass
class GetCriterions(Resource):
    def get(self, item_id):
        db_sess = db_session.create_session()
        request_criterions = db_sess.query(Item).filter(Item.id == item_id).first()
        lst_criterions = request_criterions.criterions
        lst_criterions = lst_criterions.split('-')
        criterions = {
            'criterion1': lst_criterions[0],
            'criterion2': lst_criterions[1],
            'criterion3': lst_criterions[2]
        }
        return jsonify(criterions)