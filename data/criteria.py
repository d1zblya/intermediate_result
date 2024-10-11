import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

class Criteria(SqlAlchemyBase, UserMixin, SerializerMixin):
    '''Форма создания таблицы критериев'''
    __tablename__ = 'criteria'
    id = sa.Column(sa.Integer, primary_key=True, unique=True, autoincrement=True)
    item = sa.Column(sa.VARCHAR)
    service = sa.Column(sa.VARCHAR)