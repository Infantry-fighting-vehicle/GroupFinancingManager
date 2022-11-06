from typing import Type
from models import *

person1 = User(username='Daminik', password='17102022', first_name='Dmytro', last_name='Pavliv', card_number='5375414120549230', phone='0981229315', email='daminik@gmail.com')
person2 = User(username='Oleg_1020', password='1111', first_name='Oleg', last_name='Mat', card_number='5375414135549120', phone='0971228815', email='oleg@gmail.com')

group1 = Group(name='MyFirstGroup', password='1234', owner=person1)
group2 = Group(name='MySecondGroup', password='12345', owner=person2)

membership1 = Membership(member=person1, group=group2)
membership2 = Membership(member=person2, group=group1)

type_id1 = TypeOfTransfer(name='Electronics')
type_id2 = TypeOfTransfer(name='Food')

purchase1 = Purchase(group_owner = group1, owner = person2, name = 'Headphones', cost = 500)
purchase2 = Purchase(group_owner = group2, owner = person1, name = 'Dinner', cost = 150)
transfer1 = Transfer(amount = 100, owner = person2, transferType = type_id1, purchase = purchase1)
transfer2 = Transfer(amount = 150, owner = person1, transferType = type_id2, purchase = purchase2)
transfer3 = Transfer(amount = 150, owner = person2, transferType = type_id2, purchase = purchase2)

Session.add_all([person1, person2, group1, group2, membership1, membership2, type_id1, purchase1, purchase2, transfer1, transfer2, transfer3])
Session.commit()

people = Session.query(User).all()
groups = Session.query(Group).all()
memberShips = Session.query(Membership).all()
typeOfTrans = Session.query(TypeOfTransfer).all()
purchase1 = Session.query(Purchase).all()
trans = Session.query(Transfer).all()

for person in people:
    print(person)

for group in groups:
    print(group)

for memberShip in memberShips:
    print(memberShip)

for tof in typeOfTrans:
    print(tof)

for purchase in purchase1:
    print(purchase)

for t in trans:
    print(t)


