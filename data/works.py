import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Works(SqlAlchemyBase):
    __tablename__ = 'works'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    time = sqlalchemy.Column(sqlalchemy.String)
    address = sqlalchemy.Column(sqlalchemy.String)
    mph = sqlalchemy.Column(sqlalchemy.Integer)
    min_pay = sqlalchemy.Column(sqlalchemy.Integer)
    ready = sqlalchemy.Column(sqlalchemy.String)
    photo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    amount = sqlalchemy.Column(sqlalchemy.Integer)
    free = sqlalchemy.Column(sqlalchemy.Integer)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    is_close = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')