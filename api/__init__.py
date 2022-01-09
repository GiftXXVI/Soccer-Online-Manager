import models
from api.players import players_bp
from api.countries import countries_bp
from api.positions import positions_bp
from api.accounts import accounts_bp
from api.cities import cities_bp
from api.teams import teams_bp
from api.portal import portal_bp
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.register_blueprint(countries_bp)
    app.register_blueprint(positions_bp)
    app.register_blueprint(cities_bp)
    app.register_blueprint(accounts_bp)
    app.register_blueprint(players_bp)
    app.register_blueprint(teams_bp)
    app.register_blueprint(portal_bp)
    CORS(app)
    db, migrate = models.setup_db(app)
    jwt = JWTManager(app)
    return app, db, migrate


app, db, migrate = create_app()


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Authorization, true')
    response.headers.add(
        'Access-Control-Allow-Methods', 'GET, OPTIONS, PATCH, DELETE, POST')
    return response


@app.errorhandler(404)
def error_404(error):
    message = 'not found'
    return jsonify({
        'success': False,
        'error': 404,
        'message': message.lower()
    }), 404


@app.errorhandler(401)
def error_401(error):
    message = 'unauthorized'
    return jsonify({
        'success': False,
        'error': 401,
        'message': message.lower()
    }), 401


@app.errorhandler(403)
def error_403(error):
    message = 'forbidden'
    return jsonify({
        'success': False,
        'error': 403,
        'message': message.lower()
    }), 401


@app.errorhandler(405)
def error_405(error):
    message = 'not allowed'
    return jsonify({
        'success': False,
        'error': 405,
        'message': message.lower()
    }), 405


@app.errorhandler(422)
def error_422(error):
    message = 'unprocessable'
    return jsonify({
        'success': False,
        'error': 422,
        'message': message.lower()
    }), 422


@app.errorhandler(400)
def error_400(error):
    message = 'bad request'
    return jsonify({
        'success': False,
        'error': 400,
        'message': message.lower()
    }), 400


@app.errorhandler(500)
def error_500(error):
    message = 'server error'
    return jsonify({
        'success': False,
        'error': 500,
        'message': message.lower()
    }), 500
