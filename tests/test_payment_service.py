from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from app.services.Payment_service import PaymentService
from main import app
from app.schemas.Payment import Payment, PaymentCreate, PaymentUpdate, PaymentStatus

client = TestClient(app)

PAYMENT_ID = "400"
PAYMENT_ID2 = "401"


SAMPLE_PAYMENT = Payment(
    payment_id=PAYMENT_ID,
    order_id="order123",
    amount=100.0,
    status=PaymentStatus.PENDING,
    created_at="2023-01-01T12:00:00",
    confirmation_number="conf-5678",
    card_number="1234567812345678",
    expiration_date="12/28",
    cvv="123"
)

SAMPLE_PAYMENT2 = Payment(
    payment_id=PAYMENT_ID2,
    order_id="order456",
    amount=50.0,
    status=PaymentStatus.SUCCESS,
    created_at="2023-01-02T12:00:00",
    confirmation_number="conf-5679",
    card_number="8765432187654321",
    expiration_date="11/27",
    cvv="321"
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
    with patch("app.routers.Payment.service") as mock_service, patch("app.services.Payment_service.confirm_order") as mock_confirm, patch("app.services.Payment_service.save_all") as mock_save:
        mock_service.update_payment.return_value = SAMPLE_PAYMENT
        mock_confirm.return_value = None
        mock_save.return_value = None
       
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

def test_update_payment_invalid_transition():
    with patch("app.routers.Payment.service") as mock_service:
        mock_service.update_payment.side_effect = HTTPException(status_code=400, detail="Invalid status transition from PENDING to PENDING")
       
        response = client.put(f"/payment/{PAYMENT_ID}", json={"status": "PENDING"})

        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid status transition from PENDING to PENDING"}

def test_update_payment_valid_transition():
    with patch("app.routers.Payment.service") as mock_service:
        mock_service.update_payment.return_value = SAMPLE_PAYMENT
       
        response = client.put(f"/payment/{PAYMENT_ID}", json={"status": "FAILED"})

        assert response.status_code == 200
        assert response.json() == SAMPLE_PAYMENT.model_dump(mode="json")

        SAMPLE_PAYMENT.status = PaymentStatus.FAILED
        mock_service.update_payment.return_value = SAMPLE_PAYMENT

        response = client.put(f"/payment/{PAYMENT_ID}", json={"status": "PENDING"})

        assert response.status_code == 200
        assert response.json() == SAMPLE_PAYMENT.model_dump(mode="json")

def test_delete_payment_status_success():
    with patch("app.services.Payment_service.load_all") as mock_load:
        mock_load.return_value = [SAMPLE_PAYMENT2]

        response = client.delete(f"/payment/{PAYMENT_ID2}")

        assert response.status_code == 400
        assert response.json() == {"detail": "Cannot delete a successful payment"}

def test_service_generates_confirmation_on_success():
    service = PaymentService()
    
    pending = SAMPLE_PAYMENT.model_copy()
    pending.status = PaymentStatus.PENDING
    pending.confirmation_number = None

    with patch("app.services.Payment_service.load_all", return_value=[pending]), patch("app.services.Payment_service.confirm_order", return_value=None), patch("app.services.Payment_service.save_all") as mock_save:
        mock_save.return_value = None
        updated = service.update_payment(pending.payment_id, PaymentUpdate(status="SUCCESS"))
        
        assert updated.status == PaymentStatus.SUCCESS
        assert updated.confirmation_number is not None
        assert len(updated.confirmation_number) > 0

def test_create_payment_invalid_card():
    with patch("app.services.Payment_service.load_all", return_value=[]), patch("app.services.Payment_service.save_all"):
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
            service.create_payment(expired_card_payment) == HTTPException(status_code=400, detail="Invalid expiration date")

        assert execution_info.value.status_code == 400
        assert execution_info.value.detail == "Invalid expiration date"

        empty_cvv_payment = PaymentCreate(
            order_id="order123",
            amount=100.0,
            card_number="1234567812345678",
            expiration_date="12/2028",
            cvv=""
        )

        with pytest.raises(HTTPException) as execution_info:
            service.create_payment(empty_cvv_payment) == HTTPException(status_code=400, detail="Invalid CVV")
        
        assert execution_info.value.status_code == 400
        assert execution_info.value.detail == "Invalid CVV"