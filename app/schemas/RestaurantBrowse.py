from pydantic import BaseModel

class RestaurantBrowse(BaseModel):
    restaurant_id: str
    name: str
    location: str

class RestaurantBrowseCreate(BaseModel):
    restaurant_id: str
    name: str
    location: str

class RestaurantBrowseUpdate(BaseModel):
    restaurant_id: str
    name: str
    location: str