from flask import Blueprint, request, Response, redirect, url_for
from sqlalchemy import create_engine

from services.authorization import *

from config.db_connection_info import DB_URL, get_database_session
from models.service import error_codes
from models import *
# from bcrypt import checkpw, hashpw, gensalt

# Session = get_database_session()
account_api = Blueprint('user_api', __name__)
Session = get_database_session()

@account_api.route("", methods=["POST"])
def accountList():
    if request.method == 'POST':
        print(request.get_json())
        request_data = request.get_json()
        if Session.query(User).filter(User.email == request_data['email']).first() or Session.query(User).filter(User.username == request_data['username']).first():
            return {
                        'code': "user",
                        'message': 'user with such email/username already exists'
                    }, 400
        user = User(
            username = request_data['username'],
            # password = hashpw(bytes(request_data['password'], 'utf-8'), gensalt(14)).decode(),
            password = request_data['password'],
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
    if user is not None and request.args['password'] == user.password:
            return UserSerializer().dump(user)
    
    return {
        'code': error_codes.INVALID_CREDENTIALS,
        'message': 'username of password is invalid'
    }, 400

@account_api.route("logout")
@http_auth.login_required
def logout():
    return "Successfully logout"

@account_api.route("<username>", methods=["GET", "PUT", "DELETE"])
@http_auth.login_required
def getUserBytUsername(username):
    user = Session.query(User).filter(User.username == username).first()
    if user is None:
        return {
            'code': error_codes.NOT_FOUND,
            'message': 'Unauthorized user access'
        }, 404
    if get_current_user().username != user.username:
        return {
            'code': error_codes.UNAUTHORIZED,
            'message': 'Unauthorized user access'
        }, 401

    if request.method == "PUT":
        # user_alter = UserInsensetiveSerializer().load(request.get_json())
        # for key in user_alter.keys():
        #     user.__setattr__(key, user_alter[key])
        # Session.query(User).filter(User.username == username).update(user)
        # Session.commit()
        updated_user = UserInsensetiveSerializer().load(request.json)
        Session.query(User).filter(User.username == username).update(updated_user)
        Session.commit()
        return UserInsensetiveSerializer().dump(Session.query(User).filter(User.username == username).first())
    elif request.method == "GET":
        return UserSerializer().dump(user)
    elif request.method == "DELETE":
        Session.query(User).filter(User.username == username).delete()
        Session.commit()

    return UserSerializer().dump(user)
