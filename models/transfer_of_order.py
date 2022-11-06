from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# import sqlalchemy
from config.db_connection_info import DB_URL

engine = create_engine(DB_URL)
BaseModel = declarative_base()

SessionFactory = sessionmaker(bind=engine)
Session = SessionFactory()

class TypeOfTransfer(BaseModel):
    __tablename__ = "typesOfTransfer"

    id = Column('type_id', Integer, primary_key=True)
    name = Column(String(45), nullable=False)

    transfers = relationship('Transfer', backref='transferType')
    def __str__(self):
        return f"id: {self.id}\n" \
               f"name: {self.name}\n"
