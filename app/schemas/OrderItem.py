from pydantic import BaseModel
from typing import Optional

class OrderItem(BaseModel):
    order_item_id: str
    order_id: str
    item_id: str
    quantity: int
    price_at_time: float

class OrderItemCreate(BaseModel):
    order_id: str
    item_id: str
    quantity: int
    price_at_time: float

class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = None
    price_at_time: Optional[float] = None