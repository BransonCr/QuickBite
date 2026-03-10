from fastapi import APIRouter

from app.schemas.Restaurant import Restaurant,RestaurantCreate,RestaurantUpdate
from app.services.Restaurant_service import RestaurantService
router = APIRouter(
    prefix="/restaurant",
    tags=["restaurant"],
    responses={404: {"description": "Not found"}}
)


service = RestaurantService()

@router.get("/")
async def get_all_restaurants():
    return service.get_all_restaurants()


@router.get("/{restaurant_id}")
async def get_restaurant(restaurant_id: str):
    return service.get_restaurant(restaurant_id)


@router.post("/")
async def create_restaurant(restaurant: RestaurantCreate):
    return service.create_restaurant(restaurant)


@router.put("/{restaurant_id}")
async def update_restaurant(restaurant_id: str, restaurant: RestaurantUpdate):
    return service.update_restaurant(restaurant_id, restaurant)


@router.delete("/{restaurant_id}")
async def delete_restaurant(restaurant_id: str):
    return service.delete_restaurant(restaurant_id)
