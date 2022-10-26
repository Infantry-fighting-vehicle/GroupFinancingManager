from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# import sqlalchemy
from db_connection_info import DB_URL

engine = create_engine(DB_URL)
BaseModel = declarative_base()

SessionFactory = sessionmaker(bind=engine)
Session = SessionFactory()

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

    groups = relationship('Group', backref='owner')
    memberShips = relationship('Membership', backref='member')
    purchases = relationship('Purchase', backref='owner')
    transfers = relationship('Transfer', backref='owner')
    
    def __str__(self):
        return f"id: {self.id}\n" \
               f"username: {self.username}\n" \
               f"password: {self.password}\n" \
               f"first_name: {self.first_name}\n" \
               f"last_name: {self.last_name}\n" \
               f"card_number: {self.card_number}\n" \
               f"phone: {self.phone}\n" \
               f"email: {self.email}\n"

class Group(BaseModel):
    __tablename__ = "groups_"

    id = Column('group_id', Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    name = Column(String(45), nullable=False)
    password = Column(String(45), nullable=False)

    members = relationship('Membership', backref='group')
    purchases = relationship('Purchase', backref='group_owner')
    def __str__(self):
        return f"id: {self.id}\n" \
               f"owner_id: {self.owner_id}\n" \
               f"name: {self.name}\n" \
               f"password: {self.password}\n"

class Membership(BaseModel):
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    group_id = Column(Integer, ForeignKey('groups_.group_id'), nullable=False)

    def __str__(self):
        return f"id: {self.id}\n" \
               f"user_id: {self.user_id}\n" \
               f"group_id: {self.group_id}\n"

class Purchase(BaseModel):
    __tablename__ = "purchases"

    id = Column('purchase_id', Integer, primary_key=True)

    group_id = Column(Integer, ForeignKey('groups_.group_id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    name = Column(String(45), nullable=False)
    cost = Column(Float, nullable=False)

    transfers = relationship('Transfer', backref='purchase')
    def __str__(self):
        return f"id: {self.id}\n" \
               f"group_id: {self.group_id}\n" \
               f"owner_id: {self.owner_id}\n" \
               f"name: {self.name}\n" \
               f"cost: {self.cost}\n" 

class TypeOfTransfer(BaseModel):
    __tablename__ = "typesOfTransfer"

    id = Column('type_id', Integer, primary_key=True)
    name = Column(String(45), nullable=False)

    transfers = relationship('Transfer', backref='transferType')
    def __str__(self):
        return f"id: {self.id}\n" \
               f"name: {self.name}\n"

class Transfer(BaseModel):
    __tablename__ = "transfers"

    id = Column('transfer_id', Integer, primary_key=True)
    amount = Column(Float, nullable=False)

    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    type_id = Column(Integer, ForeignKey('typesOfTransfer.type_id'), nullable=False)
    purchase_id = Column(Integer, ForeignKey('purchases.purchase_id'), nullable=False)

    def __str__(self):
        return f"id: {self.id}\n" \
               f"amount: {self.amount}\n" \
               f"user_id: {self.user_id}\n" \
               f"type_id: {self.type_id}\n" \
               f"purchase_id: {self.purchase_id}\n"