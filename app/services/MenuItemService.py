import uuid

from fastapi import HTTPException

from app.models.MenuItemModel import load_all, save_all
from app.schemas.MenuItem import MenuItem, MenuItemCreate, MenuItemUpdate


class MenuItemService:
    def get_menu_items(self):
        return load_all()

    def create_menu_item(self, menu_item: MenuItemCreate) -> MenuItem:
        new_menu_item = MenuItem(item_id=str(uuid.uuid4()), **menu_item.model_dump(), is_available=True)  #
        save_all([new_menu_item])
        return new_menu_item

    def update_menu_item(self, item_id: str, menu_item: MenuItemUpdate):
        menu_items = load_all()
        for mi in menu_items:
            if mi.item_id == item_id:
                for k, v in menu_item.model_dump().items():
                    setattr(mi, k, v)
                save_all(menu_items)
                return mi
        raise HTTPException(status_code=404, detail="Menu item not found")

    def delete_menu_item(self, item_id: str):
        menu_items = load_all()
        for mi in menu_items:
            if mi.item_id == item_id:
                menu_items.remove(mi)
                save_all(menu_items)
                return True
        raise HTTPException(status_code=404, detail="Menu item not found")

    def get_menu_item(self, item_id: str) -> MenuItem:
        menu_items = load_all()
        for mi in menu_items:
            if mi.item_id == item_id:
                return mi
        raise HTTPException(status_code=404, detail="Menu item not found")