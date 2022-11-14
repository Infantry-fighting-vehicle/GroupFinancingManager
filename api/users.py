from flask import Blueprint, request, Response, redirect, url_for
from sqlalchemy import create_engine
from api import error_codes
from services.authorization import *

from config.db_connection_info import DB_URL, get_database_session
from models.service import error_codes
from models import *
from bcrypt import checkpw, hashpw, gensalt

Session = get_database_session()
account_api = Blueprint('user_api', __name__)

@account_api.route("", methods=["POST"])
def accountList():
    if request.method == 'POST':
        print(request.get_json())
        request_data = request.get_json()
        user = User(
            username = request_data['username'],
            password = hashpw(bytes(request_data['password'], 'utf-8'), gensalt(14)).decode(),
            first_name = request_data['first_name'],
            last_name = request_data['last_name'],
            card_number = request_data['card_number'],
            phone = request_data['phone'],
            email = request_data['email']
        )
        Session.add(user)
        Session.commit()
        return UserSerializer().dump(user)


# takes login and password as args
@account_api.route("login")
def login():
    if not request.args.get('username') or not request.args.get('password'):
        return {
            'code': error_codes.INVALID_CREDENTIALS,
            'message': 'username of password is invalid'
        }, 400
    user = Session.query(User).filter(User.username == request.args['username']).first()
    if user is not None:
        is_pass_valid = checkpw(bytes(request.args['password'], 'utf-8'), bytes(user.password, 'utf-8'))

        if 'username' in request.args and 'password' in request.args and is_pass_valid:
            return UserSerializer().dump(user)
    
    return {
        'code': error_codes.INVALID_CREDENTIALS,
        'message': 'username of password is invalid'
    }, 400

@account_api.route("logout")
@http_auth.login_required
def logout():
    return redirect(f"http://logout:logout@{request.host}{url_for('user_api.login')}")

@account_api.route("<username>", methods=["GET", "PUT", "DELETE"])
@http_auth.login_required
def getUserBytUsername(username):
    user = Session.query(User).filter(User.username == username).first()
    if user is None:
        return {
            'code': error_codes.NOT_FOUND,
            'message': 'Unauthorized user access'
        }, 404

    if request.method == "PUT":
        if get_current_user().id != user.id:
            return {
                'code': error_codes.UNAUTHORIZED,
                'message': 'Unauthorized user access'
            }, 401
        user_alter = UserInsensetiveSerializer().load(request.get_json())
        for key in user_alter.keys():
            user.__setattr__(key, user_alter[key])
    elif request.method == "DELETE":
        if get_current_user().id != user.id:
            return {
                'code': error_codes.UNAUTHORIZED,
                'message': 'Unauthorized user access'
            }, 401
        Session.delete(user)

    Session.commit()
    return UserSerializer().dump(user)

@account_api.route("testinfo", methods=["GET"])
@http_auth.login_required
def test_get_info():
    return {'Message': 'Success', 'Name': get_current_user().first_name,
        'username_http': http_auth.current_user()}