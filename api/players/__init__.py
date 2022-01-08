from flask import Blueprint
from models import Player
from flask import request, abort, jsonify

players_bp = Blueprint('players_bp', __name__)


@players_bp.route('/players/<int:player_id>', methods=['GET'])
def get_player(player_id):
    player = Player.query.filter(Player.id == player_id).one_or_none()
    if player is None:
        abort(404)
    else:
        return jsonify({
            'success': True,
            'player': player.format()
        })

@players_bp.route('/players/<int:player_id>', methods=['PATCH'])
def modify_player(player_id):
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_firstname = request_body.get('firstname',None)
        request_lastname = request_body.get('firstname',None)
        
