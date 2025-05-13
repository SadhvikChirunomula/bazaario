from sqlalchemy import Column, Integer, String
from api.db.database import Base

class ItemStore(Base):
    __tablename__ = "items_store"  # <-- double underscores

    id = Column(Integer, primary_key=True, index=True)
    item_type = Column(String(100), nullable=False)
    unit = Column(String(20), nullable=False)