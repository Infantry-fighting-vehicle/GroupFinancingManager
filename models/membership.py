from email.policy import default
import enum
from sqlalchemy import Column, Integer, ForeignKey, Enum

from models import BaseModel

class UserStatus(enum.Enum):
    UNACCEPTED = 0
    ACCEPTED = 1
    BANNED = 2
class Membership(BaseModel):
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.group_id'), nullable=False)
    status = Column(Enum(UserStatus), default=False, nullable=False)

    def __str__(self):
        return f"id: {self.id}\n" \
               f"user_id: {self.user_id}\n" \
               f"group_id: {self.group_id}\n"
