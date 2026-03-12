import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app
from app.schemas.Delivery import Delivery, DeliveryStatus

client = TestClient(app)

MOCK_DELIVERY = Delivery(
    delivery_id="test-id-123",
    order_id="order-1",
    driver_id="driver-1",
    status=DeliveryStatus.ASSIGNED,
    address="123 Main St",
    instructions="Leave at door",
)


@patch("app.services.DeliveryService.load_all", return_value=[MOCK_DELIVERY])
def test_get_all_deliveries(mock_load):
    response = client.get("/delivery/")
    assert response.status_code == 200
    assert len(response.json()) == 1


@patch("app.services.DeliveryService.get_by_id", return_value=MOCK_DELIVERY)
def test_get_delivery(mock_get):
    response = client.get("/delivery/test-id-123")
    assert response.status_code == 200
    assert response.json()["delivery_id"] == "test-id-123"


@patch("app.services.DeliveryService.get_by_id", return_value=None)
def test_get_delivery_not_found(mock_get):
    response = client.get("/delivery/nonexistent")
    assert response.status_code == 404


@patch("app.services.DeliveryService.load_all", return_value=[])
@patch("app.services.DeliveryService.save_all")
def test_create_delivery(mock_save, mock_load):
    payload = {
        "order_id": "order-1",
        "driver_id": "driver-1",
        "address": "123 Main St",
        "instructions": "Leave at door",
    }
    response = client.post("/delivery/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["order_id"] == "order-1"
    assert data["status"] == DeliveryStatus.ASSIGNED


@patch("app.services.DeliveryService.load_all", return_value=[MOCK_DELIVERY])
@patch("app.services.DeliveryService.save_all")
def test_update_delivery(mock_save, mock_load):
    payload = {
        "status": "IN_PROGRESS",
        "driver_id": "driver-2",
        "address": "456 New St",
        "instructions": "Ring bell",
        "completed_at": "",
    }
    response = client.put("/delivery/test-id-123", json=payload)
    assert response.status_code == 200


@patch("app.services.DeliveryService.load_all", return_value=[MOCK_DELIVERY])
@patch("app.services.DeliveryService.save_all")
def test_update_delivery_not_found(mock_save, mock_load):
    payload = {
        "status": "IN_PROGRESS",
        "driver_id": "driver-2",
        "address": "456 New St",
        "instructions": "Ring bell",
        "completed_at": "",
    }
    response = client.put("/delivery/nonexistent", json=payload)
    assert response.status_code == 404


@patch("app.models.DeliveryModel.load_all", return_value=[MOCK_DELIVERY])
@patch("app.models.DeliveryModel.save_all")
def test_delete_delivery(mock_save, mock_load):
    response = client.delete("/delivery/test-id-123")
    assert response.status_code == 200


@patch("app.models.DeliveryModel.load_all", return_value=[])
def test_delete_delivery_not_found(mock_load):
    response = client.delete("/delivery/nonexistent")
    assert response.status_code == 404
