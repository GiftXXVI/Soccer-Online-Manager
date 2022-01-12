import models.configuration as configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timedelta
from random import randrange
from random import choice
from dateutil.relativedelta import relativedelta
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
defaults = configuration.get_app_settings()


def setup_db(app) -> tuple:
    app.config["SQLALCHEMY_DATABASE_URI"] = configuration.get_db_uri()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret"
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


class Credential(db.Model, OnlineManagerModel):
    __tablename__ = 'credential'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    firstname = db.Column(db.String(), unique=False, nullable=False)
    lastname = db.Column(db.String(), unique=False, nullable=False)
    date_of_birth = db.Column(db.DateTime(), nullable=False)
    confirmation_code = db.Column(db.String(), nullable=False)
    email_confirmed = db.Column(db.Boolean(), nullable=False, default=True)
    challenge = db.Column(db.String(), nullable=False)
    reset_required = db.Column(db.Boolean(), nullable=False, default=True)
    active = db.Column(db.Boolean(), nullable=False, default=True)
    account = db.relationship('Account', backref='credential', lazy=True)
    role_id = db.Column(db.Integer(), unique=True, nullable=False)

    def setup(self, role=0) -> None:
        self.active = False
        self.email_confirmed = False
        self.reset_required = False
        self.role_id = role

    def activate(self) -> None:
        self.active = True
        self.email_confirmed = True
        self.reset_required = False

    @staticmethod
    def get_confirmation_code(code='') -> str:
        now = datetime.now()
        if len(code) > 0:
            return f'{code}{now.strftime("%m%d%Y")}'
        else:
            return f'{str(randrange(10000, 100000))}{now.strftime("%m%d%Y")}'

    def age(self) -> int:
        now = datetime.now()
        today = now.date()
        return relativedelta(today, self.date_of_birth).years

    def name(self):
        return f'{self.firstname} {self.lastname}'


class Account(db.Model, OnlineManagerModel):
    __tablename__ = 'account'
    id = db.Column(db.Integer(), primary_key=True)
    nickname = db.Column(db.String(), nullable=True)
    credential_id = db.Column(db.Integer(), db.ForeignKey(
        'credential.id'), unique=True, nullable=False)
    teams = db.relationship('Team', backref='account', lazy=True)

    def format(self) -> dict:
        return {'id': self.id, 'email': self.credential.email}


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
    bids = db.relationship('Bid', backref='team', lazy=True)

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
            self.name = f'{choice(cities).name} {configuration.get_teamsuffix()} {randrange(1000,9999)}'

    def value(self) -> int:
        val = 0
        for p in self.players:
            val += p.value
        return val

    def format(self) -> dict:
        return {'id': self.id,
                'account_id': self.account_id,
                'account': self.account.nickname,
                'budget': self.budget,
                'country_id': self.country_id,
                'country': self.country.name,
                'name': self.name,
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
    transfers = db.relationship('Transfer', backref='player', lazy=True)

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

    def name(self) -> str:
        return f'{self.firstname} {self.lastname}'

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


class Transfer(db.Model, OnlineManagerModel):
    __tablename__ = 'transfer'
    id = db.Column(db.Integer(), primary_key=True)
    player_id = db.Column(db.Integer(), db.ForeignKey(
        'player.id'), nullable=False)
    from_team_id = db.Column(db.Integer(), db.ForeignKey(
        'team.id'), nullable=False)
    to_team_id = db.Column(db.Integer(), db.ForeignKey(
        'team.id'), nullable=True)
    transfer_value = db.Column(db.Numeric(), nullable=False)
    value_increase = db.Column(db.Integer(), nullable=True)
    date_listed = db.Column(db.DateTime(), nullable=False)
    date_completed = db.Column(db.DateTime(), nullable=True)
    bids = db.relationship('Bid', backref='transfer', lazy=True)

    from_team = db.relationship("Team", foreign_keys=[from_team_id])
    to_team = db.relationship("Team", foreign_keys=[to_team_id])

    def setup(self) -> None:
        self.date_listed = datetime.now()

    def format(self) -> dict:
        return {'id': self.id,
                'player_id': self.player_id,
                'player': self.player.name(),
                'from_team_id': self.from_team_id,
                'to_team_id': self.to_team_id,
                'transfer_value': self.transfer_value,
                'value_increase': self.value_increase,
                'date_listed': self.date_listed,
                'date_completed': self.date_completed}


class Bid(db.Model, OnlineManagerModel):
    __tablename__ = 'bid'
    id = db.Column(db.Integer(), primary_key=True)
    transfer_id = db.Column(
        db.Integer(), db.ForeignKey('transfer.id'), nullable=False)
    team_id = db.Column(db.Integer(), db.ForeignKey(
        'team.id'), nullable=False)
    bid_value = db.Column(db.Numeric(), nullable=False)
    date_of_bid = db.Column(db.DateTime(), nullable=False)
    selected = db.Column(db.Boolean(), nullable=False, default=False)

    def setup(self) -> None:
        now = datetime.now()
        self.date_of_bid = now.date()
        self.selected = False

    def format(self) -> dict:
        return {
            'id': self.id,
            'transfer_id': self.transfer_id,
            'team_id': self.team_id,
            'bid_value': self.bid_value,
            'date_of_bid': self.date_of_bid
        }
