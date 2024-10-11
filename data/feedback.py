import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

class Feedback(SqlAlchemyBase, SerializerMixin):
    '''Форма создания таблицы отзывов'''
    
    __tablename__ = 'Feedbacks'
    id = sa.Column(sa.INTEGER, primary_key=True, unique=True, autoincrement=True)
    user_id = sa.Column(sa.INTEGER, sa.ForeignKey('users.id'))
    item_id = sa.Column(sa.INTEGER, sa.ForeignKey('Items.id'))
    name = sa.Column(sa.VARCHAR, default="")
    advantage = sa.Column(sa.VARCHAR, default="")
    disadvantage = sa.Column(sa.VARCHAR, default="")
    text_feedback = sa.Column(sa.VARCHAR, default="")
    evaluation = sa.Column(sa.INTEGER, default=0)
    criterions = sa.Column(sa.JSON, default="")
    date_of_creation = sa.Column(sa.VARCHAR, default=datetime.utcnow)
    # date_of_creation = sa.Column(sa.VARCHAR)