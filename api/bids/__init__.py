from flask import Blueprint
from models import Credential, Account, Transfer
from models import Bid, Team
from flask import request, abort, jsonify
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from datetime import datetime
import sqlalchemy
from random import randrange

bids_bp = Blueprint('bids_bp', __name__)

# bidder


@bids_bp.route('/bids/<int:selected>', methods=['GET'])
@jwt_required()
def get_team_bids(selected):
    identity = get_jwt_identity()
    credential = Credential.query.filter(
        Credential.email == identity).one_or_none()
    account = Account.query.filter(
        Account.credential_id == credential.id).one_or_none()
    team = Team.query.filter(Team.account_id == account.id).one_or_none()
    if selected == 0:
        bids = Bid.query.filter(Bid.team_id == team.id,
                                Bid.selected == True).all()
    elif selected == 1:
        bids = Bid.query.filter(Bid.team_id == team.id,
                                Bid.selected != True).all()
    else:
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
    if transfer.player.team_id == team.id:
        bids = Bid.query.filter(Bid.transfer_id == transfer_id).all()
        bids_f = [bid.format() for bid in bids]
        return jsonify({
            'success': True,
            'bids': bids_f
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
        request_team = request_body.get('team', None)
        request_value = request_body.get('value', None)
        transfer = Transfer.query.filter(
            Transfer.id == transfer_id).one_or_more()
        if transfer.date_completed == None and \
                transfer.from_team_id != team.id:
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
        else:
            abort(401)


@bids_bp.route('/bids/<int:bid_id>', methods=['PATCH'])
@jwt_required()
def modify_bid(bid_id) -> jsonify:
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
        bid = Bid.query.filter(Bid.id == bid_id).one_or_none()
        if bid.transfer.date_completed == None and \
                bid.transfer.from_team_id != team.id:
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
        else:
            abort(401)


@bids_bp.route('/transfer/<int:transfer_id>/bids', methods=['PATCH'])
@jwt_required()
def select_bid(transfer_id) -> jsonify:
    '''select a bid'''
    request_body = request.get_json()
    error_state = False
    identity = get_jwt_identity()
    credential = Credential.query.filter(
        Credential.email == identity).one_or_none()
    account = Account.query.filter(
        Account.credential_id == credential.id).one_or_none()
    team = Team.query.filter(Team.account_id == account.id).one_or_none()
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

        if transfer.id == selected_bid.transfer_id and \
            transfer.team_id == team.id and \
                transfer.date_completed == None:
            try:
                transfer.value_increase = randrange(110, 201)
                transfer.stage()
                selected_bid.selected_bid = True
                selected_bid.stage()
                for bid in other_bids:
                    bid.selected_bid = False
                    bid.stage()
                transfer.apply()
                now = datetime.now()
                msg = EmailMessage()
                msg.set_content(
                    f'''Your bid for the player {} has been accepted at {now.strftime("%Y-%m-%d %H:%M:%S")}.
                    Please confirm the transfer to complete the transaction.
                    '''
                )
                msg['Subject'] = f'Please confirm your email address.'
                msg['From'] = 'no-reply@soccermanager.local'
                msg['To'] = identity
                s = smtplib.SMTP(host='localhost', port=8025)
                s.send_message(msg)
                s.quit()
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


@bids_bp.route('/transfers/<int:transfer_id>/bids', methods=['DELETE'])
@jwt_required()
def confirm_transfer(transfer_id) -> jsonify:
    '''confirm transfer to complete'''
    request_body = request.get_json()
    identity = get_jwt_identity()
    credential = Credential.query.filter(
        Credential.email == identity).one_or_none()
    account = Account.query.filter(
        Account.credential_id == credential.id).one_or_none()
    to_team = Team.query.filter(Team.account_id == account.id).one_or_none()
    if request_body is None:
        abort(400)
    else:
        request_bid = request_body.get('bid_id', None)
        request_confirmed = request_body.get('confirmed', None)
        if request_confirmed is None or request_bid is None:
            abort(400)
        transfer = Transfer.query.filter(
            Transfer.id == transfer_id).one_or_none()
        from_team = Team.query.filter(
            Team.id == transfer.from_team_id).one_or_none()
        bid = Bid.query.filter(
            Bid.id == request_bid).one_or_none()
        if bid.selected_bid == True and \
            transfer.id == bid.transfer_id and \
            transfer.from_team_id != team.id and \
                transfer.date_completed == None:
            try:
                if request_confirmed==True:
                    now = datetime.now()
                    transfer.date_completed = now.date()
                    player_value = bid.value + \
                        (bid.value*transfer.value_increase)
                    transfer.transfer_value = player_value
                    transfer.to_team_id=to_team.id
                    transfer.player.value = player_value
                    transfer.stage()

                    team.value += player_value
                    team.stage()

                    from_team.value -= player_value
                    from_team.stage()

                    transfer.apply()
                    now = datetime.now()
                    msg = EmailMessage()
                    msg.set_content(
                        f'''The trnasfer of the player {} has been confirmed at {now.strftime("%Y-%m-%d %H:%M:%S")}.
                        '''
                    )
                    msg['Subject'] = f'Please confirm your email address.'
                    msg['From'] = 'no-reply@soccermanager.local'
                    msg['To'] = identity
                    s = smtplib.SMTP(host='localhost', port=8025)
                    s.send_message(msg)
                    s.quit()
                else:
                    transfer.date_completed = None
                    bid.selected_bid = False
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

    bid = Bid.query.filter(Bid.id == bid_id).one_or_none()
    if bid.transfer.date_completed == None and \
            bid.transfer.from_team_id != team.id:
        try:
            bid.delete()
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
    else:
        abort(401)
