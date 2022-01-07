from os import error
from typing import final
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from models import Country
from flask import request, abort, jsonify

countries_bp = Blueprint('countries_bp', __name__)


@countries_bp.route('/countries', methods=['GET'])
def get_countries() -> jsonify:
    '''get a list of all countries'''
    countries = Country.query.all()
    countries_f = [country.format() for country in countries]
    return jsonify({
        'success': True,
        'countries': countries_f
    })


@countries_bp.route('/countries/<int:country_id>', methods=['GET'])
def get_country(country_id) -> jsonify:
    country = Country.query.filter(Country.id == country_id).one_or_none()
    if country is None:
        abort(404)
    else:
        return jsonify({
            'success': True,
            'country': country.format()
        })


@countries_bp.route('/countries', methods=['POST'])
def create_country() -> jsonify:
    '''create a country'''
    request_body = request.get_json()
    error_state = False
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


@countries_bp.route('/countries/<int:country_id>', methods=['PATCH'])
def modify_country(country_id) -> jsonify:
    '''modify a country name'''
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_name = request_body.get('name', None)
        if request_name is None:
            abort(400)
        else:
            country = Country.query.filter(
                Country.id == country_id).one_or_none()
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


@countries_bp.route('/countries/<int:country_id>', methods=['DELETE'])
def delete_country(country_id) -> jsonify:
    '''delete a country'''
    error_state = False
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
