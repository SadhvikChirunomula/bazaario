from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime

class SellersRequestSchema(BaseModel):
    id: int
    seller_id: int
    poc_number: Optional[str]
    poc_email_id: Optional[str]
    address_line_1: str
    address_line_2: Optional[str]
    pincode: str
    item_id: int
    quantity: float
    image: Optional[str]
    description: Optional[str]
    price: float
    preferred_date: Optional[date]
    preferred_time: Optional[time]
    is_closed: Optional[bool]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True