from flask import Blueprint
from models import Team, Player
from flask import request, abort, jsonify

teams_bp = Blueprint('teams_bp', __name__)


@teams_bp.route('/teams/<int:team_id>', methods=['GET'])
def get_team(team_id) -> jsonify:
    team = Team.query.filter(Team.id == team_id).one_or_none()
    if team is None:
        abort(404)
    else:
        return jsonify({
            'success': True,
            'team': team.format()
        })


@teams_bp.route('/teams/players/<int:team_id>', methods=['GET'])
def get_players(team_id) -> jsonify:
    players = Player.query.filter(Player.team_id == team_id).all()
    players_f = [player.format() for player in players]
    return jsonify({
        'success': True,
        'players': players_f
    })
