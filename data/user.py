import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    '''Форма создания таблицы пользователей'''
    
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True, unique=True, autoincrement=True)
    status = sa.Column(sa.VARCHAR, default='')
    name = sa.Column(sa.VARCHAR)
    email = sa.Column(sa.VARCHAR, index=True)
    count_feedbacks = sa.Column(sa.Integer, default=0)
    rank = sa.Column(sa.VARCHAR, default="Новичок")
    hashed_password = sa.Column(sa.VARCHAR)
    
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
     
    