from pydantic import BaseModel

class MenuItem(BaseModel):
    item_id: str
    restaurant_id: str
    name: str
    description: str
    price: float
    is_available: bool
    category: str
class MenuItemCreate(BaseModel):
    restaurant_id: str
    name: str
    description: str
    price: float
    category: str
class MenuItemUpdate(BaseModel):
    restaurant_id: str
    name: str
    description: str
    price: float
    is_available: bool
    category: str