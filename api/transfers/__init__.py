from flask import Blueprint
from models import Transfer
from flask import request, abort, jsonify
import sqlalchemy

transfers_bp = Blueprint('transfers_bp', __name__)


@transfers_bp.route('/transfers', methods=['GET'])
def get_transfers() -> jsonify:
    '''get a list of transfers'''
    transfers = Transfer.query.all()
    transfers_f = [transfer.format() for transfer in transfers]
    return jsonify({
        'success': True,
        'accounts': transfers_f
    })


@transfers_bp.route('/transfers', methods=['POST'])
def create_transfer() -> jsonify:
    '''create a transfer'''
    request_body = request.get_json()
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
            transfer = Transfer(
                player_id=request_player,
                from_team_id=request_from_team,
                transfer_value=request_transfer_value)
            try:
                transfer.setup()
                transfer.apply()
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


@transfers_bp.route('/transfers/<int:transfer_id>', methods=['PATCH'])
def modify_transfer(transfer_id):
    '''modify a transfer value'''
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
                if not (transfer.date_completed is None):
                    try:
                        transfer.value = request_value
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
                    abort(500)


@transfers_bp.route('/transfers/<int:transfer_id>', methods=['DELETE'])
def delete_transfer(transfer_id) -> jsonify:
    '''delete a transfer'''
    error_state = False
    transfer = Transfer.query.filter(Transfer.id == transfer_id).one_or_none()
    if transfer is None:
        abort(400)
    else:
        try:
            if not (transfer.date_completed is None):
                transfer.delete()
                transfer.apply()
            else:
                abort(400)
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
