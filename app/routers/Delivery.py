from fastapi import APIRouter

from app.schemas.Delivery import Delivery, DeliveryCreate, DeliveryUpdate

router = APIRouter(
    prefix="/delivery", tags=["delivery"], responses={404: {"description": "Not found"}}
)


@router.get("/")
async def get_all_deliveries():
    return {"message": "Get all deliveries"}


@router.get("/{delivery_id}")
async def get_delivery(delivery_id: str):
    return {"message": f"Get delivery {delivery_id}"}


@router.post("/")
async def create_delivery(delivery: DeliveryCreate):
    return {"message": f"Create delivery {delivery}"}


@router.put("/{delivery_id}")
async def update_delivery(delivery_id: str, delivery: DeliveryUpdate):
    return {"message": f"Update delivery {delivery_id}"}


@router.delete("/{delivery_id}")
async def delete_delivery(delivery_id: str):
    return {"message": f"Delete delivery {delivery_id}"}
