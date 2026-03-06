from fastapi import APIRouter


from app.schemas.Restaurant import Restaurant,RestaurantCreate,RestaurantUpdate


router = APIRouter(
    prefix="/restaurant", tags=["restaurant"], responses={404: {"description": "Not found"}}
)


@router.post("/")
def create_restaurant(restaurant: Restaurant):
    return {"restaurant": restaurant}


@router.get("/{restaurant_id}")
def read_restaurant(restaurant_id: str):
    return {"restaurant_id": restaurant_id}

@router.put("/{restaurant_id}")
def update_restaurant(restaurant_id: str, restaurant: Restaurant):
    return {"restaurant_id": restaurant_id, "restaurant": restaurant}

@router.delete("/{restaurant_id}")
def delete_restaurant(restaurant_id: str):
    return {"restaurant_id": restaurant_id}