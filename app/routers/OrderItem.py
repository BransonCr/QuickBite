from fastapi import APIRouter, Depends
from typing import List

from app.schemas.OrderItem import OrderItem, OrderItemCreate, OrderItemUpdate
from app.services.OrderItemService import OrderItemService

router = APIRouter(
    prefix="/orderitem",
    tags=["orderitem"],
    responses={404: {"description": "Not found"}}
)


@router.get("/order/{order_id}", response_model=List[OrderItem])
async def get_orderitems_by_order_id(order_id: str, service: OrderItemService = Depends()):
    return service.get_order_items_by_order_id(order_id)

@router.delete("/order/{order_id}")
async def delete_orderitems_by_order_id(order_id: str, service: OrderItemService = Depends()):
    return service.delete_order_items_by_order_id(order_id)

@router.get("/", response_model=List[OrderItem])
async def get_all_orderitems(service: OrderItemService = Depends()):
    return service.get_order_items()

@router.get("/{orderitem_id}", response_model= OrderItem)
async def get_orderitem(orderitem_id: str, service: OrderItemService = Depends()):
    return service.get_order_item(orderitem_id)


@router.post("/", response_model=OrderItem)
async def create_orderitem(orderitem: OrderItemCreate, service: OrderItemService= Depends()):
    return service.create_order_item(orderitem)


@router.put("/{orderitem_id}", response_model=OrderItem)
async def update_orderitem(orderitem_id: str, orderitem: OrderItemUpdate, service: OrderItemService=Depends()):
    return service.update_order_item(orderitem_id, orderitem)


@router.delete("/{orderitem_id}")
async def delete_orderitem(orderitem_id: str, service: OrderItemService = Depends()):
    return service.delete_order_item(orderitem_id)