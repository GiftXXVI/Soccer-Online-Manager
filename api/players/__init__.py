from flask import Blueprint
from models import Player
from flask import request, abort, jsonify

players_bp = Blueprint('players_bp', __name__)

@players_bp.route('/players/<int:team_id>', methods=['GET'])
def get_players(team_id):
    return 'Success'