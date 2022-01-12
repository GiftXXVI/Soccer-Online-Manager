from flask import Blueprint
from models import Team, Player, Account, Credential
import sqlalchemy
from flask import request, abort, jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_jwt_extended import jwt_required

teams_bp = Blueprint('teams_bp', __name__)


@teams_bp.route('/teams', methods=['GET'])
@jwt_required()
def get_teams() -> jsonify:
    '''get a list of all teams'''
    identity = get_jwt_identity()
    claims = get_jwt()
    if claims['sm_role'] == 1:
        teams = Team.query.all()
        teams_f = [team.format() for team in teams]
        return jsonify({
            'success': True,
            'teams': teams_f
        })
    else:
        abort(401)


@teams_bp.route('/teams/<int:team_id>', methods=['GET'])
@jwt_required()
def get_team(team_id) -> jsonify:
    '''get a team by id'''
    identity = get_jwt_identity()
    credential = Credential.query.filter(
        Credential.email == identity).one_or_none()
    team = Team.query.filter(Team.id == team_id).one_or_none()
    if team is None:
        abort(404)
    else:
        if team.account.credential_id == credential.id:
            return jsonify({
                'success': True,
                'team': team.format()
            })
        else:
            abort(401)


@teams_bp.route('/teams/<int:team_id>/players', methods=['GET'])
@jwt_required()
def get_players(team_id) -> jsonify:
    '''get a list of team players'''
    identity = get_jwt_identity()
    credential = Credential.query.filter(
        Credential.email == identity).one_or_none()
    team = Team.query.filter(Team.id == team_id).one_or_none()
    players = Player.query.filter(Player.team_id == team_id).all()
    players_f = [player.format() for player in players]
    if team.account.credential_id == credential.id:
        return jsonify({
            'success': True,
            'players': players_f
        })
    else:
        abort(401)


@teams_bp.route('/teams/<int:team_id>', methods=['PATCH'])
@jwt_required()
def modify_team(team_id):
    '''modify a team name'''
    identity = get_jwt_identity()
    credential = Credential.query.filter(
        Credential.email == identity).one_or_none()
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
                if team.account.credential_id == credential.id:
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
                else:
                    abort(401)
