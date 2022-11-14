
from config.db_connection_info import get_database_session
from models.user import User

from models import *
from flask_httpauth import HTTPBasicAuth
from bcrypt import checkpw
http_auth = HTTPBasicAuth()

@http_auth.verify_password
def verify_password(username, password):
    Session = get_database_session()
    user = Session.query(User).filter(User.username==username).first()
    return user and checkpw(bytes(password, 'utf-8'), bytes(user.password, 'utf-8'))

def get_current_user() -> User:
    Session = get_database_session()
    username = http_auth.current_user()
    return Session.query(User).filter(User.username==username).first()
