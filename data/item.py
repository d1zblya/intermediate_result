import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin

class Item(SqlAlchemyBase, SerializerMixin):
    '''Форма создания таблицы предметов оценивания (которые оценивают)'''
    
    __tablename__ = 'Items'
    id = sa.Column(sa.INTEGER, primary_key=True, unique=True, autoincrement=True)
    user_id = sa.Column(sa.INTEGER, sa.ForeignKey('user.id'))
    name_of_item = sa.Column(sa.VARCHAR, default="")
    description = sa.Column(sa.VARCHAR, default="")
    rating = sa.Column(sa.INTEGER, default=0)
    criterions = sa.Column(sa.VARCHAR)
    price = sa.Column(sa.INTEGER, default=0)
    feedbacks = sa.Column(sa.INTEGER, default=0)