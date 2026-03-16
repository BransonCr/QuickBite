import uuid
from fastapi import HTTPException
from typing import List
from datetime import datetime
from typing import Optional

from app.models.OrderModel import load_all, save_all
from app.models.UserModel import load_all as load_users, save_all as save_users
from app.models.RestaurantModel import load_all as load_restaurants, save_all as save_restaurants   
from app.schemas.Order import Order, OrderCreate, OrderUpdate
from app.schemas.User import User
from app.schemas.Restaurant import Restaurant
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
    def get_postal_code(self,user_id: str) -> Optional[str]:
        user = load_users()
        for u in user:
            if u.user_id == user_id:
                return u.postal_code
        return None
    def get_location(self,user_id: str) -> Optional[str]:
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
    
    def measure_distance(self, loc1: str, loc2: str) -> float: #TODO refactor this method
        if loc1 > loc2:
            return 1
        elif loc1 < loc2:
            return -1
        else: 
            return 0 
