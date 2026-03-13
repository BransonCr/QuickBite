from unittest.mock import patch
from fastapi.testclient import TestClient
from app.schemas.MenuItem import MenuItem
from main import app
from app.schemas.Restaurant import Restaurant
import pytest

RESTAURANT_ID = "300"
ITEM_ID = "item-123"

SAMPLE_MENUITEM = MenuItem(
    item_id=ITEM_ID,
    restaurant_id="rest-1",
    name="Pepperoni Pizza",
    description="Delicious pepperoni pizza with a crispy crust.",
    price=12.99,
    is_available=True,
    category="Italian"
)

SAMPLE_MENUITEM_2 = MenuItem(
    item_id="item-456",
    restaurant_id="301",
    name="Cheeseburger",
    description="Juicy cheeseburger with all the fixings.",
    price=9.99,
    is_available=True,
    category="American"
)

SAMPLE_RESTAURANT = Restaurant(
    restaurant_id=RESTAURANT_ID,
    owner_id="owner123",
    name="Test Restaurant",
    location="123 Test St",
    postal_code="12345",
    delivery_radius=5.0,
    is_active=True,
    menu_list=[SAMPLE_MENUITEM]
)

SAMPLE_RESTAURANT_2 = Restaurant(
    restaurant_id="301",
    owner_id="owner456",
    name="Burger Restaurant",
    location="456 Another St",
    postal_code="67890",
    delivery_radius=10.0,
    is_active=True,
    menu_list=[SAMPLE_MENUITEM_2]
)

client = TestClient(app)

@patch("app.routers.Restaurant.service")
def test_search_and_filter_by_name(mock_service):
    mock_service.get_all_restaurants.return_value = [SAMPLE_RESTAURANT]
    response = client.get("/search/Test")
    assert response.json()[0]["restaurant_id"] == RESTAURANT_ID

@patch("app.routers.Restaurant.service")
def test_search_and_filter_no_match(mock_service):
    mock_service.get_all_restaurants.return_value = [SAMPLE_RESTAURANT]
    response = client.get("/search/NonExistent")
    assert response.json() == []

@patch("app.routers.Restaurant.service")
def test_search_and_filter_by_menu_item(mock_service):
    mock_service.get_all_restaurants.return_value = [SAMPLE_RESTAURANT]
    response = client.get("/search/Pepperoni")
    assert response.json()[0]["restaurant_id"] == RESTAURANT_ID

@patch("app.routers.Restaurant.service")
def test_search_and_filter_case_insensitive(mock_service):
    mock_service.get_all_restaurants.return_value = [SAMPLE_RESTAURANT]
    response = client.get("/search/pepperoni")
    assert response.json()[0]["restaurant_id"] == RESTAURANT_ID

@patch("app.routers.Restaurant.service")
def test_search_and_filter_return_only_once(mock_service):
    mock_service.get_all_restaurants.return_value = [SAMPLE_RESTAURANT_2]
    response = client.get("/search/Burger")
    assert len(response.json()) == 1
    assert response.json()[0]["restaurant_id"] == "301"