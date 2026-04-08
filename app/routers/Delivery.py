from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user, require_role
from app.schemas.Delivery import DeliveryCreate, DeliveryStatusUpdate, DeliveryUpdate
from app.schemas.User import UserRole
from app.services.DeliveryService import DeliveryService

router = APIRouter(
    prefix="/delivery", tags=["delivery"], responses={404: {"description": "Not found"}}
)

service = DeliveryService()


@router.get("/")
async def get_all_deliveries():
    return service.get_all()


@router.get("/order/{order_id}")
async def get_delivery_by_order(order_id: str):
    return service.get_by_order_id(order_id)


@router.get("/{delivery_id}", dependencies=[Depends(get_current_user)])
async def get_delivery(delivery_id: str):
    return service.get_delivery(delivery_id)


@router.post("/")
async def create_delivery(delivery: DeliveryCreate):
    return service.create_delivery(delivery)


@router.put("/{delivery_id}", dependencies=[Depends(require_role([UserRole.ADMIN, UserRole.RESTAURANT_OWNER]))])
async def update_delivery(delivery_id: str, delivery: DeliveryUpdate):
    return service.update_delivery(delivery_id, delivery)


@router.patch("/{delivery_id}/status", dependencies=[Depends(require_role([UserRole.ADMIN, UserRole.RESTAURANT_OWNER]))])
async def update_delivery_status(delivery_id: str, body: DeliveryStatusUpdate):
    return service.update_status(delivery_id, body.status)


@router.delete("/{delivery_id}", dependencies=[Depends(require_role([UserRole.ADMIN]))])
async def delete_delivery(delivery_id: str):
    return service.delete_delivery(delivery_id)
