from flask import request
from mysqlx import Session
from config.db_connection_info import get_database_session
from models.service import error_codes
from models.service.Token import Token
from models.user import User, UserSerializer
import jwt

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

def get_authorized_user() -> User:
    Session = get_database_session()
    token_data = Token().load(jwt.decode(request.headers['Authorization'], 'your-256-bit-secret', algorithms=['HS256']))
    return Session.query(User).filter(User.id == token_data['user_id']).first()