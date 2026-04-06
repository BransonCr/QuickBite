from unittest.mock import patch
from fastapi.testclient import TestClient
from app.schemas.MenuItem import MenuItem
from main import app
from app.schemas.Restaurant import Restaurant

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
    contact_info="test@restaurant.com",
    operating_hours="9am-9pm",
    delivery_radius=5.0,
    is_active=True
)

SAMPLE_RESTAURANT_2 = Restaurant(
    restaurant_id="301",
    owner_id="owner456",
    name="Burger Restaurant",
    location="456 Another St",
    postal_code="67890",
    contact_info="burger@restaurant.com",
    operating_hours="10am-10pm",
    delivery_radius=10.0,
    is_active=True
)

client = TestClient(app)

@patch("app.services.MenuItemService.MenuItemService.get_menu_by_restaurant")
@patch("app.services.Restaurant_service.RestaurantService.get_all_restaurants")
def test_search_by_name(mock_get_all, mock_get_menu):
    mock_get_all.return_value = [SAMPLE_RESTAURANT]
    mock_get_menu.return_value = [SAMPLE_MENUITEM]
    response = client.get("/search/?query=Test")
    # NEW: Access the "items" array first, then the first restaurant
    assert response.json()["items"][0]["restaurant_id"] == RESTAURANT_ID

@patch("app.services.MenuItemService.MenuItemService.get_menu_by_restaurant")
@patch("app.services.Restaurant_service.RestaurantService.get_all_restaurants")
def test_search_no_match(mock_get_all, mock_get_menu):
    mock_get_all.return_value = [SAMPLE_RESTAURANT]
    mock_get_menu.return_value = [SAMPLE_MENUITEM]
    response = client.get("/search/?query=NonExistent")
    # NEW: Expect an empty list for "items" and 0 for "total"
    assert response.json()["items"] == []
    assert response.json()["total"] == 0

@patch("app.services.MenuItemService.MenuItemService.get_menu_by_restaurant")
@patch("app.services.Restaurant_service.RestaurantService.get_all_restaurants")
def test_search_by_menu_item(mock_get_all, mock_get_menu):
    mock_get_all.return_value = [SAMPLE_RESTAURANT]
    mock_get_menu.return_value = [SAMPLE_MENUITEM]
    response = client.get("/search/?query=Pepperoni")
    assert response.json()["items"][0]["restaurant_id"] == RESTAURANT_ID

@patch("app.services.MenuItemService.MenuItemService.get_menu_by_restaurant")
@patch("app.services.Restaurant_service.RestaurantService.get_all_restaurants")
def test_search_case_insensitive(mock_get_all, mock_get_menu):
    mock_get_all.return_value = [SAMPLE_RESTAURANT]
    mock_get_menu.return_value = [SAMPLE_MENUITEM]
    response = client.get("/search/?query=pepperoni")
    assert response.json()["items"][0]["restaurant_id"] == RESTAURANT_ID

@patch("app.services.MenuItemService.MenuItemService.get_menu_by_restaurant")
@patch("app.services.Restaurant_service.RestaurantService.get_all_restaurants")
def test_search_return_only_once(mock_get_all, mock_get_menu):
    mock_get_all.return_value = [SAMPLE_RESTAURANT_2]
    mock_get_menu.return_value = [SAMPLE_MENUITEM_2]
    response = client.get("/search/?query=Burger")
    assert len(response.json()["items"]) == 1
    assert response.json()["items"][0]["restaurant_id"] == "301"

@patch("app.services.MenuItemService.MenuItemService.get_menu_by_restaurant")
@patch("app.services.Restaurant_service.RestaurantService.get_all_restaurants")
def test_return_all(mock_get_all, mock_get_menu):
    mock_get_all.return_value = [SAMPLE_RESTAURANT, SAMPLE_RESTAURANT_2]
    mock_get_menu.return_value = []
    response = client.get("/search/")
    assert len(response.json()["items"]) == 2
    assert response.json()["total"] == 2

@patch("app.services.Restaurant_service.RestaurantService.get_all_restaurants")
def test_return_all_empty(mock_get_all):
    mock_get_all.return_value = []
    response = client.get("/search/")
    assert response.json()["items"] == []
    assert response.json()["total"] == 0

@patch("app.services.MenuItemService.MenuItemService.get_menu_by_restaurant")
@patch("app.services.Restaurant_service.RestaurantService.get_all_restaurants")
def test_return_all_multiple_pages(mock_get_all, mock_get_menu):
    # Mocking 25 restaurants
    mock_get_all.return_value = [SAMPLE_RESTAURANT] * 25
    mock_get_menu.return_value = []
    
    # NEW: Test Page 1 (Skip 0, Limit 10)
    response_p1 = client.get("/search/?skip=0&limit=10")
    assert len(response_p1.json()["items"]) == 10
    assert response_p1.json()["total"] == 25
    
    # NEW: Test Page 3 (Skip 20, Limit 10 -> Should only have 5 left)
    response_p3 = client.get("/search/?skip=20&limit=10")
    assert len(response_p3.json()["items"]) == 5
    assert response_p3.json()["total"] == 25

@patch("app.services.MenuItemService.MenuItemService.get_menu_by_restaurant")
@patch("app.services.Restaurant_service.RestaurantService.get_all_restaurants")
def test_filter_by_price_category(mock_get_all, mock_get_menu):
    mock_get_all.return_value = [SAMPLE_RESTAURANT, SAMPLE_RESTAURANT_2]
    mock_get_menu.return_value = [SAMPLE_MENUITEM]
    response = client.get("/search/?price_category=$")
    assert response.json()["items"][0]["price_category"] == "$"

@patch("app.services.MenuItemService.MenuItemService.get_menu_by_restaurant")
@patch("app.services.Restaurant_service.RestaurantService.get_all_restaurants")
def test_filter_by_category(mock_get_all, mock_get_menu):
    mock_get_all.return_value = [SAMPLE_RESTAURANT, SAMPLE_RESTAURANT_2]
    mock_get_menu.return_value = [SAMPLE_MENUITEM] 
    response = client.get("/search/?category=Italian")
    assert len(response.json()["items"]) == 2