from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# import sqlalchemy
from config.db_connection_info import DB_URL

engine = create_engine(DB_URL)
BaseModel = declarative_base()

SessionFactory = sessionmaker(bind=engine)
Session = SessionFactory()

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
