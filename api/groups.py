
from flask import jsonify, Blueprint, request, Response
from mysqlx import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.service import error_codes
from services.authorization import *

from config.db_connection_info import DB_URL, get_database_session
# from api.error_codes import error_codes
from models import *

from services.generate_passcode import generate_passcode

group_api = Blueprint('groups_api', __name__)
Session = get_database_session()

@group_api.route('', methods=['POST'])
@http_auth.login_required
def create_group_function():
    Session = get_database_session()
    group = GroupBasicSerializer().load(request.get_json())

    new_group = Group(
        name = group['name'],
        owner_id = get_current_user().id,
        secret_key = generate_passcode()
    )

    Session.add(new_group)
    Session.commit()
    Session.refresh(new_group)

    user_membership = Membership(
            user_id = get_current_user().id,
            group_id = new_group.id,
            status = "ACCEPTED"
        )
    Session.add(user_membership)
    Session.commit()

    return 'created successfully', 200

@group_api.route('/list', methods=['GET'])
@http_auth.login_required
def list_avaliable_groups():
    return GroupInsensitiveSerializer().dump(Session.query(Group).filter(Group.owner_id == get_current_user().id).all(), many=True), 200


@group_api.route('/<group_id>', methods=['GET', 'PUT', 'DELETE'])
@http_auth.login_required
def group_management(group_id):
    Session = get_database_session()
    group = Session.query(Group).filter(Group.id == group_id).first()

    if group is None or group.owner_id != get_current_user().id:
        return {
                'code': error_codes.UNAUTHORIZED,
                'message': 'username of password is invalid'
            }, 401

    if request.method == "PUT":
        updated_group = GroupBasicSerializer().load(request.json)
        Session.query(Group).filter(Group.id == group_id).update(updated_group)
        Session.commit()
        return UserInsensetiveSerializer().dump(Session.query(Group).filter(Group.id == group_id).first())
    elif request.method == "DELETE":
        Session.delete(group)
    Session.commit()

    return GroupSerializer().dump(group)

@group_api.route('/<group_id>/send_invitation', methods=['POST'])
@http_auth.login_required
def sent_user_invitation(group_id):
    Session = get_database_session()
    group = Session.query(Group).filter(Group.id == group_id).first()
    if group is None:
        return {
            'code': error_codes.NOT_FOUND,
            'message': 'Group not found' 
        }, 404
    elif get_current_user().id != group.owner_id:
        return {
            'code': error_codes.UNAUTHORIZED,
            'message': 'Not enough priviliges'
        }, 401

    
    user_membership = Membership(
        user_id = request.args['user_id'],
        group_id = group_id,
        status = UserStatus.UNACCEPTED
    )
    Session.add(user_membership)
    Session.commit()

    return 'sent successfully'

@group_api.route('/<group_id>/join', methods=['POST'])
@http_auth.login_required
def join_group(group_id):
    Session = get_database_session()
    group = Session.query(Group).filter(Group.id == group_id).first()

    if group is None:
        return {
            'code': error_codes.NOT_FOUND,
            'message': 'Group not found' 
        }, 404

    user_membership = Membership(
        group_id = group_id,
        user_id = get_current_user().id,
        status = "ACCEPTED"
    )
    Session.add(user_membership)
    Session.commit()

    return group.name


@group_api.route('/<group_id>/kick', methods=['DELETE'])
@http_auth.login_required
def kick_users(group_id):
    Session = get_database_session()
    group = Session.query(Group).filter(Group.id == group_id).first()

    if group is None:
        return {
            'code': error_codes.NOT_FOUND,
            'message': 'Group not found' 
        }, 404
    elif get_current_user().id != group.owner_id:
        return {
            'code': error_codes.UNAUTHORIZED,
            'message': 'Not enough priviliges'
        }, 401

    Session.query(Membership).filter(Membership.user_id == request.args['user_id']).delete()
    Session.commit()

    return 'deleted successfully', 200

@group_api.route('/<group_id>/purchase', methods=['POST'])
@http_auth.login_required
def purchase_create(group_id):
    Session = get_database_session()
    print(get_current_user().id, group_id, Session.query(Membership).filter(Membership.user_id==get_current_user().id and Membership.group_id==group_id).first())
    if not (Session.query(Membership).filter(Membership.user_id==get_current_user().id and Membership.group_id==group_id).first()):
        return {
            'code': error_codes.UNAUTHORIZED,
            'message': 'Not enough priviliges'
        }, 401

    new_purchase = Purchase(
        group_id = group_id,
        owner_id = get_current_user().id,
        name = request.args['name'],
        cost = request.args['cost']
    )
    Session.add(new_purchase)
    Session.commit()

    return 'added successfully', 200

@group_api.route('/purchase/<purchase_id>', methods=['DELETE'])
@http_auth.login_required
def purchase_delete(purchase_id):
    Session = get_database_session()

    if get_current_user().id != Session.query(Purchase).filter(Purchase.id==purchase_id).first().owner_id:
        return {
            'code': error_codes.UNAUTHORIZED,
            'message': 'Not enough priviliges'
        }, 401

    Session.query(Purchase).filter(Purchase.id==purchase_id).delete()
    Session.commit()

    return {'Message': 'Success', 'Code': 200}

@group_api.route('/purchase/<purchase_id>', methods=['PUT'])
@http_auth.login_required
def purchase_update(purchase_id):
    Session = get_database_session()
    purchase = Session.query(Purchase).filter(Purchase.id==purchase_id).first()

    if not purchase:
        return {
            'code': error_codes.NOT_FOUND,
            'message': 'Purchase not found'
        }, 404
        
    if get_current_user().id != purchase.owner_id:
        return {
            'code': error_codes.UNAUTHORIZED,
            'message': 'Not enough priviliges'
        }, 401
    updated_purchase = PurchaseCreateSerializer().load(request.json)
    Session.query(Purchase).filter(Purchase.id==purchase_id).update(updated_purchase)
    Session.commit()
    
    return 'successfully updated', 200


@group_api.route('/purchase/<purchase_id>', methods=['GET'])
@http_auth.login_required
def purchase_members(purchase_id):
    Session = get_database_session()
    purchase = Session.query(Purchase).filter(Purchase.id==purchase_id).first()
    
    if not purchase:
        return {
            'code': error_codes.NOT_FOUND,
            'message': 'Purchase not found'
        }, 404
    # print(Session.query(Membership).filter(Membership.user_id==get_current_user().id and Membership.group_id==purchase['group_id']), get_current_user().id, purchase['group_id'])
    if not Session.query(Membership).filter(Membership.user_id==get_current_user().id and Membership.group_id==purchase['group_id']).first():
        return {
            'code': error_codes.UNAUTHORIZED,
            'message': 'Not enough priviliges'
        }, 401

    return 'successfully got the purchase', 200


    