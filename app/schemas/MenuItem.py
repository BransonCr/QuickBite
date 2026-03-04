from unicodedata import category

from pydantic import BaseModel


class MenuItem(BaseModel):
    item_id: str
    name: str
    description: str
    price: float
    restaurant_id: str
    is_available: bool
    category: str


class MenuItemCreate(BaseModel):
    name: str
    description: str
    price: float
    restaurant_id: str
    is_available: bool
    category: str


class MenuItemUpdate(BaseModel):
    is_available: bool
    price: float
    category: str
    description: str
    item_id: str
