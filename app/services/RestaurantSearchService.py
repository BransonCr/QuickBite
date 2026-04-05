from typing import List
from app.schemas import Restaurant
from app.services.MenuItemService import MenuItemService
from app.services.Restaurant_service import RestaurantService
from app.schemas.RestaurantBrowse import RestaurantBrowse

MAX_PER_PAGE = 10

class RestaurantSearchService:
    def __init__(self):
        self.restaurant_service = RestaurantService()
        self.menu_item_service = MenuItemService()

    def search_restaurants(self, query: str) -> List[List[RestaurantBrowse]]:
        restaurants = self.restaurant_service.get_all_restaurants()
        
        curr_page = 0
        query_lower = query.lower()

        filtered_restaurants = [[]]
        for restaurant in restaurants:
            if query_lower in restaurant.name.lower():
                curr_page = add_restaurant(filtered_restaurants, curr_page, restaurant)
            else:
                menu_items = self.menu_item_service.get_menu_by_restaurant(restaurant.restaurant_id)
                print(menu_items)
                for menuitem in menu_items:
                     if query_lower in menuitem.name.lower():
                        curr_page = add_restaurant(filtered_restaurants, curr_page, restaurant)
                        break
        return filtered_restaurants
    
    def browse_all_restaurants(self) -> List[List[RestaurantBrowse]]:
        restaurants = self.restaurant_service.get_all_restaurants()
        
        curr_page = 0

        all_restaurants = [[]]
        for restaurant in restaurants:
            curr_page = add_restaurant(all_restaurants, curr_page, restaurant)
        return all_restaurants

def create_restaurant_browse(restaurant: Restaurant) -> RestaurantBrowse:
    return RestaurantBrowse(
        restaurant_id=restaurant.restaurant_id,
        name=restaurant.name,
        location=restaurant.location
    )

def ensure_page_capacity(restaurants: List[List[RestaurantBrowse]], curr_page: int) -> int:
    if len(restaurants[curr_page]) >= MAX_PER_PAGE:
        curr_page += 1
        restaurants.append([])
    return curr_page

def add_restaurant(restaurants: List[List[RestaurantBrowse]], curr_page: int, restaurant: Restaurant) -> int:
    restaurant_browse = create_restaurant_browse(restaurant)
    curr_page = ensure_page_capacity(restaurants, curr_page)
    restaurants[curr_page].append(restaurant_browse)
    return curr_page