from typing import Literal, Optional
from pydantic import BaseModel

class RestaurantBrowse(BaseModel):
    restaurant_id: str
    name: str
    location: str
    average_price: float
    price_category: Optional[Literal["$", "$$", "$$$"]] = None

class RestaurantBrowseCreate(BaseModel):
    restaurant_id: str
    name: str
    location: str
    average_price: float
    price_category: Optional[Literal["$", "$$", "$$$"]] = None

class RestaurantBrowseUpdate(BaseModel):
    restaurant_id: str
    name: str
    location: str
    average_price: float
    price_category: Optional[Literal["$", "$$", "$$$"]] = None