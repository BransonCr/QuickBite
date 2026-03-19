from typing import List
from app.services.Restaurant_service import RestaurantService
from app.schemas.RestaurantBrowse import RestaurantBrowse, RestaurantBrowse

MAX_PER_PAGE = 10

class RestaurantSearchService:
    def __init__(self):
        self.restaurant_service = RestaurantService()

    def search_restaurants(self, query) -> List[List[RestaurantBrowse]]:
        restaurants = self.restaurant_service.get_all_restaurants()
        
        curr_page = 0

        filtered_restaurants = [[]]
        for restaurant in restaurants:
            if query.lower() in restaurant.name.lower():
                filtered_restaurant = create_restaurant_broswe(restaurant)
                curr_page = check_pageination(filtered_restaurants, curr_page)
                filtered_restaurants[curr_page].append(filtered_restaurant)
            else:
                for menuitem in restaurant.menu_list:
                    if query.lower() in menuitem.name.lower():
                        filtered_restaurant = create_restaurant_broswe(restaurant)
                        curr_page = check_pageination(filtered_restaurants, curr_page)
                        filtered_restaurants[curr_page].append(filtered_restaurant)
                        break
        return filtered_restaurants
    
    def return_all_restaurants(self) -> List[List[RestaurantBrowse]]:
        restaurants = self.restaurant_service.get_all_restaurants()
        
        curr_page = 0

        all_restaurants = [[]]
        for restaurant in restaurants:
            restaurant_browse = create_restaurant_broswe(restaurant)
            curr_page = check_pageination(all_restaurants, curr_page)
            all_restaurants[curr_page].append(restaurant_browse)
        return all_restaurants
    
def create_restaurant_broswe(restaurant):
    return RestaurantBrowse(
        restaurant_id=restaurant.restaurant_id,
        name=restaurant.name,
        location=restaurant.location
    )

def check_pageination(restaurants, curr_page):
    if len(restaurants[curr_page]) >= MAX_PER_PAGE:
        curr_page += 1
        restaurants.append([])
    return curr_page