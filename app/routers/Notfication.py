from fastapi import APIRouter

from app.schemas.Notification import Notification, NotificationCreate, NotificationUpdate
from app.services.NotificationService import NotificationService

router = APIRouter(
    prefix="/notification",
    tags=["notification"],
    responses={404: {"description": "Not found"}}
)


service = NotificationService()

@router.get("/")
async def get_all_notifications():
    return service.get_notifications()


@router.get("/{notification_id}")
async def get_notification(notification_id: str):
    return service.get_notification(notification_id)


@router.post("/")
async def create_notification(notification: NotificationCreate):
    return service.create_notification(notification)


@router.put("/{notification_id}")
async def update_notification(notification_id: str, notification: NotificationUpdate):
    return service.update_notification(notification_id, notification)


@router.delete("/{notification_id}")
async def delete_notification(notification_id: str):
    return service.delete_notification(notification_id)