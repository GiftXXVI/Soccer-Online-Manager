import models.configuration as configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from dateutil.relativedelta import relativedelta

db = SQLAlchemy()
migrate = Migrate()
defaults = configuration.get_app_settings()


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = configuration.get_db_uri()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    return db, migrate


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
    budget = db.Column(db.Numeric(), nullable=False,
                       default=defaults['INIT_TEAM_BUDGET'])
    country_id = db.Column(db.Integer(), db.ForeignKey(
        'country.id'), nullable=False)
    players = db.relationship('Player', backref='team', lazy=True)

    def value(self):
        val = 0
        for p in self.players:
            val += p.value
        return val

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
    value = db.Column(db.Numeric(), nullable=False,
                      default=defaults['INIT_TEAM_BUDGET'])
    transfer_listed = db.Column(db.Boolean(), nullable=False, default=False)

    def age(self):
        now = datetime.now()
        today = now.date()
        return relativedelta(today, self.date_of_birth).years

    def __repr__(self) -> str:
        return super().__repr__()


class Position(db.Model, OnlineManagerModel):
    __tablename__ = 'position'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    initial_players = db.Column(db.Integer(), nullable=False)
    players = db.relationship('Player', backref='position', lazy=True)

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
