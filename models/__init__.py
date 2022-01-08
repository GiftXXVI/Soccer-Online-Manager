import models.configuration as configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timedelta
from random import randrange
from random import choice
from dateutil.relativedelta import relativedelta

db = SQLAlchemy()
migrate = Migrate()
defaults = configuration.get_app_settings()


def setup_db(app) -> tuple:
    app.config["SQLALCHEMY_DATABASE_URI"] = configuration.get_db_uri()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    return db, migrate


class OnlineManagerModel():
    def insert(self) -> None:
        db.session.add(self)

    def delete(self) -> None:
        db.session.delete(self)

    def stage(self) -> None:
        db.session.flush()

    def apply(self) -> None:
        db.session.commit()

    def refresh(self) -> None:
        db.session.refresh(self)

    def rollback(self) -> None:
        db.session.rollback()

    def dispose(self) -> None:
        db.session.close()


class Account(db.Model, OnlineManagerModel):
    __tablename__ = 'account'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)
    teams = db.relationship('Team', backref='account', lazy=True)

    def setup(self) -> None:
        self.active = True

    def format(self) -> dict:
        return {'id': self.id, 'email': self.email}


class Team(db.Model, OnlineManagerModel):
    __tablename__ = 'team'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=True)
    account_id = db.Column(db.Integer(), db.ForeignKey(
        'account.id'), unique=True, nullable=False)
    budget = db.Column(db.Numeric(), nullable=False,
                       default=defaults['INIT_TEAM_BUDGET'])
    country_id = db.Column(db.Integer(), db.ForeignKey(
        'country.id'), nullable=False)
    players = db.relationship('Player', backref='team', lazy=True)

    def setup(self) -> None:
        self.budget = defaults['INIT_TEAM_BUDGET']
        cities = City.query.filter(City.country_id == self.country_id).all()
        if len(cities) == 0:
            sample = 'abcdefghijklmnopqrstuvwxyz'
            length = 10
            string = (''.join(choice(sample)
                      for i in range(length))).capitalize()
            self.name = f'{string} {configuration.get_teamsuffix()}'
        else:
            self.name = f'{choice(cities).name} {configuration.get_teamsuffix()}'

    def value(self) -> int:
        val = 0
        for p in self.players:
            val += p.value
        return val

    def format(self) -> dict:
        return {'id': self.id,
                'account_id': self.account_id,
                'account': self.account.email,
                'budget': self.budget,
                'country_id': self.country_id,
                'country': self.country.name,
                'value': self.value()}


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
    value = db.Column(db.Numeric(), nullable=False,
                      default=defaults['INIT_PLAYER_VALUE'])
    transfer_listed = db.Column(db.Boolean(), nullable=False, default=False)

    def setup(self) -> None:
        now = datetime.now()
        self.date_of_birth = now.date() - relativedelta(years=randrange(16, 29))
        self.firstname = configuration.get_firstname()
        self.lastname = configuration.get_lastname()
        self.value = defaults['INIT_PLAYER_VALUE']
        self.transfer_listed = False

    def age(self) -> int:
        now = datetime.now()
        today = now.date()
        return relativedelta(today, self.date_of_birth).years

    def format(self) -> dict:
        return {'id': self.id,
                'firstname': self.firstname,
                'lastname': self.lastname,
                'date_of_birth': self.date_of_birth,
                'country_id': self.country_id,
                'country': self.country.name,
                'team_id': self.team_id,
                'team': self.team.name,
                'position_id': self.position_id,
                'value': self.value,
                'transfer_listed': self.transfer_listed}


class Position(db.Model, OnlineManagerModel):
    __tablename__ = 'position'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    initial_players = db.Column(db.Integer(), nullable=False)
    players = db.relationship('Player', backref='position', lazy=True)

    def format(self) -> dict:
        return {'id': self.id, 'name': self.name, 'initial_players': self.initial_players}


class City(db.Model, OnlineManagerModel):
    __tablename__ = 'city'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    country_id = db.Column(db.Integer(), db.ForeignKey(
        'country.id'), nullable=False)
    db.UniqueConstraint(name, country_id, name='UX_name_country')

    def format(self) -> dict:
        return {'id': self.id,
                'name': self.name,
                'country_id': self.country_id,
                'country': self.country.name}


class Country(db.Model, OnlineManagerModel):
    __tablename__ = 'country'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    players = db.relationship('Player', backref='country', lazy=True)
    teams = db.relationship('Team', backref='country', lazy=True)
    cities = db.relationship('City', backref='country', lazy=True)

    def format(self) -> dict:
        return {'id': self.id, 'name': self.name}
