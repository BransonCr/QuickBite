import uuid
from fastapi import HTTPException
from typing import List

from app.models.OrderItemModel import load_all, save_all
from app.schemas.OrderItem import OrderItem, OrderItemCreate, OrderItemUpdate

class OrderItemService:
    def get_order_items(self) -> List[OrderItem]:
        return load_all()

    def get_order_item(self, order_item_id: str) -> OrderItem:
        order_items = load_all()
        for item in order_items:
            if item.order_item_id == order_item_id:
                return item
        raise HTTPException(status_code=404, detail="Order item not found")

    def create_order_item(self, order_item: OrderItemCreate) -> OrderItem:
        order_items = load_all()
        new_item = OrderItem(order_item_id=str(uuid.uuid4()), **order_item.model_dump())
        order_items.append(new_item)
        save_all(order_items)
        return new_item

    def update_order_item(self, order_item_id: str, order_item_update: OrderItemUpdate) -> OrderItem:
        order_items = load_all()
        for item in order_items:
            if item.order_item_id == order_item_id:
                update_data = order_item_update.model_dump(exclude_unset=True)
                for k, v in update_data.items():
                    setattr(item, k, v)
                save_all(order_items)
                return item
        raise HTTPException(status_code=404, detail="Order item not found")

    def delete_order_item(self, order_item_id: str):
        order_items = load_all()
        for item in order_items:
            if item.order_item_id == order_item_id:
                order_items.remove(item)
                save_all(order_items)
                return
        raise HTTPException(status_code=404, detail="Order item not found")