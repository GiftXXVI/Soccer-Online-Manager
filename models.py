from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from dateutil.relativedelta import relativedelta
db = SQLAlchemy()


class OnlineManagerModel():

    def insert(self):
        db.session.add(self)
        self.apply()

    def update(self):
        self.apply()

    def delete(self):
        db.session.delete(self)
        self.apply()

    def apply(self):
        db.session.commit()

    def refresh(self):
        db.session.refresh(self)

    def rollback(self):
        db.session.rollback()

    def dispose(self):
        db.session.close()


class Account(db.Model, OnlineManagerModel):
    __tablename__ = 'account'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    teams = db.relationship('Team', backref='user', lazy=True)

    def __repr__(self) -> str:
        return super().__repr__()


class Team(db.Model, OnlineManagerModel):
    __tablename__ = 'team'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'account.id'), unique=True, nullable=False)
    budget = db.Column(db.Numeric(), nullable=False)
    country_id = db.Column(db.Integer(), db.ForeignKey(
        'country.id'), nullable=False)
    players = db.relationship('Player', backref='team', lazy=True)

    def value():
        return 0

    def __repr__(self) -> str:
        return super().__repr__()


class Player(db.Model, OnlineManagerModel):
    __tablename__ = 'player'
    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(), nullable=True)
    lastname = db.Column(db.String(), nullable=False)
    date_of_birth = db.Column(db.DateTime(), nullable=False)
    country_id = db.Column(db.Integer(), db.ForeignKey(
        'country.id'), nullable=False)
    team_id = db.Column(db.Integer(), db.ForeignKey('team.id'), nullable=False)
    position_id = db.Column(db.Integer(), db.ForeignKey(
        'position.id'), nullable=False)
    value = db.Column(db.Numeric(), nullable=False)
    transfer_listed = db.Column(db.Boolean(), nullable=False, default=False)

    def age():
        return 0

    def __repr__(self) -> str:
        return super().__repr__()


class Position(db.Model, OnlineManagerModel):
    __tablename__ = 'position'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    players = db.relationship('Player', backref='position', lazy=True)

    def __repr__(self) -> str:
        return super().__repr__()


class Config(db.Model, OnlineManagerModel):
    __tablename__ = 'config'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    value = db.Column(db.String(), nullable=False)

    def __repr__(self) -> str:
        return super().__repr__()


class Country(db.Model, OnlineManagerModel):
    __tablename__ = 'country'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    players = db.relationship('Player', backref='country', lazy=True)
    teams = db.relationship('Team', backref='country', lazy=True)

    def __repr__(self) -> str:
        return super().__repr__()
