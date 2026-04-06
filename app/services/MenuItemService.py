import uuid

from fastapi import HTTPException

from app.models.MenuItemModel import load_all, save_all
from app.schemas.MenuItem import MenuItem, MenuItemCreate, MenuItemUpdate
from app.services.Restaurant_service import RestaurantService


class MenuItemService:
    def __init__(self):
        self.restaurant_service = RestaurantService()

    def _check_restaurant_exists(self, restaurant_id: str):
        if not self.restaurant_service.get_restaurant(restaurant_id):
            raise HTTPException(status_code=400, detail="Valid restaurant ID is required.")

    def get_menu_items(self):
        return load_all()
    
    def get_menu_by_restaurant(self, restaurant_id: str):
        self._check_restaurant_exists(restaurant_id)
       
        return [mi for mi in load_all() if mi.restaurant_id == restaurant_id]

    def create_menu_item(self, menu_item: MenuItemCreate) -> MenuItem:
        self._check_restaurant_exists(menu_item.restaurant_id)
        menu_items = load_all()
        
        new_menu_item = MenuItem(
            item_id=str(uuid.uuid4()), 
            **menu_item.model_dump(), 
            is_available=True
        )
        
        menu_items.append(new_menu_item)
        save_all(menu_items)
        return new_menu_item

    def update_menu_item(self, item_id: str, menu_item: MenuItemUpdate):
        menu_items = load_all()
        
       
        target_item = next((mi for mi in menu_items if mi.item_id == item_id), None)
        
        if not target_item:
            raise HTTPException(status_code=404, detail="Menu item not found")
            
        update_data = menu_item.model_dump(exclude_unset=True)
        for k, v in update_data.items():
            setattr(target_item, k, v)
            
        save_all(menu_items)
        return target_item

    def delete_menu_item(self, item_id: str):
        menu_items = load_all()
        
      
        initial_length = len(menu_items)
        menu_items = [mi for mi in menu_items if mi.item_id != item_id]
        
        if len(menu_items) == initial_length:
            raise HTTPException(status_code=404, detail="Menu item not found")
            
        save_all(menu_items)
        return {"message": "Menu item deleted"}

    def get_menu_item(self, item_id: str) -> MenuItem:
        menu_items = load_all()
        

        item = next((mi for mi in menu_items if mi.item_id == item_id), None)
        
        if item:
            return item
            
        raise HTTPException(status_code=404, detail="Menu item not found")
