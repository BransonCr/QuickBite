from pydantic import BaseModel
from typing import Optional

class DiscountWheelRecord(BaseModel):
    user_id: str
    last_spin_date: str
    discount_percent: int
    discount_code: str
    is_redeemed: bool = False

class SpinResult(BaseModel):
    discount_percent: int
    discount_code: str
    message: str

class WheelStatus(BaseModel):
    can_spin: bool
    discount_percent: Optional[int] = None
    discount_code: Optional[str] = None
    is_redeemed: Optional[bool] = None
    next_spin_date: Optional[str] = None
    message: str