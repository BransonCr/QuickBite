from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

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
    subtotal: float = Field(..., ge=0)
    tax: float = Field(..., ge=0)
    delivery_fee: float = Field(..., ge=0)
    tip: float = Field(..., ge=0)
    total: float = Field(..., ge=0)
    created_at: str
    updated_at: str
    cancellation_reason: Optional[str] = None
    cancelled_at: Optional[str] = None

class OrderCreate(BaseModel):
    customer_id: str
    restaurant_id: str
    status: OrderStatus = OrderStatus.CART
    subtotal: float = 0.0
    tax: float = 0.0
    delivery_fee: float = 0.0
    tip: float = 0.0
    total: float = 0.0

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    delivery_fee: Optional[float] = None
    tip: Optional[float] = None
    total: Optional[float] = None
    updated_at: Optional[str] = None