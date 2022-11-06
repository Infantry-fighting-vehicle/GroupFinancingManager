from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# import sqlalchemy
from config.db_connection_info import DB_URL

engine = create_engine(DB_URL)
BaseModel = declarative_base()

SessionFactory = sessionmaker(bind=engine)
Session = SessionFactory()

class Membership(BaseModel):
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    group_id = Column(Integer, ForeignKey('groups_.group_id'), nullable=False)

    def __str__(self):
        return f"id: {self.id}\n" \
               f"user_id: {self.user_id}\n" \
               f"group_id: {self.group_id}\n"
