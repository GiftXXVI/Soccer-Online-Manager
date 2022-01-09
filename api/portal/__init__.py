from argon2 import PasswordHasher, Type
from flask import Blueprint
from models import Credential
import sqlalchemy
from flask import request, abort, jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from email.utils import parseaddr
from random import randrange
import smtplib
from email.message import EmailMessage

ph = PasswordHasher()

portal_bp = Blueprint('portal_bp', __name__)


@portal_bp.route('/portal/register', methods=['POST'])
def create_credential() -> jsonify:
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_firstname = request_body.get('firstname', None)
        request_lastname = request_body.get('lastname', None)
        request_dob = request_body.get('date_of_birth', None)
        request_password = request_body.get('password', None)
        request_email = request_body.get('email', None)
        parsed_email = parseaddr(request_email)[1]
        condition = request_firstname is not None and \
            request_lastname is not None and \
            request_dob is not None and \
            request_password is not None and \
            request_email is not None and \
            len(parsed_email) > 0
        if not condition:
            print(request_body)
            abort(400)
        else:
            credential = Credential(firstname=request_firstname,
                                    lastname=request_lastname,
                                    date_of_birth=request_dob,
                                    challenge=request_password,
                                    email=request_email)
            credential.setup()
            confirmation_code = str(randrange(10000, 100000))
            credential.confirmation_code = ph.hash(confirmation_code)
            try:
                credential.insert()
                credential.apply()
                credential.refresh()
            except sqlalchemy.exc.SQLAlchemyError as e:
                print(e)
                credential.rollback()
                error_state = True
            finally:
                credential.dispose()
                if error_state:
                    abort(500)
                else:
                    msg = EmailMessage()
                    msg.set_content(
                        f'Please confirm your account. Your code is {confirmation_code}.\n The request id is {credential.id}.')
                    msg['Subject'] = f'Confirm your account.'
                    msg['From'] = 'no-reply@soccermanager.local'
                    msg['To'] = parsed_email
                    s = smtplib.SMTP(host='localhost', port=1025)
                    s.send_message(msg)
                    s.quit()
                    return jsonify({
                        'success': True,
                        'created': credential.id
                    })


@portal_bp.route('/portal/confirm/<int:credential_id>', methods=['GET'])
@jwt_required()
def confirm_credential(credential_id) -> jsonify:
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_code = request_body.get('code', None)
        if request_code is None:
            abort(400)
        else:
            credential = Credential.query.filter(
                Credential.id == Credential).one_or_none()
            if credential is None:
                abort(400)
            else:
                if ph.verify(credential.hash, request_code):
                    try:
                        credential.activate()
                        credential.apply()
                    except sqlalchemy.exc.SQLAlchemyError as e:
                        credential.rollback()
                        error_state = True
                    finally:
                        credential.dispose()
                        if error_state:
                            abort(500)
                        else:
                            return jsonify({
                                'success': True,
                                'activated': credential.id
                            })

                else:
                    abort(400)


@portal_bp.route('/portal/login', methods=['GET'])
def issue_token() -> jsonify:
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        pass


@portal_bp.route('/portal/reset', methods=['GET'])
@jwt_required()
def reset_password() -> jsonify:
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        pass
