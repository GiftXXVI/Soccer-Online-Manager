from flask import Blueprint
from models import Transfer, Credential
from models import Team, Player
from flask import request, abort, jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_jwt_extended import jwt_required
import sqlalchemy

transfers_bp = Blueprint('transfers_bp', __name__)


@transfers_bp.route('/transfers', methods=['GET'])
@jwt_required()
def get_transfers() -> jsonify:
    '''get a list of transfers'''
    identity = get_jwt_identity()
    claims = get_jwt()
    if claims['sm_role'] == 1:
        transfers = Transfer.query.all()
        transfers_f = [transfer.format() for transfer in transfers]
        return jsonify({
            'success': True,
            'accounts': transfers_f
        })
    else:
        abort(401)


@transfers_bp.route('/transfers/state/<int:completed>', methods=['GET'])
@jwt_required()
def get_transfers_state(completed) -> jsonify:
    '''get a list of transfers by state'''
    if completed == 0:
        transfers = Transfer.query.filter(
            Transfer.date_completed == None).all()
    elif completed == 1:
        transfers = Transfer.query.filter(
            Transfer.date_completed != None).all()
    transfers_f = [transfer.format() for transfer in transfers]
    return jsonify({
        'success': True,
        'accounts': transfers_f
    })


@transfers_bp.route('/transfers', methods=['POST'])
@jwt_required()
def create_transfer() -> jsonify:
    '''create a transfer'''
    request_body = request.get_json()
    identity = get_jwt_identity()
    credential = Credential.query.filter(
        Credential.email == identity).one_or_none()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_player = request_body.get('player_id', None)
        request_from_team = request_body.get('from_team_id', None)
        request_transfer_value = request_body.get('transfer_value', None)
        if request_player is None or request_from_team is None or request_transfer_value is None:
            abort(400)
        else:
            player = Player.query.filter(
                Player.id == request_player).one_or_none()
            team = Team.query.filter(
                Team.id == request_from_team).one_or_none()
            player_active_transfers = Transfer.query.filter(
                Transfer.player_id == request_player, Transfer.date_completed is not None).all()
            if player is not None and team is not None:
                if len(player_active_transfers) == 0 and \
                        player.team_id == team.id and \
                        team.account.credential_id == credential.id:
                    transfer = Transfer(
                        player_id=request_player,
                        from_team_id=request_from_team,
                        transfer_value=request_transfer_value)
                    try:
                        transfer.setup()
                        player.transfer_listed=True
                        transfer.insert()
                        transfer.apply()
                        transfer.refresh()
                    except sqlalchemy.exc.SQLAlchemyError as e:
                        transfer.rollback()
                        error_state = True
                    finally:
                        transfer.dispose()
                        if error_state:
                            abort(400)
                        else:
                            return ({
                                'success': True,
                                'created': transfer.id
                            })
                else:
                    abort(401)
            else:
                abort(400)


@transfers_bp.route('/transfers/<int:transfer_id>', methods=['PATCH'])
@jwt_required()
def modify_transfer(transfer_id):
    '''modify a transfer value'''
    identity = get_jwt_identity()
    credential = Credential.query.filter(
        Credential.email == identity).one_or_none()
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_value = request_body.get('value', None)
        if request_value is None:
            abort(400)
        else:
            transfer = Transfer.query.filter(
                Transfer.id == transfer_id).one_or_none()
            if transfer is None:
                abort(400)
            else:
                player = Player.query.filter(
                    Player.id == transfer.player_id).one_or_none()
                team = Team.query.filter(
                    Team.id == transfer.from_team_id).one_or_none()
                if transfer.date_completed == None and \
                        player.team_id == team.id and \
                        team.account.credential_id == credential.id:
                    try:
                        transfer.transfer_value = request_value
                        transfer.apply()
                    except sqlalchemy.exc.SQLAlchemyError as e:
                        transfer.rollback()
                        error_state = True
                    finally:
                        transfer.dispose()
                        if error_state:
                            abort(500)
                        else:
                            return ({
                                'success': True,
                                'modified': transfer_id
                            })
                else:
                    abort(401)


@transfers_bp.route('/transfers/<int:transfer_id>', methods=['DELETE'])
@jwt_required()
def delete_transfer(transfer_id) -> jsonify:
    '''delete a transfer'''
    identity = get_jwt_identity()
    credential = Credential.query.filter(
        Credential.email == identity).one_or_none()
    error_state = False
    transfer = Transfer.query.filter(Transfer.id == transfer_id).one_or_none()
    if transfer is None:
        abort(400)
    else:
        player = Player.query.filter(
            Player.id == transfer.player_id).one_or_none()
        team = Team.query.filter(
            Team.id == transfer.from_team_id).one_or_none()
        if transfer.date_completed == None and \
                player.team_id == team.id and \
                team.account.credential_id == credential.id:
            try:
                transfer.delete()
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
                        'deleted': transfer_id
                    })
        else:
            abort(401)
