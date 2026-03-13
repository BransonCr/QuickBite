from datetime import UTC, datetime
import uuid

from fastapi import HTTPException

from app.models.NotificationModel import load_all, save_all
from app.schemas.Notification import Notification, NotificationCreate, NotificationUpdate


class NotificationService:
    def get_notifications(self):
        return load_all()

    def create_notification(self, notification: NotificationCreate) -> Notification:
        current_utc_aware = datetime.now(UTC)
        current_utc_aware = current_utc_aware.strftime("%Y-%m-%d %H:%M:%S")
        new_notification = Notification(notification_id=str(uuid.uuid4()), **notification.model_dump(), created_at=current_utc_aware)  #
        save_all([new_notification])
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