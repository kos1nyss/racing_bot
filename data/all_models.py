import sqlalchemy
from .db_session import SqlAlchemyBase


class Status(SqlAlchemyBase):
    __tablename__ = 'statuses'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String)


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    status = sqlalchemy.Column(sqlalchemy.ForeignKey('statuses.id'))
    car_id = sqlalchemy.Column(sqlalchemy.ForeignKey('cars.id'), nullable=False)
    rating = sqlalchemy.Column(sqlalchemy.Integer)


class Car(SqlAlchemyBase):
    __tablename__ = 'cars'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    max_speed = sqlalchemy.Column(sqlalchemy.Integer)
    acceleration = sqlalchemy.Column(sqlalchemy.Integer)
