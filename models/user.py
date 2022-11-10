from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import relationship

from models import Group, Membership, Purchase, Transfer, BaseModel
from marshmallow import Schema, fields

class User(BaseModel):
    __tablename__ = "users"

    id = Column('user_id', Integer, primary_key=True)
    username = Column(String(45), nullable=False)
    password = Column(String(120), nullable=False)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    card_number = Column(String(45), nullable=False)
    phone = Column(String(45), nullable=False)
    email = Column(String(45), nullable=False)

    groups = relationship(Group, backref='owner')
    memberShips = relationship(Membership, backref='member')
    purchases = relationship(Purchase, backref='owner')
    transfers = relationship(Transfer, backref='owner')
    
    def __str__(self):
        return f"id: {self.id}\n" \
               f"username: {self.username}\n" \
               f"password: {self.password}\n" \
               f"first_name: {self.first_name}\n" \
               f"last_name: {self.last_name}\n" \
               f"card_number: {self.card_number}\n" \
               f"phone: {self.phone}\n" \
               f"email: {self.email}\n"

class UserCardSerializer(Schema):
    username = fields.String()
    first_name = fields.String()
    last_name = fields.String()

class UserInsensetiveSerializer(UserCardSerializer):
    card_number = fields.String()
    phone = fields.String()
    email = fields.Email()

class UserSerializer(UserInsensetiveSerializer):
    id = fields.Number()
    password = fields.String()