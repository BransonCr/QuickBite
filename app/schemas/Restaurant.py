from typing import Optional
from pydantic import BaseModel, Field

from app.schemas.MenuItem import MenuItem


class Restaurant(BaseModel):
    restaurant_id: str
    owner_id: str
    name: str
    location: str
    postal_code: str
    contact_info: str
    operating_hours: str
    delivery_radius: float
    is_active: bool


class RestaurantCreate(BaseModel):
    owner_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1)
    postal_code: str = Field(..., min_length=1)
    delivery_radius: float
    contact_info: str = Field(..., min_length=1)   
    operating_hours: str = Field(..., min_length=1)
   


class RestaurantUpdate(BaseModel):
    owner_id: Optional[str] = None
    name: Optional[str] = Field(None, min_length=1)
    location: Optional[str] = Field(None, min_length=1)
    postal_code: Optional[str] = Field(None, min_length=1)
    contact_info: Optional[str] = Field(None, min_length=1)
    operating_hours: Optional[str] = Field(None, min_length=1)
    delivery_radius: Optional[float] = None
    is_active: Optional[bool] = None
    menu_list: Optional[list[str]] = None
