from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.schemas.Restaurant import Restaurant
from app.schemas.Notification import Notification, NotificationCreate, NotificationUpdate
from app.services.NotificationService import NotificationService
from app.schemas.User import User


def make_notification(notification_id="abc-123"):
    return Notification(
        notification_id=notification_id,
        user_id="user-1",
        order_id="order-1",
        message="Your order has been shipped!",
        type="order_update",
        is_read=False,
        created_at="2026-03-08 12:00:00"
    )


def make_notification_create():
    return NotificationCreate(
        user_id="user-1",
        order_id="order-1",
        message="Your order has been shipped!",
        type="order_update",
        is_read=False
    )


@patch("app.services.NotificationService.save_all")
@patch("app.services.NotificationService.load_all")
def test_get_notifications(mock_load, mock_save):
    mock_load.return_value = [make_notification()]
    service = NotificationService()
    result = service.get_notifications()
    assert len(result) == 1
    assert result[0].type == "order_update"


@patch("app.services.NotificationService.save_all")
@patch("app.services.NotificationService.load_all")
def test_get_notification_found(mock_load, mock_save):
    mock_load.return_value = [make_notification("abc-123")]
    service = NotificationService()
    result = service.get_notification("abc-123")
    assert result.notification_id == "abc-123"


@patch("app.services.NotificationService.save_all")
@patch("app.services.NotificationService.load_all")
def test_get_notification_not_found(mock_load, mock_save):
    mock_load.return_value = []
    service = NotificationService()
    with pytest.raises(HTTPException) as exc:
        service.get_notification("does-not-exist")
    assert exc.value.status_code == 404


@patch("app.services.NotificationService.save_all")
@patch("app.services.NotificationService.load_all")
def test_create_notification(mock_load, mock_save):
    mock_load.return_value = []
    service = NotificationService()
    result = service.create_notification(make_notification_create())
    assert result.message == "Your order has been shipped!"
    assert result.notification_id is not None
    mock_save.assert_called_once()


@patch("app.services.NotificationService.save_all")
@patch("app.services.NotificationService.load_all")
def test_update_notification(mock_load, mock_save):
    mock_load.return_value = [make_notification("abc-123")]
    service = NotificationService()
    update = NotificationUpdate(
        notification_id="updated-id",
        user_id="user-2",
        order_id="order-2",
        message="Your delivery has arrived!",
        type="delivery_update",
        is_read=True
    )
    result = service.update_notification("abc-123", update)
    assert result.message == "Your delivery has arrived!"
    mock_save.assert_called_once()


@patch("app.services.NotificationService.save_all")
@patch("app.services.NotificationService.load_all")
def test_update_notification_not_found(mock_load, mock_save):
    mock_load.return_value = []
    service = NotificationService()
    with pytest.raises(HTTPException) as exc:
        service.update_notification(
            "does-not-exist",
            NotificationUpdate(
                notification_id="x",
                user_id="x",
                order_id="x",
                message="x",
                type="x",
                is_read=True
            ),
        )
    assert exc.value.status_code == 404


@patch("app.services.NotificationService.save_all")
@patch("app.services.NotificationService.load_all")
def test_delete_notification(mock_load, mock_save):
    mock_load.return_value = [make_notification("abc-123")]
    service = NotificationService()
    service.delete_notification("abc-123")
    mock_save.assert_called_once()


@patch("app.services.NotificationService.save_all")
@patch("app.services.NotificationService.load_all")
def test_delete_notification_not_found(mock_load, mock_save):
    mock_load.return_value = []
    service = NotificationService()
    with pytest.raises(HTTPException) as exc:
        service.delete_notification("does-not-exist")
    assert exc.value.status_code == 404

@patch("app.services.NotificationService.save_all")
@patch("app.services.NotificationService.load_all")
def test_get_badge_status(mock_load, mock_save):
    mock_load.return_value = [make_notification("abc-123")]
    service = NotificationService()
    result = service.get_badge_status("user-1")
    assert result == True    



@patch("app.services.NotificationService.save_all")
@patch("app.services.NotificationService.load_all")
def test_order_notification(mock_load, mock_save):
    mock_load.return_value = [make_notification("abc-123")]
    service = NotificationService()
    user = User(
        user_id="user-1",
        username="testuser",
        email="test@example.com",
        password_hash="hashedpassword",
        phone="1234567890",
        role="CUSTOMER",
        location="123 Main St",
        postal_code="12345",
        created_at="2026-03-08 12:00:00"
    )
    result = service.order_notification(user, "order-123")
    assert result.message == "Your order order-123 has been placed successfully!"
    mock_save.assert_called_once()

@patch("app.services.NotificationService.save_all")
@patch("app.services.NotificationService.load_all")
def test_order_pickup_notification(mock_load, mock_save):
    mock_load.return_value = [make_notification("abc-123")]
    service = NotificationService()
    user = User(
        user_id="user-1",
        username="testuser",
        email="test@example.com",
        password_hash="hashedpassword",
        phone="1234567890",
        role="CUSTOMER",
        location="123 Main St",
        postal_code="12345",
        created_at="2026-03-08 12:00:00"
    )
    result = service.order_pickup_notification(user, "order-123")
    assert result.message == "Your order order-123 is out for pickup!"
    mock_save.assert_called_once()


@patch("app.services.NotificationService.save_all")
@patch("app.services.NotificationService.load_all")
def test_order_delivery_notification(mock_load, mock_save):
    mock_load.return_value = []
    service = NotificationService()
    user = User(
        user_id="user-1",
        username="testuser",
        email="test@example.com",
        password_hash="hashedpassword",
        phone="1234567890",
        role="CUSTOMER",
        location="123 Main St",
        postal_code="12345",
        created_at="2026-03-08 12:00:00"
    )
    result = service.order_delivery_notification(user, "order-123")
    assert result.message == "Your order order-123 has been delivered!"
    mock_save.assert_called_once()

@patch("app.services.NotificationService.save_all")
@patch("app.services.NotificationService.load_all")
def test_order_status_customer_notification(mock_load, mock_save):
    mock_load.return_value = []
    service = NotificationService()
    user = User(
        user_id="user-1",
        username="testuser",
        email="test@example.com",
        password_hash="hashedpassword",
        phone="1234567890",
        role="CUSTOMER",
        location="123 Main St",
        postal_code="12345",
        created_at="2026-03-08 12:00:00"
    )
    result = service.order_status_customer_notification(user, "order-123", "in_transit")
    assert result.message == "Your order order-123 status has been updated to in_transit!"
    mock_save.assert_called_once()

@patch("app.services.NotificationService.save_all")
@patch("app.services.NotificationService.load_all")
def test_order_status_restaurant_notification(mock_load, mock_save):
    mock_load.return_value = []
    service = NotificationService()
    user = User(
        user_id="user-1",
        username="testuser",
        email="test@example.com",
        password_hash="hashedpassword",
        phone="1234567890",
        role="CUSTOMER",
        location="123 Main St",
        postal_code="12345",
        created_at="2026-03-08 12:00:00"
    )
    result =service.order_status_customer_notification(user, "order-123", "didn't receive")
    assert result.message == "Your order order-123 status has been updated to didn't receive!"
    mock_save.assert_called_once()

@patch("app.services.NotificationService.save_all")
@patch("app.services.NotificationService.load_all")
def test_order_status_restaurant_notification(mock_load, mock_save):
    mock_load.return_value = []
    service = NotificationService()
    user = Restaurant(
        restaurant_id="restaurant-1",
        name="Test Restaurant",
        location="123 Main St",
        postal_code="12345",
        contact_info="123-456-7890",    
        operating_hours="9am - 9pm",
        delivery_radius=5.0,
        is_active=True,
        owner_id="owner-1",
        menu_list=[]
    )
    result =service.order_status_restaurant_notification(user, "order-123", "cancelled")
    assert result.message == "Order order-123 status has been updated to cancelled!"
    mock_save.assert_called_once()
