from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from main import app

from app.schemas.Restaurant import Restaurant, RestaurantCreate, RestaurantUpdate
client = TestClient(app)

RESTAURANT_ID = "300"

SAMPLE_RESTAURANT = Restaurant(
    restaurant_id=RESTAURANT_ID,
    owner_id="owner123",
    name="Test Restaurant",
    location="123 Test St",
    postal_code="12345",
    delivery_radius=5.0,
    is_active=True,
    menu_list=[],
    contact_info="123-456-7890",
    operating_hours="9AM-5PM"
)
SAMPLE_RESTAURANT_CREATE = RestaurantCreate(
    owner_id="owner123",
    name="Test Restaurant",
    location="123 Test St",
    postal_code="12345",
    contact_info="123-456-7890",
    operating_hours="9AM-5PM",
    delivery_radius=5.0
)

SAMPLE_RESTAURANT_UPDATE = RestaurantUpdate(
    operating_hours="10AM-10PM"
)   
    
def test_get_restaurants():
    with patch("app.routers.Restaurant.service") as mock_service:
        
        mock_service.get_all_restaurants.return_value = [SAMPLE_RESTAURANT]
        response = client.get("/restaurant/")

        assert response.status_code == 200
        assert response.json()[0]["restaurant_id"] == RESTAURANT_ID

def test_create_restaurant():
    with patch("app.routers.Restaurant.service") as mock_service:
        mock_service.create_restaurant.return_value = SAMPLE_RESTAURANT
        
       
        response = client.post("/restaurant/", json=SAMPLE_RESTAURANT_CREATE.model_dump(mode="json"))

        assert response.status_code == 200
        assert response.json() == SAMPLE_RESTAURANT.model_dump(mode="json")

def test_update_restaurant():
    with patch("app.routers.Restaurant.service") as mock_service:
        mock_service.update_restaurant.return_value = SAMPLE_RESTAURANT
        
       
        response = client.put(f"/restaurant/{RESTAURANT_ID}", json=SAMPLE_RESTAURANT_UPDATE.model_dump(mode="json"))

        assert response.status_code == 200
        assert response.json() == SAMPLE_RESTAURANT.model_dump(mode="json")

def test_delete_restaurant():
    with patch("app.routers.Restaurant.service") as mock_service:
        mock_service.delete_restaurant.return_value = None
        response = client.delete(f"/restaurant/{RESTAURANT_ID}")

        assert response.status_code == 200
        assert response.json() is None
        
def test_get_restaurant_not_found():

    with patch("app.routers.Restaurant.service") as mock_service:
        mock_service.get_restaurant.side_effect = HTTPException(status_code=404, detail="restaurant not found")
        response = client.get(f"/restaurant/{RESTAURANT_ID}")

        assert response.status_code == 404
        assert response.json() == {"detail": "restaurant not found"}

def test_update_restaurant_not_found():
    with patch("app.routers.Restaurant.service") as mock_service:
        mock_service.update_restaurant.side_effect = HTTPException(status_code=404, detail="restaurant not updated")
        
       
        response = client.put(f"/restaurant/{RESTAURANT_ID}", json=SAMPLE_RESTAURANT_UPDATE.model_dump(mode="json"))

        assert response.status_code == 404
        assert response.json() == {"detail": "restaurant not updated"}

def test_delete_restaurant_not_found():
    with patch("app.routers.Restaurant.service") as mock_service:
        mock_service.delete_restaurant.side_effect = HTTPException(status_code=404, detail="restaurant not deleted")
        response = client.delete(f"/restaurant/{RESTAURANT_ID}")

        assert response.status_code == 404
        assert response.json() == {"detail": "restaurant not deleted"}
