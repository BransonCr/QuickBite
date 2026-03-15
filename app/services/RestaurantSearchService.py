from typing import List
from app.routers.Restaurant import get_all_restaurants
from app.schemas.RestaurantBrowse import RestaurantBrowseCreate, RestaurantBrowse

MAX_PER_PAGE = 10

class RestaurantSearchService:
    async def search_restaurants(self, query) -> List[List[RestaurantBrowse]]:
        restaurants = await get_all_restaurants()
        
        curr_page = 0

        filtered_restaurants = [[]]
        for restaurant in restaurants:
            if query.lower() in restaurant.name.lower():
                filtered_restaurant = RestaurantBrowseCreate(
                    restaurant_id=restaurant.restaurant_id,
                    name=restaurant.name,
                    location=restaurant.location
                )
                if len(filtered_restaurants[curr_page]) >= MAX_PER_PAGE:
                    curr_page += 1
                filtered_restaurants[curr_page].append(filtered_restaurant)
            else:
                for menuitem in restaurant.menu_list:
                    if query.lower() in menuitem.name.lower():
                        filtered_restaurant = RestaurantBrowseCreate(
                            restaurant_id=restaurant.restaurant_id,
                            name=restaurant.name,
                            location=restaurant.location
                        )
                        if len(filtered_restaurants[curr_page]) >= MAX_PER_PAGE:
                            curr_page += 1
                            filtered_restaurants.append([])
                        filtered_restaurants[curr_page].append(filtered_restaurant)
                        break
        return filtered_restaurants
    
    async def return_all_restaurants(self) -> List[List[RestaurantBrowse]]:
        restaurants = await get_all_restaurants()
        
        curr_page = 0

        all_restaurants = [[]]
        for restaurant in restaurants:
            restaurant_browse = RestaurantBrowseCreate(
                restaurant_id=restaurant.restaurant_id,
                name=restaurant.name,
                location=restaurant.location
            )
            if len(all_restaurants[curr_page]) >= MAX_PER_PAGE:
                curr_page += 1
                all_restaurants.append([])
            all_restaurants[curr_page].append(restaurant_browse)
        return all_restaurants