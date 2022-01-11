from flask import Blueprint
import sqlalchemy
from models import Country, City
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_jwt_extended import jwt_required
from flask import request, abort, jsonify

countries_bp = Blueprint('countries_bp', __name__)


@countries_bp.route('/countries', methods=['GET'])
@jwt_required()
def get_countries() -> jsonify:
    '''get a list of countries'''
    countries = Country.query.all()
    countries_f = [country.format() for country in countries]
    return jsonify({
        'success': True,
        'countries': countries_f
    })


@countries_bp.route('/countries/cities/<int:country_id>', methods=['GET'])
@jwt_required()
def get_cities(country_id) -> jsonify:
    '''get a list of cities in a country'''
    cities = City.query.filter(City.country_id == country_id).all()
    cities_f = [city.format() for city in cities]
    return jsonify({
        'success': True,
        'cities': cities_f
    })


@countries_bp.route('/countries/<int:country_id>', methods=['GET'])
@jwt_required()
def get_country(country_id) -> jsonify:
    '''get a country by id'''
    country = Country.query.filter(Country.id == country_id).one_or_none()
    if country is None:
        abort(404)
    else:
        return jsonify({
            'success': True,
            'country': country.format()
        })


@countries_bp.route('/countries', methods=['POST'])
@jwt_required()
def create_country() -> jsonify:
    '''create a country'''
    request_body = request.get_json()
    error_state = False
    claims = get_jwt()
    if claims['sm_role'] == 1:
        if request_body is None:
            abort(400)
        else:
            request_name = request_body.get('name', None)
            if request_name is None:
                abort(400)
            else:
                country = Country(name=request_name)
                try:
                    country.insert()
                    country.apply()
                    country.refresh()
                except sqlalchemy.exc.SQLAlchemyError as e:
                    country.rollback()
                    error_state = True
                finally:
                    country.dispose()
                    if error_state:
                        abort(500)
                    else:
                        return jsonify({
                            'success': True,
                            'created': country.id
                        })
    else:
        abort(401)


@countries_bp.route('/countries/<int:country_id>', methods=['PATCH'])
@jwt_required()
def modify_country(country_id) -> jsonify:
    '''modify a country name'''
    request_body = request.get_json()
    error_state = False
    claims = get_jwt()
    if claims['sm_role'] == 1:
        if request_body is None:
            abort(400)
        else:
            request_name = request_body.get('name', None)
            if request_name is None:
                abort(400)
            else:
                country = Country.query.filter(
                    Country.id == country_id).one_or_none()
                if country is None:
                    abort(400)
                else:
                    try:
                        country.name = request_name
                        country.apply()
                    except sqlalchemy.exc.SQLAlchemyError as e:
                        country.rollback()
                        error_state = True
                    finally:
                        country.dispose()
                        if error_state:
                            abort(500)
                        else:
                            return jsonify({
                                'success': True,
                                'modified': country_id
                            })
    else:
        abort(401)


@countries_bp.route('/countries/<int:country_id>', methods=['DELETE'])
@jwt_required()
def delete_country(country_id) -> jsonify:
    '''delete a country'''
    error_state = False
    claims = get_jwt()
    if claims['sm_role'] == 1:
        country = Country.query.filter(Country.id == country_id).one_or_none()
        if country is None:
            abort(400)
        else:
            try:
                country.delete()
                country.apply()
            except sqlalchemy.exc.SQLAlchemyError as e:
                country.rollback()
                error_state = True
            finally:
                country.dispose()
                if error_state:
                    abort(500)
                else:
                    return jsonify({
                        'success': True,
                        'deleted': country_id
                    })
    else:
        abort(401)
