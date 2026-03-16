from fastapi import APIRouter

from app.schemas.Order import Order, OrderCreate, OrderUpdate
from app.services.OrderService import OrderService
router = APIRouter(
    prefix="/order", 
    tags=["order"], 
    responses={404: {"description": "Not found"}}
)

service = OrderService()
@router.get("/")
async def get_all_orders():
    return service.get_orders()


@router.get("/{order_id}")
async def get_order(order_id: str):
    return service.get_order(order_id)


@router.post("/")
async def create_order(order: OrderCreate):
    return service.create_order(order)


@router.put("/{order_id}")
async def update_order(order_id: str, order: OrderUpdate):
    return service.update_order(order_id, order)


@router.delete("/{order_id}")
async def delete_order(order_id: str):
    return service.delete_order(order_id)

@router.get("/{user_id}/postal_code")
async def get_postal_code(user_id: str):
    return service.get_postal_code(user_id)

@router.get("/{user_id}/location")
async def get_user_location(user_id: str):
    return service.get_location(user_id)

@router.get("/restaurant/{restaurant_id}/location")
async def get_restaurant_location(restaurant_id: str):
    return service.get_restaurant_location(restaurant_id)

@router.get("/distance")
async def measure_distance(loc1: str, loc2: str):
    return service.measure_distance(loc1, loc2)
