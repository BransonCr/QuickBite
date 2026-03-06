from fastapi import APIRouter

from app.schemas.Order import Order, OrderCreate, OrderUpdate

router = APIRouter(
    prefix="/order", 
    tags=["order"], 
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def get_all_orders():
    return {"message": "Get all orders"}


@router.get("/{order_id}")
async def get_order(order_id: str):
    return {"message": f"Get order {order_id}"}


@router.post("/")
async def create_order(order: OrderCreate):
    return {"message": f"Create order {order}"}


@router.put("/{order_id}")
async def update_order(order_id: str, order: OrderUpdate):
    return {"message": f"Update order {order_id}"}


@router.delete("/{order_id}")
async def delete_order(order_id: str):
    return {"message": f"Delete order {order_id}"}