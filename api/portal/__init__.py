from argon2 import PasswordHasher, Type
import argon2
from argon2.low_level import error_to_str
from flask import Blueprint
from models import Credential
import sqlalchemy
from flask import request, abort, jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from email.utils import parseaddr
from datetime import datetime, timedelta

from utilities import sendmail

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
        request_role = request_body.get('role', None)
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
                                    email=parsed_email)
            if request_role is not None:
                credential.setup(role=request_role)
            else:
                credential.setup()
            confirmation_code = Credential.get_confirmation_code()
            credential.confirmation_code = ph.hash(confirmation_code)
            credential.challenge = ph.hash(request_password)
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
                    now = datetime.now()
                    f_now = now.strftime("%Y-%m-%d %H:%M:%S")
                    f_code = confirmation_code[:5]
                    message = f'Your account has been created at {f_now}.' + \
                        f'The request id is {credential.id}.' + \
                        f'You are required confirm your email address.' + \
                        f'The confirmation code is {f_code}.'
                    sendmail(credential.email, message)

                    return jsonify({
                        'success': True,
                        'created': credential.id
                    })


@portal_bp.route('/portal/confirm/<int:credential_id>', methods=['POST'])
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
                Credential.id == credential_id).one_or_none()
            if credential is None:
                abort(400)
            else:
                try:
                    ph.verify(
                        credential.confirmation_code,
                        Credential.get_confirmation_code(
                            code=request_code))
                    if ph.check_needs_rehash(credential.confirmation_code):
                        ph.hash(request_code)
                    credential.activate()
                    credential.apply()
                    credential.refresh()
                except sqlalchemy.exc.SQLAlchemyError as e:
                    credential.rollback()
                    error_state = True
                except argon2.exceptions.VerifyMismatchError:
                    error_state = True
                    abort(401)
                finally:
                    credential.dispose()
                    if error_state:
                        abort(500)
                    else:
                        return jsonify({
                            'success': True,
                            'activated': credential.id
                        })


@portal_bp.route('/portal/login', methods=['POST'])
def issue_token() -> jsonify:
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_email = request_body.get('email', None)
        request_challenge = request_body.get('password', None)
        if request_email is None or request_challenge is None:
            abort(400)
        else:
            credential = Credential.query.filter(
                Credential.email == request_email).one_or_none()
            if credential is None:
                abort(401)
            else:
                try:
                    ph.verify(credential.challenge, request_challenge)
                    if ph.check_needs_rehash(credential.challenge):
                        ph.hash(request_challenge)
                    if credential.active and not credential.reset_required:
                        claims = {'sm_role': credential.role_id}
                        token = create_access_token(
                            identity=request_email, expires_delta=timedelta(
                                minutes=60), fresh=True, additional_claims=claims)
                        return jsonify({
                            'success': True,
                            'token': token
                        })
                    else:
                        abort(401)
                except argon2.exceptions.VerifyMismatchError:
                    error_state = True
                    abort(401)


@portal_bp.route('/portal/refresh', methods=['POST'])
@jwt_required()
def refresh_token() -> jsonify:
    request_body = request.get_json()
    identity = get_jwt_identity()
    credential = Credential.query.filter(
        Credential.email == identity).one_or_none()
    if request_body is None:
        abort(400)
    else:
        request_email = request_body.get('email', None)
        request_token = request_body.get('token', None)
        if request_email is None or request_token is None:
            abort(400)
        else:
            identity = get_jwt_identity()
            if request_email == identity:
                claims = {'sm_role': credential.role_id}
                token = create_access_token(
                    identity=identity, expires_delta=timedelta(
                        minutes=60), fresh=False, additional_claims=claims)
                return jsonify({
                    'success': True,
                    'token': token
                })
            else:
                abort(401)


@portal_bp.route('/portal/reset', methods=['PATCH'])
def reset_password() -> jsonify:
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_email = request_body.get('email', None)
        parsed_email = parseaddr(request_email)[1]
        request_password = request_body.get('password', None)
        request_old_password = request_body.get('old_password', None)

        if request_email is None:
            abort(400)
        else:
            credential = Credential.query.filter(
                Credential.email == parsed_email).one_or_none()
            confirmation_code = Credential.get_confirmation_code()
            if request_email is not None and \
                    len(parsed_email) > 0 and \
                    request_password is not None and \
                    request_old_password is not None:

                try:
                    ph.verify(credential.challenge, request_old_password)
                    credential.challenge = ph.hash(request_password)
                    credential.confirmation_code = ph.hash(
                        confirmation_code)
                    credential.apply()
                except sqlalchemy.exc.SQLAlchemyError as e:
                    credential.rollback()
                    error_state = True
                finally:
                    if error_state:
                        abort(500)
                    else:
                        now = datetime.now()
                        f_now = now.strftime("%Y-%m-%d %H:%M:%S")
                        f_code = confirmation_code[:5]
                        message = f'Your password has been reset at {f_now}.' + \
                            f'If you did not initiate this action, use the code {f_code} to set a new password.'
                        sendmail(credential.email, message)
                        return jsonify({
                            'success': True,
                            'reset': credential.id
                        })
            elif request_email is not None and \
                    len(parsed_email) > 0 and \
                    request_password is None and \
                    request_old_password is None:
                confirmation_code = Credential.get_confirmation_code()
                credential.confirmation_code = ph.hash(confirmation_code)
                try:
                    credential.apply()
                except sqlalchemy.exc.SQLAlchemyError as e:
                    credential.rollback()
                    error_state = True
                finally:
                    now = datetime.now()
                    f_now = now.strftime("%Y-%m-%d %H:%M:%S")
                    f_code = confirmation_code[:5]
                    message = f'You have requested a password reset at {f_now}.' + \
                        f'Please use the code {f_code} to set a new password.' + \
                        'Otherwise, ignore this email.'

                    sendmail(credential.email, message)
                    return jsonify({
                        'success': True,
                        'reset': credential.id
                    })
            else:
                abort(400)


@portal_bp.route('/portal/setpassword', methods=['PATCH'])
def confirm_reset_password() -> jsonify:
    request_body = request.get_json()
    error_state = False
    if request_body is None:
        abort(400)
    else:
        request_email = request_body.get('email', None)
        request_challenge = request_body.get('password', None)
        request_code = request_body.get('code', None)
        parsed_email = parseaddr(request_email)[1]
        if request_email is not None and \
                len(parsed_email) > 0 and \
                request_code is not None \
                and request_code is not None:
            credential = Credential.query.filter(
                Credential.email == parsed_email).one_or_none()
            if credential is None:
                abort(401)
            try:
                ph.verify(credential.confirmation_code,
                          Credential.get_confirmation_code(request_code))
                credential.challenge = ph.hash(request_challenge)
                credential.confirmation_code = ph.hash(
                    Credential.get_confirmation_code())
                credential.apply()
            except sqlalchemy.exc.SQLAlchemyError as e:
                credential.rollback()
                error_state = True
            except argon2.exceptions.VerifyMismatchError:
                error_state = True
            finally:
                id = credential.id
                credential.dispose()
                if error_state:
                    abort(500)
                else:
                    now = datetime.now()
                    f_now = now.strftime("%Y-%m-%d %H:%M:%S")
                    message = f'Your password has been reset at {f_now}.' + \
                        f'If you did not initiate this action, please reset your password.'
                    sendmail(credential.email, message)
                    return jsonify({
                        'success': True,
                        'reset': id
                    })
