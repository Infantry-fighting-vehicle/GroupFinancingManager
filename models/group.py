from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# import sqlalchemy
from config.db_connection_info import DB_URL

engine = create_engine(DB_URL)
BaseModel = declarative_base()

class Group(BaseModel):
    __tablename__ = "groups_"

    id = Column('group_id', Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(45), nullable=False)
    password = Column(String(45), nullable=False)

    members = relationship('Membership', backref='group')
    purchases = relationship('Purchase', backref='group_owner')
    def __str__(self):
        return f"id: {self.id}\n" \
               f"owner_id: {self.owner_id}\n" \
               f"name: {self.name}\n" \
               f"password: {self.password}\n"
