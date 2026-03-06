from fastapi import APIRouter

from app.schemas.Notification import Notification, NotificationCreate, NotificationUpdate

router = APIRouter(
    prefix="/notification",
    tags=["notification"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def get_all_notifications():
    return {"message": "Get all notifications"}


@router.get("/{notification_id}")
async def get_notification(notification_id: str):
    return {"message": f"Get notification {notification_id}"}


@router.post("/")
async def create_notification(notification: NotificationCreate):
    return {"message": f"Create notification {notification}"}


@router.put("/{notification_id}")
async def update_notification(notification_id: str, notification: NotificationUpdate):
    return {"message": f"Update notification {notification_id}"}


@router.delete("/{notification_id}")
async def delete_notification(notification_id: str):
    return {"message": f"Delete notification {notification_id}"}