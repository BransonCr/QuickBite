from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from main import app

from app.schemas.Restaurant import Restaurant, RestaurantCreate, RestaurantUpdate
client = TestClient(app)

RESTAURANT_ID = "300"

SAMPLE_RESTAURANT = {
    "restaurant_id": RESTAURANT_ID,
    "owner_id": "owner123",
    "name": "Test Restaurant",
    "location": "123 Test St",
    "postal_code": "12345",
    "delivery_radius": 5.0,
    "is_active": True,
    "menu_list": []
}
    

def test_get_restaurants():
    with patch("app.routers.Restaurant.service") as mock_service:
        mock_service.get_all.return_value = [Restaurant(**SAMPLE_RESTAURANT)]
        response = client.get("/restaurants/")

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json() == [SAMPLE_RESTAURANT]

def test_create_restaurant():
    with patch("app.routers.Restaurant.service") as mock_service:
        mock_service.create_restaurant.return_value = Restaurant(**SAMPLE_RESTAURANT)
        response = client.post("/restaurants/", json=SAMPLE_RESTAURANT)

        assert response.status_code == 200
        assert response.json() == SAMPLE_RESTAURANT

def test_update_restaurant():
    with patch("app.routers.Restaurant.service") as mock_service:
        mock_service.update_restaurant.return_value = Restaurant(**SAMPLE_RESTAURANT)
        response = client.put(f"/restaurants/{RESTAURANT_ID}", json=SAMPLE_RESTAURANT)

        assert response.status_code == 200
        assert response.json() == SAMPLE_RESTAURANT

def test_delete_restaurant():
    with patch("app.routers.Restaurant.service") as mock_service:
        mock_service.delete_restaurant.return_value = None
        response = client.delete(f"/restaurants/{RESTAURANT_ID}")

        assert response.status_code == 200
        assert response.json() is None
def test_get_restaurant_not_found():
    with patch("app.routers.Restaurant.service") as mock_service:
        mock_service.get_restaurant.side_effect = HTTPException(status_code=404, detail="restaurant not found")
        response = client.get(f"/restaurants/{RESTAURANT_ID}")

        assert response.status_code == 404
        assert response.json() == {"detail": "restaurant not found"}
def test_update_restaurant_not_found():
    with patch("app.routers.Restaurant.service") as mock_service:
        mock_service.update_restaurant.side_effect = HTTPException(status_code=404, detail="restaurant not updated")
        response = client.put(f"/restaurants/{RESTAURANT_ID}", json=SAMPLE_RESTAURANT)

        assert response.status_code == 404
        assert response.json() == {"detail": "restaurant not updated"}
def test_delete_restaurant_not_found():
    with patch("app.routers.Restaurant.service") as mock_service:
        mock_service.delete_restaurant.side_effect = HTTPException(status_code=404, detail="restaurant not deleted")
        response = client.delete(f"/restaurants/{RESTAURANT_ID}")

        assert response.status_code == 404
        assert response.json() == {"detail": "restaurant not deleted"}