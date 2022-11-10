from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from marshmallow import Schema, fields

from models import BaseModel

class Group(BaseModel):
    __tablename__ = "groups"

    id = Column('group_id', Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    name = Column(String(45), nullable=False)
    secret_key = Column(String(45), nullable=False)

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
    owner_id = fields.Number()
class GroupSerializer(GroupInsensitiveSerializer):
    id = fields.Number()
    secret_key = fields.String()
