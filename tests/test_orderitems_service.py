from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.schemas.OrderItem import OrderItem, OrderItemCreate, OrderItemUpdate
from app.services.OrderItemService import OrderItemService


def make_order_item(order_item_id="item-123"):
    return OrderItem(
        order_item_id=order_item_id,
        order_id="ord-123",
        item_id="prod-456",
        quantity=2,
        price_at_time=29.99,
    )


def make_order_item_create():
    return OrderItemCreate(
        order_id="ord-123",
        item_id="prod-456",
        quantity=2,
        price_at_time=29.99,
    )


@patch("app.services.OrderItemService.save_all")
@patch("app.services.OrderItemService.load_all")
def test_get_order_items(mock_load, mock_save):
    mock_load.return_value = [make_order_item()]
    service = OrderItemService()
    result = service.get_order_items()
    assert len(result) == 1
    assert result[0].order_item_id == "item-123"


@patch("app.services.OrderItemService.save_all")
@patch("app.services.OrderItemService.load_all")
def test_get_order_item_found(mock_load, mock_save):
    mock_load.return_value = [make_order_item("item-123")]
    service = OrderItemService()
    result = service.get_order_item("item-123")
    assert result.order_item_id == "item-123"


@patch("app.services.OrderItemService.save_all")
@patch("app.services.OrderItemService.load_all")
def test_get_order_item_not_found(mock_load, mock_save):
    mock_load.return_value = []
    service = OrderItemService()
    with pytest.raises(HTTPException) as exc:
        service.get_order_item("does-not-exist")
    assert exc.value.status_code == 404


@patch("app.services.OrderItemService.save_all")
@patch("app.services.OrderItemService.load_all")
def test_create_order_item(mock_load, mock_save):
    mock_load.return_value = []
    service = OrderItemService()
    result = service.create_order_item(make_order_item_create())
    assert result.order_id == "ord-123"
    assert result.order_item_id is not None
    mock_save.assert_called_once()


@patch("app.services.OrderItemService.save_all")
@patch("app.services.OrderItemService.load_all")
def test_update_order_item(mock_load, mock_save):
    mock_load.return_value = [make_order_item("item-123")]
    service = OrderItemService()
    update = OrderItemUpdate(
        quantity=5,
        price_at_time=24.99,
    )
    result = service.update_order_item("item-123", update)
    assert result.quantity == 5
    assert result.price_at_time == 24.99
    mock_save.assert_called_once()


@patch("app.services.OrderItemService.save_all")
@patch("app.services.OrderItemService.load_all")
def test_update_order_item_not_found(mock_load, mock_save):
    mock_load.return_value = []
    service = OrderItemService()
    with pytest.raises(HTTPException) as exc:
        service.update_order_item(
            "does-not-exist",
            OrderItemUpdate(
                quantity=1,
                price_at_time=0.0,
            ),
        )
    assert exc.value.status_code == 404


@patch("app.services.OrderItemService.save_all")
@patch("app.services.OrderItemService.load_all")
def test_delete_order_item(mock_load, mock_save):
    mock_load.return_value = [make_order_item("item-123")]
    service = OrderItemService()
    service.delete_order_item("item-123")
    mock_save.assert_called_once()


@patch("app.services.OrderItemService.save_all")
@patch("app.services.OrderItemService.load_all")
def test_delete_order_item_not_found(mock_load, mock_save):
    mock_load.return_value = []
    service = OrderItemService()
    with pytest.raises(HTTPException) as exc:
        service.delete_order_item("does-not-exist")
    assert exc.value.status_code == 404