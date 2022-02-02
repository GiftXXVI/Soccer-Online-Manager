from flask import Blueprint
from models import Credential, Account, Player, Position, Team
from flask import request, abort, jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_jwt_extended import jwt_required
import sqlalchemy

accounts_bp = Blueprint('accounts_bp', __name__)


@accounts_bp.route('/accounts', methods=['GET'])
@jwt_required()
def get_accounts() -> jsonify:
    '''get a list of accounts'''
    identity = get_jwt_identity()
    claims = get_jwt()
    if claims['sm_role'] == 1:
        accounts = Account.query.all()
        accounts_f = [account.format() for account in accounts]
        return jsonify({
            'success': True,
            'accounts': accounts_f
        })
    else:
        abort(401)


@accounts_bp.route('/accounts/me', methods=['GET'])
@jwt_required()
def get_my_account() -> jsonify:
    '''get a list of accounts'''
    identity = get_jwt_identity()
    claims = get_jwt()
    credential = Credential.query.filter(
        Credential.email == identity).one_or_none()
    account = Account.query.filter(
        Account.credential_id == credential.id).one_or_none()
    return jsonify({
        'success': True,
        'account': account.format()
    })


@accounts_bp.route('/accounts/<int:account_id>', methods=['GET'])
@jwt_required()
def get_account(account_id) -> jsonify:
    '''get an account by id'''
    identity = get_jwt_identity()
    credential = Credential.query.filter(
        Credential.email == identity).one_or_none()
    account = Account.query.filter(Account.id == account_id).one_or_none()
    if account.credential_id == credential.id:
        if account is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'account': account.format()
            })
    else:
        abort(401)


@accounts_bp.route('/accounts/<int:account_id>/teams', methods=['GET'])
@jwt_required()
def get_teams(account_id):
    '''get team associated with account'''
    identity = get_jwt_identity()
    team = Team.query.filter(Team.account_id == account_id).one_or_none()
    credential = Credential.query.filter(
        Credential.email == identity).one_or_none()
    if team.account.credential_id == credential.id:
        return jsonify({
            'success': True,
            'teams': team.format()
        })
    else:
        abort(401)


@accounts_bp.route('/accounts', methods=['POST'])
@jwt_required()
def create_account() -> jsonify:
    '''create account, team and players.'''
    request_body = request.get_json()
    identity = get_jwt_identity()
    credential = Credential.query.filter(
        Credential.email == identity).one_or_none()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_country = request_body.get('country', None)
        request_nickname = request_body.get('nickname', None)
        if request_country is None:
            abort(400)
        else:
            existing = Account.query.filter(
                Account.credential_id == credential.id).one_or_none()
            if existing is None:
                account = Account(credential_id=credential.id,
                                  nickname=request_nickname)
                try:
                    account.insert()
                    account.stage()
                    team = Team(account_id=account.id,
                                country_id=request_country)
                    team.setup()
                    team.insert()
                    team.stage()
                    positions = Position.query.all()
                    for position in positions:
                        for i in range(position.initial_players):
                            player = Player(
                                country_id=request_country,
                                position_id=position.id,
                                team_id=team.id)
                            player.setup()
                            player.insert()
                            player.stage()
                    account.apply()
                    account.refresh()
                except sqlalchemy.exc.SQLAlchemyError as e:
                    account.rollback()
                    error_state = True
                finally:
                    account.dispose()
                    if error_state:
                        abort(500)
                    else:
                        return jsonify({
                            'success': True,
                            'created': account.id
                        })
            else:
                abort(401)


@accounts_bp.route('/accounts/<int:account_id>', methods=['PATCH'])
@jwt_required()
def modify_account(account_id) -> jsonify:
    '''modify an account'''
    request_body = request.get_json()
    identity = get_jwt_identity()
    credential = Credential.query.filter(
        Credential.email == identity).one_or_none()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_nickname = request_body.get('nickname', None)
        account = Account.query.filter(
            Account.id == account_id,
            Account.credential_id == credential.id).one_or_none()
        if account is None or request_nickname is None:
            abort(400)
        else:
            try:
                account.nickname = request_nickname
                account.apply()
            except sqlalchemy.exc.SQLAlchemyError as e:
                account.rollback()
                error_state = True
            finally:
                account.dispose()
                if error_state:
                    abort(500)
                else:
                    return jsonify({
                        'success': True,
                        'modified': account_id
                    })
