from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from main import app
from app.schemas.Payment import Payment, PaymentCreate, PaymentUpdate,PaymentStatus

client = TestClient(app)


PAYMENT_ID = "400"

SAMPLE_PAYMENT = {
    "payment_id": PAYMENT_ID,
    "order_id": "order123",
    "amount": 100.0,
    "status": PaymentStatus.PENDING,
    "created_at": "2023-01-01 12:00:00"
}

def test_get_payments():
    with patch("app.routers.Payment.service") as mock_service:
        mock_service.get_payments.return_value = [Payment(**SAMPLE_PAYMENT)]
        response = client.get("/payments/")

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json() == [SAMPLE_PAYMENT]
def test_create_payment():
    with patch("app.routers.Payment.service") as mock_service:
        mock_service.create_payment.return_value = Payment(**SAMPLE_PAYMENT)
        response = client.post("/payments/", json=SAMPLE_PAYMENT)

        assert response.status_code == 200
        assert response.json() == SAMPLE_PAYMENT
def test_update_payment():
    with patch("app.routers.Payment.service") as mock_service:
        mock_service.update_payment.return_value = Payment(**SAMPLE_PAYMENT)
        response = client.put(f"/payments/{PAYMENT_ID}", json=SAMPLE_PAYMENT)

        assert response.status_code == 200
        assert response.json() == SAMPLE_PAYMENT

def test_delete_payment():
    with patch("app.routers.Payment.service") as mock_service:
        mock_service.delete_payment.return_value = None
        response = client.delete(f"/payments/{PAYMENT_ID}")

        assert response.status_code == 200
        assert response.json() is None

def test_get_payment_not_found():
    with patch("app.routers.Payment.service") as mock_service:
        mock_service.get_payment.side_effect = HTTPException(status_code=404, detail="Payment not found")
        response = client.get(f"/payments/{PAYMENT_ID}")

        assert response.status_code == 404
        assert response.json() == {"detail": "Payment not found"}
def test_update_payment_not_found():
    with patch("app.routers.Payment.service") as mock_service:
        mock_service.update_payment.side_effect = HTTPException(status_code=404, detail="Payment not found")
        response = client.put(f"/payments/{PAYMENT_ID}", json=SAMPLE_PAYMENT)

        assert response.status_code == 404
        assert response.json() == {"detail": "Payment not found"}
def test_delete_payment_not_found():
    with patch("app.routers.Payment.service") as mock_service:
        mock_service.delete_payment.side_effect = HTTPException(status_code=404, detail="Payment not found")
        response = client.delete(f"/payments/{PAYMENT_ID}")

        assert response.status_code == 404
        assert response.json() == {"detail": "Payment not found"}