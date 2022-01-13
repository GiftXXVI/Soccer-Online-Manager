from email import message
from flask import Blueprint
from models import Credential, Account, Transfer, Player
from models import Bid, Team
from flask import request, abort, jsonify
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from datetime import date, datetime
import sqlalchemy
from random import randrange

from utilities import sendmail


bids_bp = Blueprint('bids_bp', __name__)

# bidder


@bids_bp.route('/bids', methods=['GET'])
@jwt_required()
def get_team_bids():
    identity = get_jwt_identity()
    credential = Credential.query.filter(
        Credential.email == identity).one_or_none()
    account = Account.query.filter(
        Account.credential_id == credential.id).one_or_none()
    team = Team.query.filter(Team.account_id == account.id).one_or_none()
    bids = Bid.query.filter(Bid.team_id == team.id).all()
    bids_f = [bid.format() for bid in bids]
    return jsonify({
        'success': True,
        'bids:': bids_f
    })

# owner


@bids_bp.route('/transfers/<int:transfer_id>/bids', methods=['GET'])
@jwt_required()
def get_transfer_bids(transfer_id):
    identity = get_jwt_identity()
    credential = Credential.query.filter(
        Credential.email == identity).one_or_none()
    account = Account.query.filter(
        Account.credential_id == credential.id).one_or_none()
    team = Team.query.filter(Team.account_id == account.id).one_or_none()
    transfer = Transfer.query.filter(Transfer.id == transfer_id).one_or_none()
    player = Player.query.filter(Player.id == transfer.player_id).one_or_none()
    if player.team_id == team.id:
        bids = Bid.query.filter(Bid.transfer_id == transfer_id).all()
        bids_f = [bid.format() for bid in bids]
        return jsonify({
            'success': True,
            'bids': bids_f
        })
    else:
        bid = Bid.query.filter(
            Bid.transfer_id == transfer_id, Bid.team_id == team.id).one_or_none()
        if bid is not None:
            return jsonify({
                'success': True,
                'bids': [bid.format()]
            })
        else:
            abort(401)


@bids_bp.route('/transfers/<int:transfer_id>/bids', methods=['POST'])
@jwt_required()
def create_bid(transfer_id) -> jsonify:
    '''submit a bid on a transfer'''
    request_body = request.get_json()
    identity = get_jwt_identity()
    credential = Credential.query.filter(
        Credential.email == identity).one_or_none()
    account = Account.query.filter(
        Account.credential_id == credential.id).one_or_none()
    team = Team.query.filter(Team.account_id == account.id).one_or_none()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_value = request_body.get('value', None)
        transfer = Transfer.query.filter(
            Transfer.id == transfer_id).one_or_none()
        bids = Bid.query.filter(Bid.team_id == team.id).all()
        if transfer.date_completed == None and \
            len(bids) == 0 and   \
                transfer.from_team_id != team.id:
            bid = Bid(transfer_id=transfer.id,
                      team_id=team.id, bid_value=request_value)
            bid.setup()
            try:
                bid.insert()
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
        else:
            abort(401)


@bids_bp.route('/transfers/<int:transfer_id>/bids', methods=['PATCH'])
@jwt_required()
def modify_bid(transfer_id) -> jsonify:
    '''modify a bid on a transfer'''
    request_body = request.get_json()
    identity = get_jwt_identity()
    credential = Credential.query.filter(
        Credential.email == identity).one_or_none()
    account = Account.query.filter(
        Account.credential_id == credential.id).one_or_none()
    team = Team.query.filter(Team.account_id == account.id).one_or_none()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_value = request_body.get('value', None)
        bid = Bid.query.filter(
            Bid.transfer_id == transfer_id, Bid.team_id == team.id).one_or_none()
        if bid.transfer.date_completed == None and \
                bid.transfer.from_team_id != team.id:
            try:
                bid.bid_value = request_value
                bid.apply()
            except sqlalchemy.exc.SQLAlchemyError as e:
                bid.rollback()
                error_state = True
            finally:
                bid_id = bid.id
                bid.dispose()
                if error_state:
                    abort(500)
                else:
                    return jsonify({
                        'success': True,
                        'modified': bid_id
                    })
        else:
            abort(401)


@bids_bp.route('/bids/select/<int:bid_id>', methods=['PATCH'])
@jwt_required()
def select_bid(bid_id) -> jsonify:
    '''select a bid'''
    error_state = False
    identity = get_jwt_identity()
    credential = Credential.query.filter(
        Credential.email == identity).one_or_none()
    account = Account.query.filter(
        Account.credential_id == credential.id).one_or_none()
    team = Team.query.filter(Team.account_id == account.id).one_or_none()

    selected_bid = Bid.query.filter(
        Bid.id == bid_id).one_or_none()

    transfer = Transfer.query.filter(
        Transfer.id == selected_bid.transfer_id).one_or_none()

    other_bids = Bid.query.filter(
        Bid.transfer_id == transfer.id, Bid.id != selected_bid.id).all()

    if transfer.from_team_id == team.id and \
            selected_bid.team_id != team.id and \
            team.id not in [bid.team_id for bid in other_bids] and \
            transfer.date_completed == None:
        try:
            # update transfer
            transfer.bid_selected()
            transfer.stage()

            # update selected bid
            selected_bid.selected = True
            selected_bid.stage()

            # update other bids
            for bid in other_bids:
                bid.selected = False
                bid.stage()

            # commit
            transfer.apply()

            # send email
            now = datetime.now()
            f_now = now.strftime("%Y-%m-%d %H:%M:%S")
            f_name = transfer.player.name()
            message = f'Your bid for the player {f_name}' + \
                f'has been selected at {f_now}. \n' + \
                'Please confirm the transfer to complete the transaction.'
            to_team = Team.query.filter(
                Team.id == selected_bid.team_id).one_or_none()
            to_account = Account.query.filter(
                Account.id == to_team.account_id).one_or_none()
            address = Credential.query.filter(
                Credential.id == to_account.credential_id).one_or_none()

            sendmail(address.email, message)
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
    else:
        abort(401)


@bids_bp.route('/bids/confirm/<int:bid_id>', methods=['PATCH'])
@jwt_required()
def confirm_transfer(bid_id) -> jsonify:
    '''confirm transfer to complete'''
    identity = get_jwt_identity()
    credential = Credential.query.filter(
        Credential.email == identity).one_or_none()
    account = Account.query.filter(
        Account.credential_id == credential.id).one_or_none()
    to_team = Team.query.filter(Team.account_id == account.id).one_or_none()

    bid = Bid.query.filter(
        Bid.id == bid_id).one_or_none()
    transfer = Transfer.query.filter(
        Transfer.id == bid.transfer_id).one_or_none()
    from_team = Team.query.filter(
        Team.id == transfer.from_team_id).one_or_none()
    error_state = False

    if bid is None:
        abort(400)
    if bid.selected == True and \
        transfer.id == bid.transfer_id and \
        bid.team_id == to_team.id and \
        transfer.from_team_id != to_team.id and \
            transfer.date_completed == None:
        try:
            player_value = bid.bid_value

            transfer.transfer_confirmed(player_value, to_team.id)
            transfer.stage()

            transfer.apply()
            now = datetime.now()
            f_now = now.strftime("%Y-%m-%d %H:%M:%S")
            message = f'The transfer of the player {transfer.player.name()}' + \
                f'has been confirmed at {f_now}.'

            from_address = Credential.query.filter(
                Credential.id == from_team.account.credential_id).one_or_none()

            sendmail(from_address.email, message)

        except sqlalchemy.exc.SQLAlchemyError as e:
            transfer.rollback()
            error_state = True
        finally:
            bid_id = bid.id
            transfer.dispose()
            if error_state:
                abort(500)
            else:
                return jsonify({
                    'success': True,
                    'modified': bid_id
                })
    else:
        abort(401)


@bids_bp.route('/bids/<int:bid_id>', methods=['DELETE'])
@jwt_required()
def delete_bid(bid_id) -> jsonify:
    '''delete a bid on a transfer'''
    identity = get_jwt_identity()
    credential = Credential.query.filter(
        Credential.email == identity).one_or_none()
    account = Account.query.filter(
        Account.credential_id == credential.id).one_or_none()
    team = Team.query.filter(Team.account_id == account.id).one_or_none()
    error_state = False

    bid = Bid.query.filter(
        Bid.id == bid_id, Bid.team_id == team.id).one_or_none()
    if bid is None:
        abort(400)
    if bid.transfer.date_completed == None and \
            bid.transfer.from_team_id != team.id:
        try:
            bid.delete()
            bid.apply()
        except sqlalchemy.exc.SQLAlchemyError as e:
            bid.rollback()
            error_state = True
        finally:
            bid_id = bid.id
            bid.dispose()
            if error_state:
                abort(500)
            else:
                return jsonify({
                    'success': True,
                    'deleted': bid_id
                })
    else:
        abort(401)
