from pydantic import BaseModel

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
    quantity: int
    price_at_time: float