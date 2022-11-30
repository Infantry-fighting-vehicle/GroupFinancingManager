import unittest
from main import app
from models import *
from config.db_connection_info import get_database_session
from services.generate_passcode import generate_passcode

db = get_database_session()

app.testing = True
client = app.test_client()

from base64 import b64encode

def authentication_headers(username, password):
    return {'headers': {
            'Authorization': f'''Basic {b64encode(f"{username}:{password}".encode('UTF-8')).decode('UTF-8')}'''
        }
    }

def get_valid_user(user):
    valid_user = User(
        username = user['username'],
        password = user['password'],
        first_name = user['first_name'],
        last_name = user['last_name'],
        card_number = user['card_number'],
        phone = user['phone'],
        email = user['email']
    )
    return valid_user

def get_valid_user_id(user):
    valid_user = User(
        username = user['username'],
        password = user['password'],
        first_name = user['first_name'],
        last_name = user['last_name'],
        card_number = user['card_number'],
        phone = user['phone'],
        email = user['email']
    )
    db.add(valid_user)
    db.commit()
    get_user = UserSerializer().dump(db.query(User).filter(User.username == user['username']).first())
    valid_user_res = User(
        id = get_user['id'],
        username = get_user['username'],
        password = get_user['password'],
        first_name = get_user['first_name'],
        last_name = get_user['last_name'],
        card_number = get_user['card_number'],
        phone = get_user['phone'],
        email = get_user['email']
    )
    return valid_user_res

valid_user_schema = {
    "username": "username",
    "password": "password",
    "first_name": "first_name",
    "last_name": "last_name",
    "card_number": "card_number",
    "phone": "phone",
    "email": "email"
}

valid_user_schema1 = {
    "username": "username1",
    "password": "password1",
    "first_name": "first_name1",
    "last_name": "last_name1",
    "card_number": "card_number1",
    "phone": "phone1",
    "email": "email1"
}
valid_user_schema2 = {
    "username": "username2",
    "password": "password2",
    "first_name": "first_name2",
    "last_name": "last_name2",
    "card_number": "card_number2",
    "phone": "phone2",
    "email": "email2"
}
valid_user_schema3 = {
    "username": "username3",
    "password": "password3",
    "first_name": "first_name3",
    "last_name": "last_name3",
    "card_number": "card_number3",
    "phone": "phone3",
    "email": "email3"
}
invalid_user_schema1 = {
    "username": "invalid_username1",
    "password": "invalid_password1",
    "first_name": "invalid_first_name1",
    "last_name": "invalid_last_name1",
    "card_number": "invalid_card_number1",
    "phone": "invalid_phone1",
    "email": "invalid_email1"
}
login_user_schema1 = {
    "username": "username1",
    "password": "password1"
}
login_user_schema2 = {
    "username": "username2",
    "password": "password2"
}
login_user_schema3 = {
    "username": "username3",
    "password": "password3"
}
invalid_login_user_schema1 = {
    "username": "invalid_username1",
    "password": "invalid_password1"
}
invalid_login_without_password_user_schema1 = {
    "username": "invalid_username1"
}
valid_put_user_schema1 = {
    "first_name": "put_first_name1",
    "last_name": "put_last_name1",
    "phone": "put_phone1"
}

class TestUser(unittest.TestCase):
    URL = 'http://localhost:8000/user'

    def setUp(self):
        self.db = db
        valid_user1 = get_valid_user(valid_user_schema1)
        valid_user2 = get_valid_user(valid_user_schema2)
        valid_user3 = get_valid_user(valid_user_schema3)
        self.db.add_all([valid_user1, valid_user2, valid_user3])
        self.db.commit()

    def test_create_user(self):
        response = client.post(self.URL, json=valid_user_schema)
        self.assertEqual(response.status_code, 200)
        response2 = client.post(self.URL, json=valid_user_schema)
        self.assertEqual(response2.status_code, 400)

    def test_login_user(self):
        response = client.get(self.URL + '/login', query_string=login_user_schema1)
        self.assertEqual(response.status_code, 200)
        response2 = client.get(self.URL + '/login', query_string=invalid_login_without_password_user_schema1)
        self.assertEqual(response2.status_code, 400)
        response3 = client.get(self.URL + '/login', query_string=invalid_login_user_schema1)
        self.assertEqual(response3.status_code, 400)
        
    def test_logout_user(self):
        response = client.get(self.URL + '/logout', **authentication_headers(login_user_schema1['username'], login_user_schema1['password']))
        self.assertEqual(response.status_code, 200)
        response2 = client.get(self.URL + '/logout', **authentication_headers(invalid_login_user_schema1['username'], invalid_login_user_schema1['password']))
        self.assertEqual(response2.status_code, 401)

    def test_get_user_by_username(self):
        response = client.get(self.URL + '/' + valid_user_schema1['username'], **authentication_headers(login_user_schema1['username'], login_user_schema1['password']))
        self.assertEqual(response.status_code, 200)
        response2 = client.get(self.URL + '/' + invalid_user_schema1['username'] + 'invalid', **authentication_headers(login_user_schema1['username'], login_user_schema1['password']))
        self.assertEqual(response2.status_code, 404)

    def test_put_user_by_username(self):
        response = client.put(self.URL + '/' + valid_user_schema1['username'], json=valid_put_user_schema1, **authentication_headers(login_user_schema1['username'], login_user_schema1['password']))
        self.assertEqual(response.status_code, 200)
        response2 = client.put(self.URL + '/' + valid_user_schema2['username'], json=valid_put_user_schema1, **authentication_headers(login_user_schema1['username'], login_user_schema1['password']))
        self.assertEqual(response2.status_code, 401)

    def test_delete_user_by_username(self):
        response2 = client.delete(self.URL + '/' + valid_user_schema3['username'], **authentication_headers(login_user_schema3['username'], login_user_schema3['password']))
        self.assertEqual(response2.status_code, 200)
        response = client.delete(self.URL + '/' + valid_user_schema1['username'], **authentication_headers(login_user_schema2['username'], login_user_schema2['password']))
        self.assertEqual(response.status_code, 401)

    def tearDown(self):
        self.db.query(User).delete()
        self.db.commit()

valid_group_schema1 = {
    "name":"group1"
}
valid_group_schema2 = {
    "name":"group2"
}
valid_group_schema3 = {
    "name":"group3"
}
valid_put_group_schema2 = {
    "name":"put_group3"
}
sent_invitation_schema = {
    "user_id":"100"
}
kick_user_from_group_schema1 = {
    "user_id":"100"
}
purchase_group_schema = {
    "name":"tea",
    "cost":"1000"
}
def get_valid_group(group, user):
    valid_group = Group(
        name = group['name'],
        owner_id = user.id,
        secret_key = generate_passcode()
    )
    db.add(valid_group)
    db.commit()
    get_group = GroupSerializer().dump(db.query(Group).filter(Group.name == group['name']).first())
    valid_group_res = Group(
        id = get_group['id'],
        name = get_group['name'],
        owner_id = get_group['owner_id'],
        secret_key = get_group['secret_key']
    )
    return valid_group_res

class TestGroup(unittest.TestCase):
    URL = 'http://localhost:8000/group'

    def setUp(self):
        self.db = db
        self.valid_user1 = get_valid_user_id(valid_user_schema1)
        self.valid_user2 = get_valid_user_id(valid_user_schema2)
        self.valid_user3 = get_valid_user_id(valid_user_schema3)
        self.valid_group2 = get_valid_group(valid_group_schema2, self.valid_user2)

    def test_create_group(self):
        response = client.post(self.URL, json=valid_group_schema1, **authentication_headers(valid_user_schema1["username"],valid_user_schema1["password"]))
        self.assertEqual(response.status_code, 200)

    def test_get_group_list(self):
        response = client.get(self.URL + '/list', **authentication_headers(valid_user_schema1["username"],valid_user_schema1["password"]))
        self.assertEqual(response.status_code, 200)

    def test_get_group_by_id(self):
        response = client.get(self.URL + '/' + str(int(self.valid_group2.id)), **authentication_headers(valid_user_schema1["username"],valid_user_schema1["password"]))
        self.assertEqual(response.status_code, 401)

    def test_put_group_by_id(self):
        # raise Exception(int(self.valid_group2.id))
        response = client.put(self.URL + '/' + str(int(self.valid_group2.id)), json=valid_put_group_schema2, **authentication_headers(valid_user_schema2["username"],valid_user_schema2["password"]))
        self.assertEqual(response.status_code, 200)
        response2 = client.put(self.URL + '/' + str(int(self.valid_group2.id)), **authentication_headers(invalid_user_schema1["username"],invalid_user_schema1["password"]))
        self.assertEqual(response2.status_code, 401)
        
    def test_delete_group_by_id(self):
        response = client.delete(self.URL + '/' + str(int(self.valid_group2.id)), **authentication_headers(valid_user_schema2["username"],valid_user_schema2["password"]))
        self.assertEqual(response.status_code, 200)
        
    def test_send_invitation_group_by_id(self):
        response = client.post(self.URL + '/' + str(1) + '/send_invitation', **authentication_headers(valid_user_schema1["username"],valid_user_schema1["password"]))
        self.assertEqual(response.status_code, 404)
        response2 = client.post(self.URL + '/' + str(int(self.valid_group2.id)) + '/send_invitation', **authentication_headers(valid_user_schema1["username"],valid_user_schema1["password"]))
        self.assertEqual(response2.status_code, 401)
        # response3 = client.post(self.URL + '/' + str(int(self.valid_group2.id)) + '/send_invitation', query_string=sent_invitation_schema, **authentication_headers(valid_user_schema2["username"],valid_user_schema2["password"]))
        # self.assertEqual(response3.status_code, 200)

    def test_join_group_by_id(self):
        response = client.post(self.URL + '/' + str(1) + '/join', **authentication_headers(valid_user_schema1["username"],valid_user_schema1["password"]))
        self.assertEqual(response.status_code, 404)
        response2 = client.post(self.URL + '/' + str(int(self.valid_group2.id)) + '/join', **authentication_headers(valid_user_schema1["username"],valid_user_schema1["password"]))
        self.assertEqual(response2.status_code, 200)

    def tearDown(self):
        self.db.query(Membership).delete()
        self.db.query(Group).delete()
        self.db.query(User).delete()
        self.db.commit()

def valid_delete_user_id(valid_id):
    id = str(int(valid_id))
    return {"user_id" : id}

def get_valid_purchase_id(group_id, owner_id, purchase):
    valid_purchase = Purchase(
        group_id=group_id,
        owner_id=owner_id, 
        name=purchase['name'], 
        cost=purchase['cost']
    )
    db.add(valid_purchase)
    db.commit()
    get_purchase = PurchaseInfoSerializer().dump(db.query(Purchase).filter(Purchase.group_id == group_id and Purchase.owner_id == owner_id).first())
    valid_purchase_res = Purchase(
        id = get_purchase['id'],
        group_id = group_id,
        owner_id = owner_id,
        name = get_purchase['name'],
        cost=get_purchase['cost']
    )
    return valid_purchase_res

valid_purchase_schema1 = {
    "name":"hello",
    "cost":"1000"
}
updated_valid_purchase_schema1 = {
    "name":"hello1",
    "cost":"10001"
}
class TestGroup2(unittest.TestCase):
    URL = 'http://localhost:8000/group'

    def setUp(self):
        self.db = db
        self.valid_user1 = get_valid_user_id(valid_user_schema1)
        self.valid_user2 = get_valid_user_id(valid_user_schema2)
        self.valid_user3 = get_valid_user_id(valid_user_schema3)
        self.valid_group2 = get_valid_group(valid_group_schema2, self.valid_user2)
        self.membership2 = Membership(user_id=self.valid_user2.id, group_id=self.valid_group2.id, status=UserStatus.UNACCEPTED)
        self.purchase1 = get_valid_purchase_id(self.valid_group2.id, self.valid_user2.id, valid_purchase_schema1)
        self.db.add(self.membership2)
        self.db.commit()

    def test_kick_from_group_by_id(self):
        response = client.delete(self.URL + '/' + str(1) + '/kick', query_string=kick_user_from_group_schema1, **authentication_headers(valid_user_schema1["username"],valid_user_schema1["password"]))
        self.assertEqual(response.status_code, 404)
        response2 = client.delete(self.URL + '/' + str(int(self.valid_group2.id)) + '/kick', query_string=kick_user_from_group_schema1, **authentication_headers(valid_user_schema3["username"],valid_user_schema3["password"]))
        self.assertEqual(response2.status_code, 401)
        response3 = client.delete(self.URL + '/' + str(int(self.valid_group2.id)) + '/kick', query_string=valid_delete_user_id(self.valid_user2.id), **authentication_headers(valid_user_schema2["username"],valid_user_schema2["password"]))
        self.assertEqual(response3.status_code, 200)

    def test_post_purchase_group_by_id(self):
        response = client.post(self.URL + '/' + str(int(self.valid_group2.id)) + '/purchase', query_string=purchase_group_schema, **authentication_headers(valid_user_schema1["username"],valid_user_schema1["password"]))
        self.assertEqual(response.status_code, 401)
        response2 = client.post(self.URL + '/' + str(int(self.valid_group2.id)) + '/purchase', query_string=purchase_group_schema, **authentication_headers(valid_user_schema2["username"],valid_user_schema2["password"]))
        self.assertEqual(response2.status_code, 200)

    def test_delete_purchase_group_by_id(self):
        response = client.delete(self.URL + '/purchase/' + str(int(self.purchase1.id)), **authentication_headers(valid_user_schema1["username"],valid_user_schema1["password"]))
        self.assertEqual(response.status_code, 401)
        response2 = client.delete(self.URL + '/purchase/' + str(int(self.purchase1.id)), **authentication_headers(valid_user_schema2["username"],valid_user_schema2["password"]))
        self.assertEqual(response2.status_code, 200)

    def test_update_purchase_group_by_id(self):
        response = client.put(self.URL + '/purchase/' + str(1), json=updated_valid_purchase_schema1, **authentication_headers(valid_user_schema2["username"],valid_user_schema2["password"]))
        self.assertEqual(response.status_code, 404)
        response2 = client.put(self.URL + '/purchase/' + str(int(self.purchase1.id)), json=updated_valid_purchase_schema1, **authentication_headers(valid_user_schema1["username"],valid_user_schema1["password"]))
        self.assertEqual(response2.status_code, 401)
        response3 = client.put(self.URL + '/purchase/' + str(int(self.purchase1.id)), json=updated_valid_purchase_schema1, **authentication_headers(valid_user_schema2["username"],valid_user_schema2["password"]))
        self.assertEqual(response3.status_code, 200)

    def test_get_purchase_group_by_id(self):
        response = client.get(self.URL + '/purchase/' + str(1), **authentication_headers(valid_user_schema2["username"],valid_user_schema2["password"]))
        self.assertEqual(response.status_code, 404)
        response2 = client.get(self.URL + '/purchase/' + str(int(self.purchase1.id)), **authentication_headers(valid_user_schema1["username"],valid_user_schema1["password"]))
        self.assertEqual(response2.status_code, 401)
        response3 = client.get(self.URL + '/purchase/' + str(int(self.purchase1.id)), **authentication_headers(valid_user_schema2["username"],valid_user_schema2["password"]))
        self.assertEqual(response3.status_code, 200)

    def tearDown(self):
        self.db.query(Purchase).delete()
        self.db.query(Membership).delete()
        self.db.query(Group).delete()
        self.db.query(User).delete()
        self.db.commit()
