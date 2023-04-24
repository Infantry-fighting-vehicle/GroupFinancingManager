from flask import request
from mysqlx import Session
from config.db_connection_info import get_database_session
from models.service import error_codes
from models.service.Token import Token
from models.user import User, UserSerializer
import jwt
from datetime import datetime, timedelta

# token to test:
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU0NDc4ODc2LCJqdGkiOiJiYmQ0ZGFkNzUxYWU0YWM5OTg4YjUwODMzYTNiODhmNiIsInVzZXJfaWQiOjE2fQ.4cWe2RWrg5A2TC7BSSjGKTxuTGi2bSsxwvbjP-8cRdI

def authorize(role = "anybody"):
    def decoration(func):
        def inner(*args, **kwargs):
            if 'Authorization' in request.headers and request.headers['Authorization'] != '':
                ## add role checking
                return func(*args, **kwargs)
            return {
                'code': error_codes.UNAUTHORIZED,
                'message': 'You are not authorized'
            }
        inner.__name__ = func.__name__
        return inner
    if type(role) != str:
        return decoration(role)
    return decoration

def generate_token(user_id) -> dict:
    return {
        "accessToken": jwt.encode({
            "token_type": "auth",
            "user_id": user_id,
            "exp": datetime.now() + timedelta(7),
            "jti": "test"
        }, 'your-256-bit-secret', algorithm='HS256'),
        "refreshToken": jwt.encode({
            "token_type": "refresh",
            "user_id": user_id,
            "exp": datetime.now() + timedelta(14),
            "jti": "test2"
        }, 'your-256-bit-secret', algorithm='HS256'),
    }

def get_authorized_user() -> User:
    Session = get_database_session()
    try:
        token_data = Token().load(jwt.decode(request.headers['Authorization'].split(' ')[-1], 'your-256-bit-secret', algorithms=['HS256']))
    except KeyError:
        return None

    return Session.query(User).filter(User.id == token_data['user_id']).first()
