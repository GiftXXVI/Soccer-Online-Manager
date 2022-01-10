from flask import Blueprint
from models import Transfer, Bid
from flask import request, abort, jsonify
import sqlalchemy

bids_bp = Blueprint('bids_bp', __name__)

# bidder


@bids_bp.route('/teams/<int:team_id>/bids', methods=['GET'])
def get_team_bids(team_id):
    pass

# owner


@bids_bp.route('/transfers/<int:transfer_id>/bids', methods=['GET'])
def get_transfer_bids():
    pass


@bids_bp.route('/transfers/<int:transfer_id>/bids', methods=['POST'])
def bid_on_transfer(transfer_id) -> jsonify:
    '''submit a bid on a transfer'''
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_team = request_body.get('team', None)
        request_value = request_body.get('value', None)
        transfer = Transfer.query.filter(
            Transfer.id == transfer_id).one_or_more()
        if transfer.date_completed is None:
            bid = Bid(transfer_id=transfer.id,
                      team_id=request_team, bid_value=request_value)
            bid.setup()
            try:
                bid.apply()
                bid.refresh()
            except sqlalchemy.exc.SQLAlchemyError as e:
                bid.rollback()
                error_state = True
            finally:
                bid.dispose()
                if error_state:
                    abort(500)
                else:
                    return jsonify({
                        'success': True,
                        'created': bid.id
                    })


@bids_bp.route('/bids/<int:bid_id>', methods=['PATCH'])
def modify_bid(bid_id) -> jsonify:
    '''modify a bid on a transfer'''
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_value = request_body.get('value', None)
        bid = Bid.query.filter(Bid.id == bid_id).one_or_none()
        try:
            bid.apply()
        except sqlalchemy.exc.SQLAlchemyError as e:
            bid.rollback()
            error_state = True
        finally:
            bid.dispose()
            if error_state:
                abort(500)
            else:
                return jsonify({
                    'success': True,
                    'modified': bid_id
                })
