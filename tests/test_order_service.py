from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.schemas.Order import Order, OrderCreate, OrderUpdate, OrderStatus
from app.services.OrderService import OrderService


def make_order(order_id="ord-123"):
    return Order(
        order_id=order_id,
        customer_id="cust-123",
        restaurant_id="rest-456",
        subtotal=40.00,
        tax=2.00,
        delivery_fee=3.00,
        tip=5.00,
        total=50.00,
        status=OrderStatus.PENDING,
        created_at="2026-03-09T10:00:00",
        updated_at="2026-03-09T10:00:00"
    )


def make_order_create():
    return OrderCreate(
        customer_id="cust-123",
        restaurant_id="rest-456",
        subtotal=40.00,
        tax=2.00,
        delivery_fee=3.00,
        tip=5.00,
        total=50.00,
        status=OrderStatus.PENDING
    )



@patch("app.services.OrderService.load_all")
def test_get_orders(mock_load):
    mock_load.return_value = [make_order()]
    service = OrderService()
    result = service.get_orders()
    assert len(result) == 1
    assert result[0].restaurant_id == "rest-456"

@patch("app.services.OrderService.load_all")
def test_get_order_found(mock_load):
    mock_load.return_value = [make_order("ord-123")]
    service = OrderService()
    result = service.get_order("ord-123")
    assert result.order_id == "ord-123"

@patch("app.services.OrderService.load_all")
def test_get_order_not_found(mock_load):
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
    assert result.customer_id == "cust-123"
    assert result.order_id is not None
    mock_save.assert_called_once()

@patch("app.services.OrderService.save_all")
@patch("app.services.OrderService.load_all")
def test_update_order(mock_load, mock_save):
    mock_load.return_value = [make_order("ord-123")]
    service = OrderService()
    update = OrderUpdate(
        status=OrderStatus.OUT_FOR_DELIVERY,
        tip=10.00,
        total=55.00
    )
    result = service.update_order("ord-123", update)
    assert result.status == OrderStatus.OUT_FOR_DELIVERY
    assert result.tip == 10.00
    mock_save.assert_called_once()

@patch("app.services.OrderService.load_all")
def test_update_order_not_found(mock_load):
    mock_load.return_value = []
    service = OrderService()
    with pytest.raises(HTTPException) as exc:
        service.update_order(
            "does-not-exist",
            OrderUpdate(
                status=OrderStatus.CANCELLED
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

@patch("app.services.OrderService.load_all")
def test_delete_order_not_found(mock_load):
    mock_load.return_value = []
    service = OrderService()
    with pytest.raises(HTTPException) as exc:
        service.delete_order("does-not-exist")
    assert exc.value.status_code == 404

@patch("app.services.OrderService.save_all")
@patch("app.services.OrderService.load_all")
def test_get_postal_code(mock_load, mock_save):
    mock_load.return_value = [make_order("ord-123")]
    service = OrderService()
    result = service.get_postal_code("user-1")
    assert result is None

@patch("app.services.OrderService.save_all")
@patch("app.services.OrderService.load_all")
def test_get_location(mock_load, mock_save):
    mock_load.return_value = [make_order("ord-123")]
    service = OrderService()
    result = service.get_location("user-1")
    assert result is None


@patch("app.services.OrderService.save_all")
@patch("app.services.OrderService.load_all")
def test_get_restaurant_location(mock_load, mock_save):
    mock_load.return_value = [make_order("ord-123")]
    service = OrderService()
    result = service.get_restaurant_location("rest-456")
    assert result is None

@patch("app.services.OrderService.save_all")
@patch("app.services.OrderService.load_all")
def measure_distance(mock_load, mock_save):
    service = OrderService()
    result = service.measure_distance("loc1", "loc2")
    assert result == 0
