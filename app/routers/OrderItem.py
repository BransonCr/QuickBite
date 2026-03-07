from fastapi import APIRouter

from app.schemas.OrderItem import OrderItem, OrderItemCreate, OrderItemUpdate

router = APIRouter(
    prefix="/orderitem",
    tags=["orderitem"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def get_all_orderitems():
    return {"message": "Get all order items"}


@router.get("/{orderitem_id}")
async def get_orderitem(orderitem_id: str):
    return {"message": f"Get order item {orderitem_id}"}


@router.post("/")
async def create_orderitem(orderitem: OrderItemCreate):
    return {"message": f"Create order item {orderitem}"}


@router.put("/{orderitem_id}")
async def update_orderitem(orderitem_id: str, orderitem: OrderItemUpdate):
    return {"message": f"Update order item {orderitem_id}"}


@router.delete("/{orderitem_id}")
async def delete_orderitem(orderitem_id: str):
    return {"message": f"Delete order item {orderitem_id}"}