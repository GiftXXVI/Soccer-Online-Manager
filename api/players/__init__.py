from flask import Blueprint
from models import Player, Credential
import sqlalchemy
from flask import request, abort, jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_jwt_extended import jwt_required

players_bp = Blueprint('players_bp', __name__)


@players_bp.route('/players', methods=['GET'])
@jwt_required()
def get_players() -> jsonify:
    '''get a list of players'''
    identity = get_jwt_identity()
    claims = get_jwt()
    if claims['sm_role'] == 1:
        players = Player.query.all()
        players_f = [player.format() for player in players]
        return jsonify({
            'success': True,
            'players': players_f
        })
    else:
        abort(401)


@players_bp.route('/players/<int:player_id>', methods=['GET'])
@jwt_required()
def get_player(player_id) -> jsonify:
    '''get a player by id'''
    identity = get_jwt_identity()
    credential = Credential.query.filter(
        Credential.email == identity).one_or_none()
    player = Player.query.filter(Player.id == player_id).one_or_none()
    if player is None:
        abort(404)
    else:
        if player.team.account.credential_id == credential.id:
            return jsonify({
                'success': True,
                'player': player.format()
            })
        else:
            abort(401)


@players_bp.route('/players/<int:player_id>', methods=['PATCH'])
@jwt_required()
def modify_player(player_id) -> jsonify:
    '''modify a player name'''
    identity = get_jwt_identity()
    credential = Credential.query.filter(
        Credential.email == identity).one_or_none()
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_firstname = request_body.get('firstname', None)
        request_lastname = request_body.get('lastname', None)
        if request_firstname is None or request_lastname is None:
            abort(400)
        else:
            player = Player.query.filter(Player.id == player_id).one_or_none()
            if player.team.account.credential_id == credential.id:
                if player is None:
                    abort(400)
                else:
                    try:
                        player.firstname = request_firstname
                        player.lastname = request_lastname
                        player.apply()
                    except sqlalchemy.exc.SQLAlchemyError as e:
                        player.rollback()
                        error_state = True
                    finally:
                        player.dispose()
                        if error_state:
                            abort(500)
                        else:
                            return ({
                                'success': True,
                                'modified': player_id
                            })
            else:
                abort(401)
