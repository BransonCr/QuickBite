from datetime import timezone, datetime
import uuid

from fastapi import HTTPException

from app.models.NotificationModel import load_all, save_all
from app.schemas.Notification import Notification, NotificationCreate, NotificationUpdate

class NotificationService:
    def get_notifications(self):
        return load_all()

    def create_notification(self, notification: NotificationCreate) -> Notification:
        current_utc_aware = datetime.now(timezone.utc)
        current_utc_aware = current_utc_aware.strftime("%Y-%m-%d %H:%M:%S")
        new_notification = Notification(notification_id=str(uuid.uuid4()), **notification.model_dump(), created_at=current_utc_aware)  #
        existing = load_all()
        existing.append(new_notification)
        save_all(existing)
        return new_notification

    def update_notification(self, notification_id: str, notification: NotificationUpdate):
        notifications = load_all()
        for n in notifications:
            if n.notification_id == notification_id:
                for k, v in notification.model_dump().items():
                    setattr(n, k, v)
                save_all(notifications)
                return n
        raise HTTPException(status_code=404, detail="Notification not found")

    def delete_notification(self, notification_id: str):
        notifications = load_all()
        for n in notifications:
            if n.notification_id == notification_id:
                notifications.remove(n)
                save_all(notifications)
                return
        raise HTTPException(status_code=404, detail="Notification not found")

    def get_notification(self, notification_id: str) -> Notification:
        notifications = load_all()
        for n in notifications:
            if n.notification_id == notification_id:
                return n
        raise HTTPException(status_code=404, detail="Notification not found")
    
    def get_badge_status(self, user_id: str) ->bool: 
        notifications = load_all()
        for n in notifications:
            if n.user_id == user_id:
                return notifications[0].badge
        return False
    
    def order_notification(self, user_id: str, order_id: str):

        newNotification = NotificationCreate(
            user_id=user_id,
            message=f"Your order {order_id} has been placed successfully!",
            type="order_update",
            is_read=False,
            order_id=order_id
            
        )
        return self.create_notification(newNotification)
       

    def order_pickup_notification(self, user_id: str, order_id: str):
        notification = NotificationCreate(
            user_id=user_id,
            message=f"Your order {order_id} is out for pickup!",
            type="order_update",
            is_read=False,
            order_id=order_id
            
        )
        return self.create_notification(notification)

    def order_delivery_notification(self, user_id: str, order_id: str):
        notification = NotificationCreate(
            user_id=user_id,
            message=f"Your order {order_id} has been delivered!",
            type="order_update",
            is_read=False,
            order_id=order_id
            
        )
        return self.create_notification(notification)

    def order_status_customer_notification(self, user_id: str, order_id: str, status: str):
        notification = NotificationCreate(
            user_id=user_id,
            message=f"Your order {order_id} status has been updated to {status}!",
            type="order_update",
            is_read=False,
            order_id=order_id
            
        )
        return self.create_notification(notification) 

    def order_status_restaurant_notification(self, restaurant_id: str, order_id: str, status: str):
        notification = NotificationCreate(
            user_id=restaurant_id,
            message=f"Order {order_id} status has been updated to {status}!",
            type="order_update",
            is_read=False,
            order_id=order_id
            
        )
        return self.create_notification(notification)

    
  

