from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from app.services.Payment_service import PaymentService
from main import app
from app.schemas.Payment import Payment, PaymentCreate, PaymentUpdate, PaymentStatus

client = TestClient(app)

PAYMENT_ID = "400"


SAMPLE_PAYMENT = Payment(
    payment_id=PAYMENT_ID,
    order_id="order123",
    amount=100.0,
    status=PaymentStatus.PENDING,
    created_at="2023-01-01 12:00:00",
    confirmation_number="conf-5678",
    card_number="1234567812345678",
    expiration_date="12/2028",
    cvv="123"
)

def test_get_payments():
    with patch("app.routers.Payment.service") as mock_service:
      
        mock_service.get_all_payments.return_value = [SAMPLE_PAYMENT]
        
        response = client.get("/payment/")

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["payment_id"] == PAYMENT_ID

def test_create_payment():
    with patch("app.routers.Payment.service") as mock_service:
        mock_service.create_payment.return_value = SAMPLE_PAYMENT
        
       
        response = client.post("/payment/", json=SAMPLE_PAYMENT.model_dump(mode="json"))

        assert response.status_code == 200
        assert response.json() == SAMPLE_PAYMENT.model_dump(mode="json")

def test_update_payment():
    with patch("app.routers.Payment.service") as mock_service:
        mock_service.update_payment.return_value = SAMPLE_PAYMENT
        
       
        response = client.put(f"/payment/{PAYMENT_ID}", json=SAMPLE_PAYMENT.model_dump(mode="json"))

        assert response.status_code == 200
        assert response.json() == SAMPLE_PAYMENT.model_dump(mode="json")

def test_delete_payment():
    with patch("app.routers.Payment.service") as mock_service:
        mock_service.delete_payment.return_value = None
        response = client.delete(f"/payment/{PAYMENT_ID}")

        assert response.status_code == 200
        assert response.json() is None

def test_get_payment_not_found():
    with patch("app.routers.Payment.service") as mock_service:
        mock_service.get_payment.side_effect = HTTPException(status_code=404, detail="Payment not found")
        response = client.get(f"/payment/{PAYMENT_ID}")

        assert response.status_code == 404
        assert response.json() == {"detail": "Payment not found"}

def test_update_payment_not_found():
    with patch("app.routers.Payment.service") as mock_service:
        mock_service.update_payment.side_effect = HTTPException(status_code=404, detail="Payment not found")
       
        response = client.put(f"/payment/{PAYMENT_ID}", json=SAMPLE_PAYMENT.model_dump(mode="json"))

        assert response.status_code == 404
        assert response.json() == {"detail": "Payment not found"}

def test_delete_payment_not_found():
    with patch("app.routers.Payment.service") as mock_service:
        mock_service.delete_payment.side_effect = HTTPException(status_code=404, detail="Payment not found")
        
       
        response = client.delete(f"/payment/{PAYMENT_ID}")

        assert response.status_code == 404
        assert response.json() == {"detail": "Payment not found"}

def test_create_payment_invalid_card():
    service = PaymentService()

    invalid_card_payment = PaymentCreate(
        order_id="order123",
        amount=100.0,
        card_number="invalid_card",
        expiration_date="12/2028",
        cvv="123"
    )
    with pytest.raises(HTTPException) as execution_info:
        service.create_payment(invalid_card_payment) == HTTPException(status_code=400, detail="Invalid card number")

    assert execution_info.value.status_code == 400
    assert execution_info.value.detail == "Invalid card number"

    expired_card_payment = PaymentCreate(
        order_id="order123",
        amount=100.0,
        card_number="1234567812345678",
        expiration_date="10/2020",
        cvv="123"
    )

    with pytest.raises(HTTPException) as execution_info:
        service.create_payment(expired_card_payment) == HTTPException(status_code=400, detail="Card has expired")

    assert execution_info.value.status_code == 400
    assert execution_info.value.detail == "Card has expired"

    empty_cvv_payment = PaymentCreate(
        order_id="order123",
        amount=100.0,
        card_number="1234567812345678",
        expiration_date="12/2028",
        cvv=""
    )

    with pytest.raises(HTTPException) as execution_info:
        service.create_payment(empty_cvv_payment) == HTTPException(status_code=400, detail="CVV is required")
    
    assert execution_info.value.status_code == 400
    assert execution_info.value.detail == "CVV is required"