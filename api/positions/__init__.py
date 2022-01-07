from flask import Blueprint
import sqlalchemy
from models import Position
from flask import request, abort, jsonify

positions_bp = Blueprint('positions_bp', __name__)


@positions_bp.route('/positions', methods=['GET'])
def get_positions() -> jsonify:
    '''get a list of all countries'''
    positions = Position.query.all()
    positions_f = [position.format() for position in positions]
    return jsonify({
        'success': True,
        'positions': positions_f
    })


@positions_bp.route('/positions/<int:position_id>', methods=['GET'])
def get_position(position_id) -> jsonify:
    '''get a position by its id'''
    position = Position.query.filter(Position.id == position_id).one_or_none()
    if position is None:
        abort(404)
    else:
        return jsonify({
            'success': True,
            'position': position.format()
        })


@positions_bp.route('/positions', methods=['POST'])
def create_position() -> jsonify:
    '''create a position'''
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_name = request_body.get('name', None)
        request_initial_players = request_body.get('initial_players', None)
        if request_name is None or request_initial_players is None:
            abort(400)
        else:
            position = Position(name=request_name,
                                initial_players=request_initial_players)
            try:
                position.insert()
                position.apply()
                position.refresh()
            except sqlalchemy.exc.SQLAlchemyError as e:
                position.rollback()
                error_state = True
            finally:
                position.dispose()
                if error_state:
                    abort(500)
                else:
                    return jsonify({
                        'success': True,
                        'created': position.id
                    })


@positions_bp.route('/positions/<int:position_id>', methods=['PATCH'])
def modify_position(position_id) -> jsonify:
    '''modify a position name and initial players'''
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_name = request_body.get('name', None)
        request_initial_players = request_body.get('initial_players', None)
        if request_name is None or request_initial_players is None:
            abort(400)
        else:
            position = Position.query.filter(
                Position.id == position_id).one_or_none()
            try:
                position.name = request_name
                position.initial_players = request_initial_players
                position.apply()
            except sqlalchemy.exc.SQLAlchemyError as e:
                position.rollback()
                error_state = True
            finally:
                position.dispose()
                if error_state:
                    abort(500)
                else:
                    return jsonify({
                        'success': True,
                        'modified': position_id
                    })

@positions_bp.route('/positions/<int:position_id>', methods=['DELETE'])
def delete_position(position_id) -> jsonify:
    '''delete a position'''
    error_state = False
    position = Position.query.filter(Position.id == position_id).one_or_none()
    if position is None:
        abort(400)
    else:
        try:
            position.delete()
            position.apply()
        except sqlalchemy.exc.SQLAlchemyError as e:
            position.rollback()
            error_state = True
        finally:
            position.dispose()
            if error_state:
                abort(500)
            else:
                return jsonify({
                    'success': True,
                    'deleted': position_id
                })