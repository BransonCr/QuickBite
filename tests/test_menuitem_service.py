from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.schemas.MenuItem import MenuItem, MenuItemCreate, MenuItemUpdate
from app.services.MenuItemService import MenuItemService


def make_menu_item(item_id="abc-123"):
    return MenuItem(
        item_id=item_id,
        restaurant_id="rest-1",
        name="Pepperoni Pizza",
        description="Delicious pepperoni pizza with a crispy crust.",
        price=12.99,
        is_available=True,
        category="Italian"
    )


def make_menu_item_create():
    return MenuItemCreate(
        restaurant_id="rest-1",
        name="Pepperoni Pizza",
        description="Delicious pepperoni pizza with a crispy crust.",
        price=12.99,
        category="Italian"
    )


@patch("app.services.MenuItemService.load_all")
def test_get_menu_items(mock_load):
    mock_load.return_value = [make_menu_item()]
    service = MenuItemService()
    result = service.get_menu_items()
    assert len(result) == 1
    assert result[0].category == "Italian"


@patch("app.services.MenuItemService.load_all")
def test_get_menu_item_found(mock_load):
    mock_load.return_value = [make_menu_item("abc-123")]
    service = MenuItemService()
    result = service.get_menu_item("abc-123")
    assert result.item_id == "abc-123"


@patch("app.services.MenuItemService.load_all")
def test_get_menu_item_not_found(mock_load):
    mock_load.return_value = []
    service = MenuItemService()
    with pytest.raises(HTTPException) as exc:
        service.get_menu_item("does-not-exist")
    assert exc.value.status_code == 404


@patch("app.services.MenuItemService.save_all")
@patch("app.services.MenuItemService.load_all")
def test_create_menu_item(mock_load, mock_save):
    mock_load.return_value = []
    service = MenuItemService()
    result = service.create_menu_item(make_menu_item_create())
    assert result.name == "Pepperoni Pizza"
    assert result.item_id is not None
    mock_save.assert_called_once()


@patch("app.services.MenuItemService.save_all")
@patch("app.services.MenuItemService.load_all")
def test_update_menu_item(mock_load, mock_save):
    mock_load.return_value = [make_menu_item("abc-123")]
    service = MenuItemService()
    update = MenuItemUpdate(
        restaurant_id="rest-2",
        name="Updated Pizza",
        description="Awesome updated pizza.",
        price=16.99,
        is_available=False,
        category="Greek"
    )
    result = service.update_menu_item("abc-123", update)
    assert result.name == "Updated Pizza"
    mock_save.assert_called_once()


@patch("app.services.MenuItemService.load_all")
def test_update_menu_item_not_found(mock_load):
    mock_load.return_value = []
    service = MenuItemService()
    with pytest.raises(HTTPException) as exc:
        service.update_menu_item(
            "does-not-exist",
            MenuItemUpdate(
                restaurant_id="x",
                name="x",
                description="x.",
                price=0.0,
                is_available=False,
                category="x"
            ),
        )
    assert exc.value.status_code == 404


@patch("app.services.MenuItemService.save_all")
@patch("app.services.MenuItemService.load_all")
def test_delete_menu_item(mock_load, mock_save):
    mock_load.return_value = [make_menu_item("abc-123")]
    service = MenuItemService()
    service.delete_menu_item("abc-123")
    mock_save.assert_called_once()


@patch("app.services.MenuItemService.load_all")
def test_delete_menu_item_not_found(mock_load):
    mock_load.return_value = []
    service = MenuItemService()
    with pytest.raises(HTTPException) as exc:
        service.delete_menu_item("does-not-exist")
    assert exc.value.status_code == 404