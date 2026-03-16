from pydantic import BaseModel, Field
from typing import Optional

class MenuItem(BaseModel):
    item_id: str
    restaurant_id: str
    name: str
    description: str
    price: float
    is_available: bool
    category: str

class MenuItemCreate(BaseModel):
    restaurant_id: str = Field(..., min_length=1, description="Must link to a restaurant")
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    category: str = Field(..., min_length=1)
    
class MenuItemUpdate(BaseModel):
    restaurant_id: Optional[str] = Field(None, min_length=1)
    name: Optional[str]= Field(None, min_length=1)
    description: Optional[str] = Field(None, min_length=1)
    price: Optional[float] = Field(None, gt=1)
    is_available: Optional[bool] = None
    category: Optional[str] = Field(None, min_length=1)