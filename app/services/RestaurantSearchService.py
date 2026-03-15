from typing import List
from app.routers.Restaurant import get_all_restaurants
from app.schemas.RestaurantBrowse import RestaurantBrowseCreate, RestaurantBrowse

class RestaurantSearchService:
    async def search_restaurants(self, query) -> List[RestaurantBrowse]:
        restaurants = await get_all_restaurants()
        
        filtered_restaurants = []
        for restaurant in restaurants:
            if query.lower() in restaurant.name.lower():
                filtered_restaurant = RestaurantBrowseCreate(
                    restaurant_id=restaurant.restaurant_id,
                    name=restaurant.name,
                    location=restaurant.location
                )
                filtered_restaurants.append(filtered_restaurant)
            else:
                for menuitem in restaurant.menu_list:
                    if query.lower() in menuitem.name.lower():
                        filtered_restaurant = RestaurantBrowseCreate(
                            restaurant_id=restaurant.restaurant_id,
                            name=restaurant.name,
                            location=restaurant.location
                        )
                        filtered_restaurants.append(filtered_restaurant)
                        break
        return filtered_restaurants