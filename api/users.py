from flask import Blueprint, request, Response
from sqlalchemy import create_engine
from api import error_codes
from services.authorization import authorize

from config.db_connection_info import DB_URL, get_database_session
from models.service import error_codes
from models import *
from bcrypt import checkpw, hashpw, gensalt

Session = get_database_session()
account_api = Blueprint('user_api', __name__)

@account_api.route("", methods=["POST", "GET"])
def accountList():
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

    return user.to_dict()

# takes login and password as args
@account_api.route("login")
def login():
    user = Session.query(User).filter(User.username == request.args['username']).first()
    if user is not None:
        is_pass_valid = checkpw(bytes(request.args['password'], 'utf-8'), bytes(user.password, 'utf-8'))

        if 'username' in request.args and 'password' in request.args and is_pass_valid:
            return {
                'accessToken': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c',
                'refreshToken': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c',
            }
    
    return {
        'code': error_codes.INVALID_CREDENTIALS,
        'message': 'username of password is invalid'
    }, 400

@account_api.route("logout")
@authorize
def logout():
    return {
        'code': error_codes.SUCCESS,
        'message': 'Logged out successfully'
    }, 200

@account_api.route("<username>", methods=["GET", "PUT", "DELETE"])
@authorize(role = 'self')
def getUserBytUsername(username):
    user = Session.query(User).filter(User.username == username).first()
    if user is None:
        return {
            'code': error_codes.NOT_FOUND,
            'message': 'Unauthorized user access'
        }, 404

    if request.method == "PUT":
        user_alter = UserSerializer().load(request.get_json())
        for key in user_alter.keys():
            user.__setattr__(key, user_alter[key])
    elif request.method == "DELETE":
        Session.delete(user)

    Session.commit()
    return UserSerializer().dump(user)

