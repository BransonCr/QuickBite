from pydantic import BaseModel

class Notification(BaseModel):
    notification_id: str
    user_id: str
    order_id: str
    message: str
    type: str
    is_read: bool
    created_at: str

class NotificationCreate(BaseModel):
    user_id: str
    order_id: str
    message: str
    type: str
    is_read: bool

class NotificationUpdate(BaseModel):
    user_id: str
    order_id: str
    message: str
    type: str
    is_read: bool