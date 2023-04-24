from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from marshmallow import Schema, fields

from models import BaseModel
from .user import UserSerializer

class Group(BaseModel):
    __tablename__ = "groups"

    id = Column('group_id', Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    secret_key = Column(String(45), nullable=False, unique=True)

    members = relationship('Membership', backref='group')
    purchases = relationship('Purchase', backref='group_owner')
    def __str__(self):
        return f"id: {self.id}\n" \
               f"owner_id: {self.owner_id}\n" \
               f"name: {self.name}\n" \
               f"password: {self.secret_key}\n"

class GroupBasicSerializer(Schema):
    name = fields.String()
class GroupInsensitiveSerializer(GroupBasicSerializer):
    id = fields.Integer()
    owner_id = fields.Number()
class GroupSerializer(GroupInsensitiveSerializer):
    id = fields.Number()

class GroupSensitiveSerialzier(GroupInsensitiveSerializer):
    secret_key = fields.String()

class MembershipSerializer(Schema):
    user = fields.Nested(UserSerializer)
    # group = fields.Nested(GroupSerializer)

class FullGroupSerializer(Schema):
    id = fields.Int()
    name = fields.Str()
    members = fields.Nested('MembershipSerializer', many=True)

