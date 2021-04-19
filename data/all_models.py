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
    upgrade_points = sqlalchemy.Column(sqlalchemy.Integer)


class Car(SqlAlchemyBase):
    __tablename__ = 'cars'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    max_speed = sqlalchemy.Column(sqlalchemy.Integer)
    acceleration = sqlalchemy.Column(sqlalchemy.Integer)
    turbo = sqlalchemy.Column(sqlalchemy.Integer)


class InvitedUsers(SqlAlchemyBase):
    __tablename__ = 'invited_users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    owner_id = sqlalchemy.Column(sqlalchemy.ForeignKey('users.id'))
    in_game = sqlalchemy.Column(sqlalchemy.Boolean)


class Result(SqlAlchemyBase):
    __tablename__ = 'results'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user1 = sqlalchemy.Column(sqlalchemy.ForeignKey('users.id'))
    user2 = sqlalchemy.Column(sqlalchemy.ForeignKey('users.id'))
    winner = sqlalchemy.Column(sqlalchemy.ForeignKey('users.id'))
    time = sqlalchemy.Column(sqlalchemy.Integer)
