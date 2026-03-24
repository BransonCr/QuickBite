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

@router.get("/badge/{user_id}")
async def get_badge_status(user_id: str):
    return service.get_badge_status(user_id)

@router.post("/order/{user_id}/{order_id}")
async def order_notification(user_id: str, order_id: str):
    service.order_notification(user_id, order_id)
    return {"message": f"Notification for order {order_id} created successfully!"}


@router.post("/order-pickup/{user_id}/{order_id}")
async def order_pickup_notification(user_id: str, order_id: str):
    service.order_pickup_notification(user_id, order_id)
    return {"message": f"Pickup notification for order {order_id} created successfully!"}

@router.post("/order-delivery/{user_id}/{order_id}")
async def order_delivery_notification(user_id: str, order_id: str):
    service.order_delivery_notification(user_id, order_id)
    return {"message": f"Delivery notification for order {order_id} created successfully!"}

@router.post("/order-status-customer/{user_id}/{order_id}/{status}")
async def order_status_customer_notification(user_id: str, order_id: str, status: str):
    service.order_status_customer_notification(user_id, order_id, status)
    return {"message": f"Status update notification for order {order_id} created successfully!"}

@router.post("/order-status-restaurant/{user_id}/{order_id}/{status}")
async def order_status_restaurant_notification(user_id: str, order_id: str, status: str):
    service.order_status_restaurant_notification(restaurant_id=user_id, order_id=order_id, status=status)
    return {"message": f"Status update notification for order {order_id} created successfully!"}

@router.post("/payment-status-customer/{user_id}/{payment_id}/{order_id}/{status}")
async def payment_status_customer_notification(user_id: str, payment_id: str, order_id: str, status: str):
    service.payment_status_customer_notification(user_id, payment_id, order_id, status)
    return {"message": f"Payment status update notification for payment {payment_id} created successfully!"}
