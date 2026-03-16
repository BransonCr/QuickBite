from typing import Optional
from pydantic import BaseModel
from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class Payment(BaseModel):
    payment_id: str
    order_id: str
    amount: float
    status: PaymentStatus
    confirmation_number: Optional[str] = None,
    card_number: str
    expiration_date: str
    cvv: str
    created_at: str

class PaymentCreate(BaseModel):
    order_id: str
    amount: float
    card_number: str
    expiration_date: str
    cvv: str

class PaymentUpdate(BaseModel):
    status: PaymentStatus