import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException

from app.models.OrderModel import load_all, save_all
from app.schemas.Order import Order, OrderCreate, OrderUpdate, OrderStatus
from app.models.RestaurantModel import load_all as load_restaurants
from app.models.RestaurantModel import save_all as save_restaurants
from app.models.UserModel import load_all as load_users
from app.models.UserModel import save_all as save_users
from app.schemas.Restaurant import Restaurant
from app.schemas.User import User


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
            **order.model_dump(),
        )
        orders.append(new_order)
        save_all(orders)
        return new_order

    def update_order(self, order_id: str, order_update: OrderUpdate) -> Order:
        orders = load_all()
        for o in orders:
            if o.order_id == order_id:
                update_data = order_update.model_dump(exclude_unset=True)
                financial_fields = {"subtotal", "tax", "total", "delivery_fee", "tip"}
                if any(field in update_data for field in financial_fields):
                    if o.status not in [OrderStatus.CART, OrderStatus.PENDING]:
                        raise HTTPException(status_code=400, detail="Cannot modify items or totals for an order that is already confirmed.")

                if order_update.status == OrderStatus.CANCELLED:
                    if o.status in [OrderStatus.DELIVERED, OrderStatus.CANCELLED]:
                        raise HTTPException(status_code=400, detail="Cannot cancel an order that has already been delivered.")
                    o.cancelled_at = datetime.now().isoformat()


                for k, v in update_data.items():
                    setattr(o, k, v)
                
                o.updated_at = datetime.now().isoformat()
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

    def get_postal_code(self, user_id: str) -> Optional[str]:
        user = load_users()
        for u in user:
            if u.user_id == user_id:
                return u.postal_code
        return None

    def get_location(self, user_id: str) -> Optional[str]:
        user = load_users()
        for u in user:
            if u.user_id == user_id:
                return u.location
        return None

    def get_restaurant_location(self, restaurant_id: str) -> Optional[str]:
        restaurants = load_restaurants()
        for r in restaurants:
            if r.restaurant_id == restaurant_id:
                return r.location
        return None

    def measure_distance(
        self, loc1: str, loc2: str
    ) -> float:  # TODO refactor this method DONE
        if loc1.strip().lower() == loc2.strip().lower():
            return 0.0  # Delivery is still going
        else:
            return 5.5  # Delivery is complete
