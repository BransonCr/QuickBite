import uuid
from fastapi import HTTPException
from typing import List
from datetime import datetime
from typing import Optional

from app.models.OrderModel import load_all, save_all
from app.schemas.Order import Order, OrderCreate, OrderUpdate

class OrderService:
    def get_orders(self) -> List[Order]:
        return load_all()

    def get_order(self, order_id: str) -> Order:
        orders = load_all()
        for o in orders:
            if o.order_id == order_id:
                return o
        raise HTTPException(status_code=404, detail="Order not found")

    def create_order(self, order: OrderCreate) -> Order:
        orders = load_all() 
        now = datetime.now().isoformat() 
        new_order = Order(
            order_id=str(uuid.uuid4()), 
            created_at=now,
            updated_at=now,
            **order.model_dump()
        )
        orders.append(new_order)
        save_all(orders)
        return new_order
    
    def update_order(self, order_id: str, order_update: OrderUpdate) -> Order:
        orders = load_all()
        for o in orders:
            if o.order_id == order_id:
                update_data = order_update.model_dump(exclude_unset=True)
                for k, v in update_data.items():
                    setattr(o, k, v)
                save_all(orders)
                return o
        raise HTTPException(status_code=404, detail="Order not found")

    def delete_order(self, order_id: str):
        orders = load_all()
        for o in orders:
            if o.order_id == order_id:
                orders.remove(o)
                save_all(orders)
                return
        raise HTTPException(status_code=404, detail="Order not found")