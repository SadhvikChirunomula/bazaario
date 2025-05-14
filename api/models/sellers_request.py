from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, Date, Time, Text, ForeignKey, TIMESTAMP
from api.db.database import Base

class SellersRequest(Base):
    __tablename__ = "sellers_requests"  # <-- double underscores

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    poc_number = Column(String(20))
    poc_email_id = Column(String(100))
    address_line_1 = Column(String(255), nullable=False)
    address_line_2 = Column(String(255))
    pincode = Column(String(10), nullable=False)
    item_id = Column(Integer, ForeignKey("items_store.id"), nullable=False)
    quantity = Column(DECIMAL(10, 2), nullable=False)
    image = Column(String(255))
    description = Column(Text)
    price = Column(DECIMAL(10, 2), nullable=False)
    preferred_date = Column(Date)
    preferred_time = Column(Time)
    is_closed = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP)