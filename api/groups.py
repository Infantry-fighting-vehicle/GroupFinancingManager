
from flask import jsonify, Blueprint, request, Response
from mysqlx import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.service import error_codes
from services.authorization import authorize, get_authorized_user

from config.db_connection_info import DB_URL, get_database_session
# from api.error_codes import error_codes
from models import *
from bcrypt import checkpw, hashpw, gensalt
from sqlalchemy import and_

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
        secret_key = passcode
    )

    Session.add(new_group)
    Session.commit()

    new_membership = Membership(
        group_id = new_group.id,
        user_id = owner.id,
        status = UserStatus.OWNER,
    )

    Session.add(new_membership)
    Session.commit()

    return GroupSensitiveSerialzier().dump(new_group)

@group_api.route('/list', methods=['GET'])
@authorize
def list_avaliable_groups():
    Session = get_database_session()
    user = get_authorized_user()
    groups = Session.query(Group).join(
        Membership, Group.id == Membership.group_id
    ).filter(Membership.user_id == user.id).all()
    return GroupInsensitiveSerializer().dump(groups, many=True)


@group_api.route('/<group_id>', methods=['GET', 'PUT', 'DELETE'])
@authorize
def group_management(group_id):
    Session = get_database_session()
    user = get_authorized_user()
    group: Group = Session.query(Group).outerjoin(
        Membership, Group.id == Membership.group_id
    ).filter(and_(Group.id == group_id, Membership.user_id == user.id)).first()

    if group is None or (request.method != 'GET' and not len([1 for member in group.members if member.user_id == user.id and member.status == UserStatus.OWNER])):
        return { 'code': error_codes.UNAUTHORIZED, 'message': 'unauthorized access' }, 401

    # if request.method == "GET":
        
    if request.method == "PUT":
        group_alter = GroupBasicSerializer().load(request.get_json())
        for key in group_alter.keys():
            group.__setattr__(key, group_alter[key])
    elif request.method == "DELETE":
        for x in group.members:
            Session.delete(x)
        Session.commit()
        Session.delete(group)
    Session.commit()

    group_data = FullGroupSerializer().dump(group)
    members_data = [
        MembershipSerializer().dump(membership)['user']
        for membership in group.members
    ]
    group_data['members'] = members_data


    group_data['purchases'] = [
        PurchaseInfoSerializer().dump(purchase)
        for purchase in group.purchases
    ]
    
    if user.id in [member.user_id for member in group.members if member.status == UserStatus.OWNER]:
        group_data['secret_code'] = group.secret_key
    
    print(list([member.status for member in group.members if member.user_id == user.id]))
    group_data['is_owner'] = any([member.status == UserStatus.OWNER for member in group.members if member.user_id == user.id])

    return group_data

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

# @group_api.route('/join', methods=['POST'])
@authorize
def join_group():
    Session = get_database_session()
    user = get_authorized_user()
    secret_key = request.json.get('secret_key')
    if not secret_key:
        return {
            'code': error_codes.BAD_REQUEST,
            'message': 'Secret not provided' 
        }, 400
    
    group: Group = Session.query(Group).filter(Group.secret_key == secret_key).first()

    if group is None:
        return {
            'code': error_codes.NOT_FOUND,
            'message': 'Group not found' 
        }, 404

    user_membership: Membership = Session.query(Membership).filter(and_(Membership.user_id == user.id, Membership.group_id == group.id)).first()

    if user_membership is None:
        user_membership = Membership(
            group_id = group.id,
            user_id = user.id,
            status = UserStatus.ACCEPTED
        )
        Session.add(user_membership)
    else:
        user_membership.status = UserStatus.ACCEPTED
    
    Session.commit()

    return str(group.id)


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
    elif len([member for member in group.members if member.status == UserStatus.OWNER and member.user_id == user.id]) == 0:
        return {
            'code': error_codes.UNAUTHORIZED,
            'message': 'Not enough priviliges'
        }, 403

    invitations = []
    users_to_kick = request.args.get('users[]')
    for user_id in users_to_kick:
        user_membership = Session.query(Membership).filter(Membership.user_id == user_id).first()
        if user_membership is None:
            continue
        Session.delete(user_membership)
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
def purchase_delete(group_id, purchase_id):
    Session = get_database_session()
    user = get_authorized_user()

    purchase = Session.query(Purchase) \
        .join(Group, Group.id == Purchase.group_id) \
        .join(Membership, Membership.group_id == Purchase.group_id) \
        .filter(and_(Purchase.id==purchase_id, Purchase.group_id == group_id, Membership.user_id == user.id)) \
        .first()

    if not purchase:
        return {'Error': 'Not found', 'Code': 404}
    
    Session.delete(purchase)
    Session.commit()

    return {'Message': 'Success', 'Code': 200}

def get_purchase(group_id, purchase_id):
    Session = get_database_session()
    user = get_authorized_user()

    purchase = Session.query(Purchase).filter(and_(Purchase.id==purchase_id, Purchase.group_id == group_id)).first()
    if not purchase:
        return {'Error': 'Not found', 'Code': 404}
    purchase_schema = PurchaseInfoSerializer().dump(purchase)
    purchase_schema['balance'] = 0

    return purchase_schema

@group_api.route('/<group_id>/purchase/<purchase_id>', methods=['PUT'])
@authorize
def purchase_update(group_id, purchase_id):
    Session = get_database_session()
    user = get_authorized_user()

    updated_info = request.json

    purchase = Session.query(Purchase).filter(Purchase.id==purchase_id).first()
    if not purchase:
        return {'Error': 'Not found', 'Code': 404}
    purchase.name = updated_info['name']
    purchase.cost = updated_info['prica']
    Session.add(purchase)
    Session.commit()

    purchase_schema = PurchaseInfoSerializer().dump(purchase)
    purchase_schema['balance'] = 0
    transfers = Session.query(Transfer).filter(Transfer.purchase_id==purchase_id).all()
    for transfer in transfers:
        purchase_schema['balance'] += transfer.amount
    
    return purchase_schema


@group_api.route('/<group_id>/purchases/<purchase_id>/members', methods=['GET'])
@authorize
def purchase_members(group_id, purchase_id):
    Session = get_database_session()
    user = get_authorized_user()

    purchase = Session.query(Purchase).filter(Purchase.id==purchase_id).first()
    if not purchase:
        return {'Error': 'Not found', 'Code': 404}
    transfers = Session.query(Transfer).filter(Transfer.purchase_id==purchase_id).all()
    users = set()
    for transfer in transfers:
        users.add(transfer.user_id)

    purchase_member_schemas = []
    for user_id in users:
        purchase_member_schemas.append(PurchaseMemberInfo().dump(
            Session.query(User).filter(User.id==user_id).first()
        ))
        purchase_member_schemas[-1]['amount'] = 0
        user_purchase_transfers = Session.query(Transfer).filter(Transfer.purchase_id==purchase_id and Transfer.user_id==user_id).all()
        for user_purchase_transfer in user_purchase_transfers:
            purchase_member_schemas[-1]['amount'] += user_purchase_transfer.amount
        
    return purchase_member_schemas

    

# make endpoint to create transfer
@group_api.route('/<group_id>/purchase/<purchase_id>/transfer', methods=['POST'])
def create_transfer(group_id, purchase_id):
    Session = get_database_session()
    user = get_authorized_user()

    transfer = CreateTransferSerializer().load(request.get_json())
    new_transfer = Transfer(
        user_id = user.id,
        purchase_id = purchase_id,
        amount = transfer['amount']
    )
    Session.add(new_transfer)
    Session.commit()

    return {'Message': 'Success', 'Code': 200}