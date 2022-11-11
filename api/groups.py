import code
from crypt import methods
from distutils.log import error
from tokenize import group
from unicodedata import name
from webbrowser import get
from flask import Blueprint, request, Response
from mysqlx import Session
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

@group_api.route('/<group_id>/send_invitation', methods=['POST'])
@authorize
def sent_user_invitation(group_id):
    Session = get_database_session()
    user = get_authorized_user()
    group = Session.query(Group).filter(Group.id == group_id).first()
    if group is None:
        return {
            'code': error_codes.NOT_FOUND,
            'message': 'Group not found' 
        }, 404
    elif user.id != group.owner_id:
        return {
            'code': error_codes.UNAUTHORIZED,
            'message': 'Not enough priviliges'
        }, 403

    invitations = []
    for user_id in request.get_json():
        user_membership = Membership(
            user_id = user_id,
            group_id = group_id,
            status = UserStatus.UNACCEPTED._value_
        )
        invitations.append(UserStatus.UNACCEPTED.name)
        Session.add(user_membership)
    Session.commit()

    return invitations

@group_api.route('/<group_id>/join', methods=['POST'])
@authorize
def join_group(group_id):
    Session = get_database_session()
    user = get_authorized_user()
    secret_key = request.args.get('secret_key')
    group = Session.query(Group).filter(Group.id == group_id).first()

    if group is None:
        return {
            'code': error_codes.NOT_FOUND,
            'message': 'Group not found' 
        }, 404

    user_membership = Session.query(Membership).filter(Membership.user_id == user.id).first()
    if user_membership is None:
        user_membership = Membership(
            group_id = group_id,
            user_id = user.id,
            status = UserStatus.ACCEPTED._value_
        )
        Session.add(user_membership)
    else:
        user_membership.status = UserStatus.ACCEPTED._value_
    
    Session.commit()

    return group.name


@group_api.route('/<group_id>/kick', methods=['DELETE'])
@authorize
def kick_users(group_id):
    Session = get_database_session()
    user = get_authorized_user()
    group = Session.query(Group).filter(Group.id == group_id).first()
    if group is None:
        return {
            'code': error_codes.NOT_FOUND,
            'message': 'Group not found' 
        }, 404
    elif user.id != group.owner_id:
        return {
            'code': error_codes.UNAUTHORIZED,
            'message': 'Not enough priviliges'
        }, 403

    invitations = []
    for user_id in request.get_json():
        user_membership = Session.query(Membership).filter(Membership.user_id == user_id)
        Session.remove(user_membership)
    Session.commit()

    return {
        'code': error_codes.SUCCESS,
        'message': 'Successfully deleted'
    }

@group_api.route('/<group_id>/purchase', methods=['POST'])
@authorize
def purchase_create(group_id):
    Session = get_database_session()
    user = get_authorized_user()

    purchase = PurchaseCreateSerializer().load(request.get_json())

    new_purchase = Purchase(
        group_id = group_id,
        owner_id = user.id,
        name = purchase['name'],
        cost = purchase['cost']
    )
    Session.add(new_purchase)
    Session.commit()

    return purchase


@group_api.route('/<group_id>/purchase', methods=['DELETE'])
@authorize
def purchase_create(group_id):
    Session = get_database_session()
    user = get_authorized_user()

    purchase = PurchaseCreateSerializer().load(request.get_json())

    new_purchase = Purchase(
        group_id = group_id,
        owner_id = user.id,
        name = purchase['name'],
        cost = purchase['cost']
    )
    Session.add(new_purchase)
    Session.commit()

    return purchase
