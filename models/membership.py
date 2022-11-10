from sqlalchemy import Column, Integer, ForeignKey

from models import BaseModel

class Membership(BaseModel):
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.group_id'), nullable=False)

    def __str__(self):
        return f"id: {self.id}\n" \
               f"user_id: {self.user_id}\n" \
               f"group_id: {self.group_id}\n"
