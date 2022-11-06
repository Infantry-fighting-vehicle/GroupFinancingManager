from unittest import result
from flask import Blueprint, request
from models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.db_connection_info import DB_URL

account_api = Blueprint('user_api', __name__)

engine = create_engine(DB_URL)
SessionFactory = sessionmaker(bind=engine)
Session = SessionFactory()

@account_api.route("", methods=["POST", "GET"])
def accountList():
    print(request.get_json())
    request_data = request.get_json()
    user = User(
        username = request_data['username'],
        password = request_data['password'],
        first_name = request_data['first_name'],
        last_name = request_data['last_name'],
        card_number = request_data['card_number'],
        phone = request_data['phone'],
        email = request_data['email']
    )

    Session.add(user)
    Session.commit()

    return dict(user)

@account_api.route("login")
def login(username, password):
    return "login"