from fastapi import APIRouter

from app.models.OrderModel import load_all as load_orders
from app.models.RestaurantModel import load_all as load_restaurants
from app.models.UserModel import load_all as load_users

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats")
async def get_stats():
    users = load_users()
    orders = load_orders()
    restaurants = load_restaurants()

    users_by_role = {}
    for u in users:
        r = u.role.value
        users_by_role[r] = users_by_role.get(r, 0) + 1

    orders_by_status = {}
    for o in orders:
        s = o.status.value
        orders_by_status[s] = orders_by_status.get(s, 0) + 1

    total_revenue = sum(o.total for o in orders if o.status.value == "DELIVERED")

    return {
        "users_count": len(users),
        "orders_count": len(orders),
        "restaurants_count": len(restaurants),
        "active_restaurants": sum(1 for r in restaurants if r.is_active),
        "total_revenue": round(total_revenue, 2),
        "users_by_role": users_by_role,
        "orders_by_status": orders_by_status,
    }
