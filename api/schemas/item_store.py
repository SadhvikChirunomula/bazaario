from pydantic import BaseModel
from typing import Optional

class ItemStoreSchema(BaseModel):
    id: int
    item_name: str
    description: Optional[str] = None
    price: float
    quantity: int
    seller_id: int

    class Config:
        orm_mode = True