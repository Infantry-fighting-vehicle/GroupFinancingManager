from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models import BaseModel

class TypeOfTransfer(BaseModel):
    __tablename__ = "typesOfTransfer"

    id = Column('type_id', Integer, primary_key=True)
    name = Column(String(45), nullable=False)

    transfers = relationship('Transfer', backref='transferType')
    def __str__(self):
        return f"id: {self.id}\n" \
               f"name: {self.name}\n"
