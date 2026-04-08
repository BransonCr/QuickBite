from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.schemas.Notification import Notification, NotificationCreate, NotificationUpdate
from app.services.NotificationService import NotificationService


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
    result = service.order_notification("user-1", "order-123")
    assert result.message == "Your order order-123 has been placed successfully!"
    mock_save.assert_called_once()

@patch("app.services.NotificationService.save_all")
@patch("app.services.NotificationService.load_all")
def test_order_pickup_notification(mock_load, mock_save):
    mock_load.return_value = [make_notification("abc-123")]
    service = NotificationService()
    result = service.order_pickup_notification("user-1", "order-123")
    assert result.message == "Your order order-123 is out for pickup!"
    mock_save.assert_called_once()


@patch("app.services.NotificationService.save_all")
@patch("app.services.NotificationService.load_all")
def test_order_delivery_notification(mock_load, mock_save):
    mock_load.return_value = []
    service = NotificationService()
    result = service.order_delivery_notification("user-1", "order-123")
    assert result.message == "Your order order-123 has been delivered!"
    mock_save.assert_called_once()

@patch("app.services.NotificationService.save_all")
@patch("app.services.NotificationService.load_all")
def test_order_status_customer_notification(mock_load, mock_save):
    mock_load.return_value = []
    service = NotificationService()
    result = service.order_status_customer_notification("user-1", "order-123", "in_transit")
    assert result.message == "Your order order-123 status has been updated to in_transit!"
    mock_save.assert_called_once()

@patch("app.services.NotificationService.save_all")
@patch("app.services.NotificationService.load_all")
def test_order_status_customer_notification_didnt_receive(mock_load, mock_save):
    mock_load.return_value = []
    service = NotificationService()
    result = service.order_status_customer_notification("user-1", "order-123", "didn't receive")
    assert result.message == "Your order order-123 status has been updated to didn't receive!"
    mock_save.assert_called_once()

@patch("app.services.NotificationService.save_all")
@patch("app.services.NotificationService.load_all")
def test_order_status_restaurant_notification(mock_load, mock_save):
    mock_load.return_value = []
    service = NotificationService()
    result = service.order_status_restaurant_notification("restaurant-1", "order-123", "cancelled")
    assert result.message == "Order order-123 status has been updated to cancelled!"
    mock_save.assert_called_once()

@patch("app.services.NotificationService.save_all")
@patch("app.services.NotificationService.load_all")
def test_payment_status_message(mock_load, mock_save):
    mock_load.return_value = []
    service = NotificationService()
    result = service.payment_status_customer_notification("user-1","paym-123", "order-123", "FAILED")
    assert result.message == "Your payment paym-123 for order order-123 has failed. Please try again."

    result = service.payment_status_customer_notification("user-1","paym-123", "order-123", "SUCCESS")
    assert result.message == "Your payment paym-123 for order order-123 was successful! Thank you for your purchase."

    result = service.payment_status_customer_notification("user-1","paym-123", "order-123", "PENDING")
    assert result.message == "Your payment paym-123 for order order-123 is pending. We will notify you once it is processed."

    result = service.payment_status_customer_notification("user-1","paym-123", "order-123", "DELIVERED")
    assert result.message == "Your payment paym-123 for order order-123 has an unknown payment status: DELIVERED."

    assert mock_save.call_count == 4


@patch("app.services.NotificationService.save_all")
@patch("app.services.NotificationService.load_all")
def test_get_user_notifications(mock_load, mock_save):
    mock_load.return_value = [
        make_notification("abc-123"),
        Notification(
            notification_id="def-456",
            user_id="user-2",
            order_id="order-2",
            message="Your delivery has arrived!",
            type="delivery_update",
            is_read=False,
            created_at="2026-03-08 12:00:00"
        )
    ]
    service = NotificationService()
    result = service.get_user_notifications("user-1")
    assert len(result) == 1
    assert result[0].user_id == "user-1"
