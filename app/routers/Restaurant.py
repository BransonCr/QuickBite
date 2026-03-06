from fastapi import APIRouter

from app.schemas.Restaurant import Restaurant,RestaurantCreate,RestaurantUpdate

router = APIRouter(
    prefix="/restaurant",
    tags=["restaurant"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def get_all_restaurants():
    return {"message":"all restaurant is return"}


@router.get("/{restaurant_id}")
async def get_restaurant(restaurant_id: str):
    return {"restaurant_id": restaurant_id}


@router.post("/")
async def create_restaurant(restaurant: RestaurantCreate):
    return {"restaurant": restaurant}


@router.put("/{restaurant_id}")
async def update_restaurant(restaurant_id: str, restaurant: RestaurantUpdate):
    return {"restaurant_id": restaurant_id, "restaurant": restaurant}


@router.delete("/{restaurant_id}")
async def delete_restaurant(restaurant_id: str):
    return {"restaurant_id": restaurant_id}