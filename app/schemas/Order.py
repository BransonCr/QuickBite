from pydantic import BaseModel
from enum import Enum

class OrderStatus(str, Enum):
    CART = "CART"
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    IN_PREPARATION = "IN_PREPARATION"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

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
    status: OrderStatus
    subtotal: float
    tax: float
    delivery_fee: float
    tip: float
    total: float
    updated_at: str