from flask import Blueprint
from models import Transfer, Bid
from flask import request, abort, jsonify
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from datetime import datetime
import sqlalchemy
from random import randrange

bids_bp = Blueprint('bids_bp', __name__)

# bidder


@bids_bp.route('/teams/<int:team_id>/bids', methods=['GET'])
@jwt_required()
def get_team_bids(team_id):
    bids = Bid.query.filter(Bid.team_id == team_id).all()
    bids_f = [bid.format() for bid in bids]
    return jsonify({
        'success': True,
        'bids:': bids_f
    })

# owner


@bids_bp.route('/transfers/<int:transfer_id>/bids', methods=['GET'])
@jwt_required()
def get_transfer_bids(transfer_id):
    bids = Bid.query.filter(Bid.transfer_id == transfer_id).all()
    bids_f = [bid.format() for bid in bids]
    return jsonify({
        'success': True,
        'bids': bids_f
    })


@bids_bp.route('/transfers/<int:transfer_id>/bids', methods=['POST'])
@jwt_required()
def create_bid(transfer_id) -> jsonify:
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
@jwt_required()
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


@bids_bp.route('/transfer/<int:transfer_id>/bids', methods=['PATCH'])
@jwt_required()
def select_bid(transfer_id) -> jsonify:
    '''select a bid'''
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_selected = request_body.get('selected', None)
        if request_selected is None:
            abort(400)
        transfer = Transfer.query.filter(
            Transfer.id == transfer_id).one_or_none()
        selected_bid = Bid.query.filter(
            Bid.id == request_selected).one_or_none()
        other_bids = Bid.query.filter(
            Bid.transfer_id == transfer_id and Bid.id != request_selected).all()
        now = datetime.now()
        try:
            transfer.value_increase = (
                100 + randrange(10, 101)) * max(transfer.value, transfer.player.value)
            transfer.date_completed = now.date()
            transfer.stage()
            selected_bid.selected_bid = True
            selected_bid.stage()
            for bid in other_bids:
                bid.selected = False
                bid.stage()
            transfer.apply()
        except sqlalchemy.exc.SQLAlchemyError as e:
            transfer.rollback()
            error_state = True
        finally:
            transfer.dispose()
            if error_state:
                abort(500)
            else:
                return jsonify({
                    'success': True,
                    'modified': transfer.id
                })
