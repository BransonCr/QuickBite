from typing import List
from app.schemas import Restaurant
from app.services.MenuItemService import MenuItemService
from app.services.Restaurant_service import RestaurantService
from app.schemas.RestaurantBrowse import RestaurantBrowse

LOW_PRICE_THRESHOLD = 15
MEDIUM_PRICE_THRESHOLD = 30
LOW_PRICE_CATEGORY = "$"
MEDIUM_PRICE_CATEGORY = "$$"
HIGH_PRICE_CATEGORY = "$$$"

class RestaurantSearchService:
    def __init__(self):
        self.restaurant_service = RestaurantService()
        self.menu_item_service = MenuItemService()

    def search_restaurants(self, query: str, price_category: str = None, category: str = None) -> List[RestaurantBrowse]:
        restaurants = self.restaurant_service.get_all_restaurants()
        
        filtered_restaurants = []

        for restaurant in restaurants:
            menu_items = self.menu_item_service.get_menu_by_restaurant(restaurant.restaurant_id)
            
            if price_category:
                avg = self._calculate_average_price(menu_items)
                if self._get_price_category(avg) != price_category:
                    continue
            
            if category:
                if not any(category.lower() in mi.category.lower() for mi in menu_items):
                    continue
                
            if query:
                query_lower = query.lower()
                name_match = query_lower in restaurant.name.lower()
                item_match = any(query_lower in mi.name.lower() for mi in menu_items)
                if not name_match and not item_match:
                    continue
                
            restaurant_browse = self.create_restaurant_browse(restaurant, menu_items)
            filtered_restaurants.append(restaurant_browse)

        return filtered_restaurants

    def _calculate_average_price(self, menu_items: list) -> float:
        if not menu_items:
            return 0.0
        return sum(item.price for item in menu_items) / len(menu_items)

    def _get_price_category(self, avg: float) -> str:
        if avg == 0.0:
            return None
        elif avg < LOW_PRICE_THRESHOLD:
            return LOW_PRICE_CATEGORY
        elif avg < MEDIUM_PRICE_THRESHOLD:
            return MEDIUM_PRICE_CATEGORY
        else:
            return HIGH_PRICE_CATEGORY

    def create_restaurant_browse(self, restaurant: Restaurant, menu_items=None) -> RestaurantBrowse:
        if menu_items is None:
            menu_items = self.menu_item_service.get_menu_by_restaurant(restaurant.restaurant_id)
        avg = self._calculate_average_price(menu_items)
        
        return RestaurantBrowse(
            restaurant_id=restaurant.restaurant_id,
            name=restaurant.name,
            location=restaurant.location,
            average_price=avg,
            price_category=self._get_price_category(avg)
        )