from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.schemas.Review import Review, ReviewCreate, ReviewUpdate
from main import app

client = TestClient(app)

REVIEW_ID = "abc-123"

SAMPLE_REVIEW = Review(
    review_id=REVIEW_ID,
    customer_id="cust-1",
    restaurant_id="rest-1",
    order_id="order-1",
    rating=5,
    text="Great food!",
    created_at="2026-03-08T00:00:00+00:00",
)


def test_get_reviews():
    with patch("app.routers.Review.service") as mock_service:
        mock_service.get_review.return_value = [SAMPLE_REVIEW]
        response = client.get("/review/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["review_id"] == REVIEW_ID


def test_get_review_by_id():
    with patch("app.routers.Review.service") as mock_service:
        mock_service.get_review_by_id.return_value = SAMPLE_REVIEW
        response = client.get(f"/review/{REVIEW_ID}")

    assert response.status_code == 200
    assert response.json()["review_id"] == REVIEW_ID


def test_get_review_by_id_not_found():
    with patch("app.routers.Review.service") as mock_service:
        mock_service.get_review_by_id.side_effect = HTTPException(status_code=404, detail="Review not found")
        response = client.get("/review/nonexistent")

    assert response.status_code == 404


def test_create_review():
    payload = {
        "customer_id": "cust-1",
        "restaurant_id": "rest-1",
        "order_id": "order-1",
        "rating": 5,
        "text": "Great food!",
    }
    with patch("app.routers.Review.service") as mock_service:
        mock_service.create_review.return_value = SAMPLE_REVIEW
        response = client.post("/review/", json=payload)

    assert response.status_code == 200
    assert response.json()["review_id"] == REVIEW_ID
    assert response.json()["rating"] == 5


def test_update_review():
    updated = SAMPLE_REVIEW.model_copy(update={"rating": 3, "text": "Okay food."})
    with patch("app.routers.Review.service") as mock_service:
        mock_service.update_review.return_value = updated
        response = client.put(f"/review/{REVIEW_ID}", json={"rating": 3, "text": "Okay food."})

    assert response.status_code == 200
    assert response.json()["rating"] == 3
    assert response.json()["text"] == "Okay food."


def test_update_review_not_found():
    with patch("app.routers.Review.service") as mock_service:
        mock_service.update_review.side_effect = HTTPException(status_code=404, detail="Review not found")
        response = client.put("/review/nonexistent", json={"rating": 3, "text": "Okay food."})

    assert response.status_code == 404


def test_delete_review():
    with patch("app.routers.Review.service") as mock_service:
        mock_service.delete_review.return_value = None
        response = client.delete(f"/review/{REVIEW_ID}")

    assert response.status_code == 200


def test_delete_review_not_found():
    with patch("app.routers.Review.service") as mock_service:
        mock_service.delete_review.side_effect = HTTPException(status_code=404, detail="Review not found")
        response = client.delete("/review/nonexistent")

    assert response.status_code == 404
