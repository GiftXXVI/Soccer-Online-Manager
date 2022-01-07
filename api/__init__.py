import models
from api.players import players_bp
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.register_blueprint(players_bp)
    CORS(app)
    db, migrate = models.setup_db(app)
    return app, db, migrate


app, db, migrate = create_app()


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Authorization, true')
    response.headers.add(
        'Access-Control-Allow-Methods', 'GET, OPTIONS, PATCH, DELETE, POST')
    return response
