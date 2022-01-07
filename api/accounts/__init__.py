from flask import Blueprint
from models import Account, Player, Position, Team
from flask import request, abort, jsonify

accounts_bp = Blueprint('accounts_bp', __name__)


@accounts_bp.route('/accounts/', methods=['POST'])
def create_account() -> jsonify:
    '''create a user account with a team with players included.'''
    request_body = request.get_json()
    if request_body is None:
        abort(400)
    else:
        request_email = request_body.get('email', None)
        request_country = request_body.get('preferred_country', None)
        # add email validation
        if request_email is None or request_country is None:
            abort(400)
        else:
            account = Account(email=request_email)
            account.insert()
            account.refresh()
            team = Team(account_id=account.id, country_id=request_country)
            players = list()
            positions = Position.query.all()
            for position in positions:
                for i in range(position.initial_players):
                    # generate values
                    player = Player()
