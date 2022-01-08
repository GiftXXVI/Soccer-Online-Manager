from flask import Blueprint
from models import Account, Player, Position, Team
from flask import request, abort, jsonify
from email.utils import parseaddr
import sqlalchemy

accounts_bp = Blueprint('accounts_bp', __name__)


@accounts_bp.route('/accounts', methods=['GET'])
def get_accounts() -> jsonify:
    '''get a list of user accounts'''
    accounts = Account.query.all()
    accounts_f = [account.format() for account in accounts]
    return jsonify({
        'success': True,
        'accounts': accounts_f
    })


@accounts_bp.route('/accounts/<int:account_id>', methods=['GET'])
def get_account(account_id) -> jsonify:
    '''get a single user account'''
    account = Account.query.filter(Account.id == account_id).one_or_none()
    if account is None:
        abort(404)
    else:
        return jsonify({
            'success': True,
            'account': account.format()
        })


@accounts_bp.route('/accounts/teams/<int:account_id>', methods=['GET'])
def get_teams(account_id):
    teams = Team.query.filter(Team.account_id == account_id).all()
    teams_f = [team.format() for team in teams]
    return jsonify({
        'success': True,
        'teams': teams_f
    })


@accounts_bp.route('/accounts', methods=['POST'])
def create_account() -> jsonify:
    '''create a user account, their team and team players.)'''
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_email = request_body.get('email', None)
        request_country = request_body.get('country', None)
        # add email validation
        if request_email is None or parseaddr(request_email) == ('', '') or request_country is None:
            abort(400)
        else:
            account = Account(email=request_email)
            try:
                account.setup()
                account.insert()
                account.stage()
                team = Team(account_id=account.id, country_id=request_country)
                team.setup()
                team.insert()
                team.stage()
                positions = Position.query.all()
                for position in positions:
                    for i in range(position.initial_players):
                        player = Player(country_id=request_country,
                                        position_id=position.id, team_id=team.id)
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


@accounts_bp.route('/accounts/<int:account_id>', methods=['PATCH'])
def modify_account(account_id) -> jsonify:
    '''modify a user account'''
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_email = request_body.get('email', None)
        request_active = request_body.get('active', None)
        if request_email is None or request_active is None:
            abort(400)
        else:
            account = Account.query.filter(
                Account.id == account_id).one_or_none()
            account.email = request_email
            account.active = bool(request_active)
            try:
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


@accounts_bp.route('/accounts/<int:account_id>', methods=['DELETE'])
def delete_account(account_id) -> jsonify:
    '''delete a user account'''
    error_state = False
    account = Account.query.filter(Account.id == account_id).one_or_none()
    if account is None:
        abort(400)
    else:
        try:
            account.delete()
            account.apply()
        except sqlalchemy.exc.SQLAlchemyError as e:
            account.rollback()
            error_state = True
            print(e)
        finally:
            account.dispose()
            if error_state:
                abort(500)
            else:
                return jsonify({
                    'success': True,
                    'deleted': account_id
                })
