from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# import sqlalchemy
from config.db_connection_info import DB_URL
from models.group import Group
from models.membership import Membership
from models.purchase import Purchase
from models.transfer import Transfer

engine = create_engine(DB_URL)
BaseModel = declarative_base()

class User(BaseModel):
    __tablename__ = "users"

    id = Column('user_id', Integer, primary_key=True)
    username = Column(String(45), nullable=False)
    password = Column(String(45), nullable=False)
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
