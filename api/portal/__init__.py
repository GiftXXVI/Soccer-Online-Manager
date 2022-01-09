from argon2 import PasswordHasher
from flask import Blueprint
from models import Credential
import sqlalchemy
from flask import request, abort, jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

portal_bp = Blueprint('portal_bp', __name__)


@portal_bp.route('/portal/register', methods=['GET'])
def create_credential() -> jsonify:
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        pass


@portal_bp.route('/portal/confirm', methods=['GET'])
def confirm_credential() -> jsonify:
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        pass


@portal_bp.route('/portal/token', methods=['GET'])
def issue_token() -> jsonify:
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        pass
