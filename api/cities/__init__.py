from flask import Blueprint
import sqlalchemy
from models import City, Country
from flask import request, abort, jsonify

cities_bp = Blueprint('cities_bp', __name__)


@cities_bp.route('/cities', methods=['GET'])
@jwt_required()
def get_cities() -> jsonify:
    '''get a list of cities'''
    cities = City.query.all()
    cities_f = [city.format() for city in cities]
    return jsonify({
        'success': True,
        'cities': cities_f
    })


@cities_bp.route('/cities/<int:city_id>', methods=['GET'])
@jwt_required()
def get_city(city_id) -> jsonify:
    '''get a city by id'''
    city = City.query.filter(City.id == city_id).one_or_none()
    if city is None:
        abort(404)
    else:
        return jsonify({
            'success': True,
            'city': city.format()
        })


@cities_bp.route('/cities', methods=['POST'])
@jwt_required()
def create_city() -> jsonify:
    '''create a city'''
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_name = request_body.get('name', None)
        request_country = request_body.get('country_id', None)
        if request_name is None or request_country is None:
            abort(400)
        else:
            city = City(name=request_name, country_id=request_country)
            try:
                city.insert()
                city.apply()
                city.refresh()
            except sqlalchemy.exc.SQLAlchemyError as e:
                city.rollback()
                error_state = True
            finally:
                id = city.id
                city.dispose()
                if error_state:
                    abort(500)
                else:
                    return jsonify({
                        'success': True,
                        'created': id
                    })


@cities_bp.route('/cities/<int:city_id>', methods=['PATCH'])
@jwt_required()
def modify_city(city_id) -> jsonify:
    '''modify a city name and country'''
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_name = request_body.get('name', None)
        request_country = request_body.get('country_id', None)
        if request_name is None:
            abort(400)
        else:
            city = City.query.filter(
                City.id == city_id).one_or_none()
            if city is None:
                abort(400)
            else:
                try:
                    city.name = request_name
                    city.country_id = request_country
                    city.apply()
                except sqlalchemy.exc.SQLAlchemyError as e:
                    city.rollback()
                    error_state = True
                finally:
                    city.dispose()
                    if error_state:
                        abort(500)
                    else:
                        return jsonify({
                            'success': True,
                            'modified': city_id
                        })


@cities_bp.route('/cities/<int:city_id>', methods=['DELETE'])
@jwt_required()
def delete_city(city_id) -> jsonify:
    '''delete a city'''
    error_state = False
    city = City.query.filter(City.id == city_id).one_or_none()
    if city is None:
        abort(400)
    else:
        try:
            city.delete()
            city.apply()
        except sqlalchemy.exc.SQLAlchemyError as e:
            city.rollback()
            error_state = True
        finally:
            city.dispose()
            if error_state:
                abort(500)
            else:
                return jsonify({
                    'success': True,
                    'deleted': city_id
                })
