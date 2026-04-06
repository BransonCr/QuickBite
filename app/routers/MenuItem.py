from fastapi import APIRouter, Depends

from app.schemas.MenuItem import MenuItem, MenuItemCreate, MenuItemUpdate
from app.services.MenuItemService import MenuItemService

router = APIRouter(
    prefix="/menuitem",
    tags=["menu_item"],
    responses={404: {"description": "Not found"}}
)

service = MenuItemService()


@router.get("/categories")
async def get_all_categories(service: MenuItemService = Depends()):
    return service.get_all_categories()

@router.get("/")
async def get_all_menu_items(service: MenuItemService = Depends()):
    return service.get_menu_items()

@router.get("/restaurant/{restaurant_id}")
async def get_menu_by_restaurant(restaurant_id: str, service: MenuItemService = Depends()):
    return service.get_menu_by_restaurant(restaurant_id)

@router.get("/{item_id}")
async def get_menu_item(item_id: str, service: MenuItemService = Depends()):
    return service.get_menu_item(item_id)


@router.post("/")
async def create_menu_item(menu_item: MenuItemCreate, service: MenuItemService = Depends()):
    return service.create_menu_item(menu_item)


@router.put("/{item_id}")
async def update_menu_item(item_id: str, menu_item: MenuItemUpdate, service: MenuItemService = Depends()):
    return service.update_menu_item(item_id, menu_item)


@router.delete("/{item_id}")
async def delete_menu_item(item_id: str, service: MenuItemService = Depends()):
    return service.delete_menu_item(item_id)