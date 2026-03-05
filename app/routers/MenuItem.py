from fastapi import APIRouter

from app.schemas.MenuItem import MenuItem, MenuItemCreate, MenuItemUpdate

router = APIRouter(
    prefix="/menu_item", tags=["menu_item"], responses={404: {"description": "Not found"}}
)


@router.get("/")
async def get_all_menu_items():
    return {"message": "Get all menu items"}


@router.get("/{item_id}")
async def get_menu_item(item_id: str):
    return {"message": f"Get menu item {item_id}"}


@router.post("/")
async def create_menu_item(menu_item: MenuItemCreate):
    return {"message": f"Create menu item {menu_item}"}


@router.put("/{item_id}")
async def update_menu_item(item_id: str, menu_item: MenuItemUpdate):
    return {"message": f"Update menu item {item_id}"}


@router.delete("/{item_id}")
async def delete_menu_item(item_id: str):
    return {"message": f"Delete menu item {item_id}"}