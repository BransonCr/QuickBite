from pydantic import BaseModel
# TODO: Import MenuItem from the correct path

class Restaurant(BaseModel):
    # TODO change id to restaurant_id
    id: str
    owner_id: str
    name: str
    location: str
    postal_code: str
    delivery_radius: float
    is_active: bool
    menu_list: list[MenuItem]


class RestaurantCreate(BaseModel):
    owner_id: str
    name: str
    location: str
    postal_code: str
    delivery_radius: float


class RestaurantUpdate(BaseModel):
    owner_id: str
    name: str
    location: str
    postal_code: str
    delivery_radius: float
    is_active: bool
    menu_list: list[MenuItem]
