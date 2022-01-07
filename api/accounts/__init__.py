from os import error
from flask import Blueprint
from models import Account, Player, Position, Team
from flask import request, abort, jsonify
import sqlalchemy

accounts_bp = Blueprint('accounts_bp', __name__)


@accounts_bp.route('/accounts', methods=['GET'])
def get_accounts():
    accounts = Account.query.all()
    accounts_f = [account.format() for account in accounts]
    return jsonify({
        'success': True,
        'accounts': accounts_f
    })


@accounts_bp.route('/accounts', methods=['POST'])
def create_account() -> jsonify:
    '''create a user account with a team with players included.'''
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_email = request_body.get('email', None)
        request_country = request_body.get('country', None)
        # add email validation
        if request_email is None or request_country is None:
            abort(400)
        else:
            account = Account(email=request_email)
            try:
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
