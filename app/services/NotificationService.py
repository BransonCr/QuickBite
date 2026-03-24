import uuid
from datetime import datetime, timezone
from fastapi import HTTPException

from app.models.NotificationModel import load_all, save_all
from app.schemas.Notification import Notification, NotificationCreate, NotificationUpdate

class NotificationService:
    def get_notifications(self):
        return load_all()

    def create_notification(self, notification: NotificationCreate) -> Notification:
        notifications = load_all()
        
       
        created_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        
        new_notification = Notification(
            notification_id=str(uuid.uuid4()), 
            **notification.model_dump(), 
            created_at=created_at
        )
        
        notifications.append(new_notification)
        save_all(notifications)
        return new_notification

    def update_notification(self, notification_id: str, notification_update: NotificationUpdate) -> Notification:
        notifications = load_all()
        
 
        target_notification = next((n for n in notifications if n.notification_id == notification_id), None)
        
        if not target_notification:
            raise HTTPException(status_code=404, detail="Notification not found")
            
       
        update_data = notification_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(target_notification, key, value)
            
        save_all(notifications)
        return target_notification

    def delete_notification(self, notification_id: str):
        notifications = load_all()
        
        
        initial_length = len(notifications)
        notifications = [n for n in notifications if n.notification_id != notification_id]
        
        if len(notifications) == initial_length:
            raise HTTPException(status_code=404, detail="Notification not found")
            
        save_all(notifications)

    def get_notification(self, notification_id: str) -> Notification:
        notifications = load_all()
        
        
        notification = next((n for n in notifications if n.notification_id == notification_id), None)
        if notification:
            return notification
            
        raise HTTPException(status_code=404, detail="Notification not found")
    
    def get_badge_status(self, user_id: str) -> bool: 
        notifications = load_all()
        for n in notifications:
            if n.user_id == user_id:
                #Now it returns value belonging to the matched notification.
                return n.badge
        return False
    
    # --- Helper Methods ---

    def order_notification(self, user_id: str, order_id: str) -> Notification:
        new_notification = NotificationCreate(
            user_id=user_id,
            message=f"Your order {order_id} has been placed successfully!",
            type="order_update",
            is_read=False,
            order_id=order_id
        )
        return self.create_notification(new_notification)

    def order_pickup_notification(self, user_id: str, order_id: str) -> Notification:
        notification = NotificationCreate(
            user_id=user_id,
            message=f"Your order {order_id} is out for pickup!",
            type="order_update",
            is_read=False,
            order_id=order_id
        )
        return self.create_notification(notification)

    def order_delivery_notification(self, user_id: str, order_id: str) -> Notification:
        notification = NotificationCreate(
            user_id=user_id,
            message=f"Your order {order_id} has been delivered!",
            type="order_update",
            is_read=False,
            order_id=order_id
        )
        return self.create_notification(notification)

    def order_status_customer_notification(self, user_id: str, order_id: str, status: str) -> Notification:
        notification = NotificationCreate(
            user_id=user_id,
            message=f"Your order {order_id} status has been updated to {status}!",
            type="order_update",
            is_read=False,
            order_id=order_id
        )
        return self.create_notification(notification) 

    def order_status_restaurant_notification(self, restaurant_id: str, order_id: str, status: str) -> Notification:
        notification = NotificationCreate(
            user_id=restaurant_id,
            message=f"Order {order_id} status has been updated to {status}!",
            type="order_update",
            is_read=False,
            order_id=order_id
        )
        return self.create_notification(notification)
    
    def payment_status_customer_notification(self, user_id: str, payment_id: str, order_id: str, status: str) -> Notification:
        notification = NotificationCreate(
            user_id=user_id,
            message=set_payment_message(payment_id, order_id, status),
            type="payment_update",
            is_read=False,
            order_id=order_id
        )
        return self.create_notification(notification)

# --- Global Functions ---

def set_payment_message(payment_id: str, order_id: str, status: str) -> str:
    if status == "FAILED":
        return f"Your payment {payment_id} for order {order_id} has failed. Please try again."
    elif status == "SUCCESS":
        return f"Your payment {payment_id} for order {order_id} was successful! Thank you for your purchase."
    elif status == "PENDING":
        return f"Your payment {payment_id} for order {order_id} is pending. We will notify you once it is processed."
    
    return f"Your payment {payment_id} for order {order_id} has an unknown payment status: {status}."
