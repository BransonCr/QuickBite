from fastapi import APIRouter

from app.schemas.Delivery import Delivery, DeliveryCreate, DeliveryUpdate
from app.services.DeliveryService import DeliveryService

router = APIRouter(
    prefix="/delivery", tags=["delivery"], responses={404: {"description": "Not found"}}
)

service = DeliveryService()


@router.get("/")
async def get_all_deliveries():
    return service.get_all()


@router.get("/{delivery_id}")
async def get_delivery(delivery_id: str):
    return service.get_delivery(delivery_id)


@router.post("/")
async def create_delivery(delivery: DeliveryCreate):
    return service.create_delivery(delivery)


@router.put("/{delivery_id}")
async def update_delivery(delivery_id: str, delivery: DeliveryUpdate):
    return service.update_delivery(delivery_id, delivery)


@router.delete("/{delivery_id}")
async def delete_delivery(delivery_id: str):
    return service.delete_delivery(delivery_id)
