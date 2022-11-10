from crypt import methods
from unicodedata import name
from flask import Blueprint, request, Response
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.service import error_codes
from services.authorization import authorize, get_authorized_user

from config.db_connection_info import DB_URL, get_database_session
# from api.error_codes import error_codes
from models import *
from bcrypt import checkpw, hashpw, gensalt

from services.generate_passcode import generate_passcode

group_api = Blueprint('groups_api', __name__)

@group_api.route('', methods=['POST'])
@authorize
def create_function():
    Session = get_database_session()
    group = GroupBasicSerializer().load(request.get_json())
    owner = get_authorized_user()
    passcode = generate_passcode()

    new_group = Group(
        name = group['name'],
        owner_id = owner.id,
        secret_key = passcode
    )

    Session.add(new_group)
    Session.commit()

    return GroupSerializer().dump(new_group)

@group_api.route('/list', methods=['GET'])
@authorize
def list_avaliable_groups():
    Session = get_database_session()
    user = get_authorized_user()
    groups = Session.query(Group).filter(Group.owner_id == user.id).all()
    return GroupInsensitiveSerializer().dump(groups, many=True)


@group_api.route('/<group_id>', methods=['GET', 'PUT', 'DELETE'])
@authorize
def group_management(group_id):
    Session = get_database_session()
    group = Session.query(Group).filter(Group.id == group_id).first()
    user = get_authorized_user()

    if group is None or (request.method != 'GET' and group.owner_id != user.id):
        return { 'code': error_codes.UNAUTHORIZED, 'message': 'unauthorized access' }

    if request.method == "PUT":
        group_alter = GroupBasicSerializer().load(request.get_json())
        for key in group_alter.keys():
            group.__setattr__(key, group_alter[key])
    elif request.method == "DELETE":
        Session.delete(group)
    Session.commit()

    return GroupSerializer().dump(group)