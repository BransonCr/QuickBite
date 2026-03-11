from fastapi import APIRouter

from app.schemas.MenuItem import MenuItem, MenuItemCreate, MenuItemUpdate
from app.services.MenuItemService import MenuItemService

router = APIRouter(
    prefix="/menuitem",
    tags=["menu_item"],
    responses={404: {"description": "Not found"}}
)

service = MenuItemService()


@router.get("/")
async def get_all_menu_items():
    return service.get_menu_items()


@router.get("/{item_id}")
async def get_menu_item(item_id: str):
    return service.get_menu_item(item_id)


@router.post("/")
async def create_menu_item(menu_item: MenuItemCreate):
    return service.create_menu_item(menu_item)


@router.put("/{item_id}")
async def update_menu_item(item_id: str, menu_item: MenuItemUpdate):
    return service.update_menu_item(item_id, menu_item)


@router.delete("/{item_id}")
async def delete_menu_item(item_id: str):
    return service.delete_menu_item(item_id)