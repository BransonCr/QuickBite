from pydantic import BaseModel

from app.schemas.MenuItem import MenuItem


class Restaurant(BaseModel):
    restaurant_id: str
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
