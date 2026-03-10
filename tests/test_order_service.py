from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.schemas.Order import Order, OrderCreate, OrderUpdate
from app.services.OrderService import OrderService


def make_order(order_id="ord-123"):
    return Order(
        order_id=order_id,
        user_id="abc-123",
        item_description="Test Product",
        total_price=49.99,
        status="PENDING",
        created_at="2026-03-09",
    )


def make_order_create():
    return OrderCreate(
        user_id="abc-123",
        item_description="Test Product",
        total_price=49.99,
        status="PENDING",
        created_at="2026-03-09",
    )


@patch("app.services.OrderService.save_all")
@patch("app.services.OrderService.load_all")
def test_get_orders(mock_load, mock_save):
    mock_load.return_value = [make_order()]
    service = OrderService()
    result = service.get_orders()
    assert len(result) == 1
    assert result[0].item_description == "Test Product"


@patch("app.services.OrderService.save_all")
@patch("app.services.OrderService.load_all")
def test_get_order_found(mock_load, mock_save):
    mock_load.return_value = [make_order("ord-123")]
    service = OrderService()
    result = service.get_order("ord-123")
    assert result.order_id == "ord-123"


@patch("app.services.OrderService.save_all")
@patch("app.services.OrderService.load_all")
def test_get_order_not_found(mock_load, mock_save):
    mock_load.return_value = []
    service = OrderService()
    with pytest.raises(HTTPException) as exc:
        service.get_order("does-not-exist")
    assert exc.value.status_code == 404


@patch("app.services.OrderService.save_all")
@patch("app.services.OrderService.load_all")
def test_create_order(mock_load, mock_save):
    mock_load.return_value = []
    service = OrderService()
    result = service.create_order(make_order_create())
    assert result.item_description == "Test Product"
    assert result.order_id is not None
    mock_save.assert_called_once()


@patch("app.services.OrderService.save_all")
@patch("app.services.OrderService.load_all")
def test_update_order(mock_load, mock_save):
    mock_load.return_value = [make_order("ord-123")]
    service = OrderService()
    update = OrderUpdate(
        user_id="abc-123",
        item_description="Updated Product",
        total_price=59.99,
        status="SHIPPED",
    )
    result = service.update_order("ord-123", update)
    assert result.item_description == "Updated Product"
    assert result.status == "SHIPPED"
    mock_save.assert_called_once()


@patch("app.services.OrderService.save_all")
@patch("app.services.OrderService.load_all")
def test_update_order_not_found(mock_load, mock_save):
    mock_load.return_value = []
    service = OrderService()
    with pytest.raises(HTTPException) as exc:
        service.update_order(
            "does-not-exist",
            OrderUpdate(
                user_id="x",
                item_description="x",
                total_price=0.0,
                status="x",
            ),
        )
    assert exc.value.status_code == 404


@patch("app.services.OrderService.save_all")
@patch("app.services.OrderService.load_all")
def test_delete_order(mock_load, mock_save):
    mock_load.return_value = [make_order("ord-123")]
    service = OrderService()
    service.delete_order("ord-123")
    mock_save.assert_called_once()


@patch("app.services.OrderService.save_all")
@patch("app.services.OrderService.load_all")
def test_delete_order_not_found(mock_load, mock_save):
    mock_load.return_value = []
    service = OrderService()
    with pytest.raises(HTTPException) as exc:
        service.delete_order("does-not-exist")
    assert exc.value.status_code == 404