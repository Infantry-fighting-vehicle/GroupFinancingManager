from flask import Blueprint, request, Response
from sqlalchemy import create_engine
from api import error_codes
from services.authorization import authorize, generate_token, get_authorized_user

from config.db_connection_info import DB_URL, get_database_session
from models.service import error_codes
from models import *
from bcrypt import checkpw, hashpw, gensalt
from random import randint
from sqlalchemy import or_

Session = get_database_session()
account_api = Blueprint('user_api', __name__)

@account_api.route("", methods=["GET", "POST"])
def accountList():
    # print(request.get_json())
    print(request.method)
    if request.method == "POST":
        request_data = request.get_json()
        user = User(
            username = request_data['username'],
            password = hashpw(bytes(request_data['password'], 'utf-8'), gensalt(14)).decode(),
            first_name = request_data['first_name'],
            last_name = request_data['last_name'],
            card_number = int(f'{randint(1,9)}'+''.join([str(randint(0, 9)) for i in range(16)])),
            phone = '',
            email = request_data['email']
        )

        Session.add(user)
        Session.commit()

        return UserSerializer().dump(user)
    elif request.method == "GET":
        user = get_authorized_user()
        if user is None:
            return {
                'code': error_codes.UNAUTHORIZED,
                'message': 'Unauthorized user access'
            }, 401

        return UserSerializer().dump(user), 200

# takes login and password as args
@account_api.route("login", methods=["POST"])
def login():
    request_data = request.get_json()
    user: User = Session.query(User).filter(or_(User.username == request_data['username'], User.email == request_data['username'])).first()
    if user is not None:
        is_pass_valid = checkpw(bytes(request_data['password'], 'utf-8'), bytes(user.password, 'utf-8'))
        print(request_data['password'], is_pass_valid)
        if 'username' in request_data and 'password' in request_data and is_pass_valid:
            return generate_token(user.id)
    
    return {
        'code': error_codes.INVALID_CREDENTIALS,
        'message': 'username or password is invalid'
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
        user_alter = UserInsensetiveSerializer().load(request.get_json())
        for key in user_alter.keys():
            user.__setattr__(key, user_alter[key])
    elif request.method == "DELETE":
        Session.delete(user)

    Session.commit()
    return UserSerializer().dump(user)

