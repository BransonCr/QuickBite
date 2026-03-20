import uuid
from fastapi import HTTPException
from typing import List

from app.models.OrderItemModel import load_all, save_all
from app.schemas.OrderItem import OrderItem, OrderItemCreate, OrderItemUpdate
from app.services.OrderService import OrderService
from app.services.MenuItemService import MenuItemService
from app.schemas.Order import OrderStatus

class OrderItemService:
    def __init__(self):
        self.order_service = OrderService()
        self.menu_item_service = MenuItemService()

    def _check_order_modifiable(self,order_id:str):
        order = self.order_service.get_order(order_id)
        if order.status not in [OrderStatus.CART, OrderStatus.PENDING]:
            raise HTTPException(status_code=400, detail="Cannot modify items. The order is already confirmed or completed.")
        return order

    def get_order_items(self) -> List[OrderItem]:
        return load_all()

    def get_order_item(self, order_item_id: str) -> OrderItem:
        order_items = load_all()
        for item in order_items:
            if item.order_item_id == order_item_id:
                return item
        raise HTTPException(status_code=404, detail="Order item not found")

    def create_order_item(self, order_item: OrderItemCreate) -> OrderItem:
        parent_order = self._check_order_modifiable(order_item.order_id)
        menu_item = self.menu_item_service.get_menu_item(order_item.item_id)
        if menu_item.restaurant_id != parent_order.restaurant_id:
            raise HTTPException(status_code=400, detail="Cannot add items from multiple restaurants to the same order.")
        
        order_items = load_all()
        new_item = OrderItem(order_item_id=str(uuid.uuid4()), **order_item.model_dump())
        order_items.append(new_item)
        save_all(order_items)
        return new_item

    def update_order_item(self, order_item_id: str, order_item_update: OrderItemUpdate) -> OrderItem:
        order_items = load_all()
        for item in order_items:
            if item.order_item_id == order_item_id:
                self._check_order_modifiable(item.order_id)

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
                self._check_order_modifiable(item.order_id)

                order_items.remove(item)
                save_all(order_items)
                return {"message": "Order item deleted"}
        raise HTTPException(status_code=404, detail="Order item not found")