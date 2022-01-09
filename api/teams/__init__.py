from flask import Blueprint
from models import Team, Player
import sqlalchemy
from flask import request, abort, jsonify

teams_bp = Blueprint('teams_bp', __name__)


@teams_bp.route('/teams', methods=['GET'])
def get_teams() -> jsonify:
    '''get a list of all teams'''
    teams = Team.query.all()
    teams_f = [team.format() for team in teams]
    return jsonify({
        'success': True,
        'teams': teams_f
    })


@teams_bp.route('/teams/<int:team_id>', methods=['GET'])
def get_team(team_id) -> jsonify:
    '''get a team by id'''
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
    '''get a list of team players'''
    players = Player.query.filter(Player.team_id == team_id).all()
    players_f = [player.format() for player in players]
    return jsonify({
        'success': True,
        'players': players_f
    })


@teams_bp.route('/teams/<int:team_id>', methods=['PATCH'])
def modify_team(team_id):
    '''modify a team name'''
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_name = request_body.get('name', None)
        if request_name is None:
            abort(400)
        else:
            team = Team.query.filter(Team.id == team_id).one_or_none()
            if team is None:
                abort(400)
            else:
                try:
                    team.name = request_name
                    team.apply()
                except sqlalchemy.exc.SQLAlchemyError as e:
                    team.rollback()
                    error_state = True
                finally:
                    team.dispose()
                    if error_state:
                        abort(500)
                    else:
                        return ({
                            'success': True,
                            'modified': team_id
                        })
