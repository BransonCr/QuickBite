from pydantic import BaseModel

class Order(BaseModel):
    order_id: str
    customer_id: str
    restaurant_id: str
    status: OrderStatus
    subtotal: float
    tax: float
    delivery_fee: float
    tip: float
    total: float
    created_at: str
    updated_at: str

class OrderCreate(BaseModel):
    customer_id: str
    restaurant_id: str
    status: OrderStatus
    subtotal: float
    tax: float
    delivery_fee: float
    tip: float
    total: float

class OrderUpdate(BaseModel):
    customer_id: str
    restaurant_id: str
    status: OrderStatus
    subtotal: float
    tax: float
    delivery_fee: float
    tip: float
    total: float
    updated_at: str