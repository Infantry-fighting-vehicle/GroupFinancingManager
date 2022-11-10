from sqlalchemy import Column, Integer, Float, ForeignKey

from models import BaseModel

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