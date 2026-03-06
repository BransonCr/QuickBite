from enum import Enum

from pydantic import BaseModel


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class Payment(BaseModel):
    payment_id: str
    order_id: str
    amount: float
    status: PaymentStatus
    confirmation_number: str
    card_last_four: str
    created_at: str


class PaymentCreate(BaseModel):
    order_id: str
    amount: float
    card_last_four: str


class PaymentUpdate(BaseModel):
    status: PaymentStatus