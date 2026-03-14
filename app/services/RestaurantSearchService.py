from app.routers.Restaurant import get_all_restaurants

async def search_restaurants(query):
    restaurants = await get_all_restaurants()
    
    filtered_restaurants = []
    for restaurant in restaurants:
        if query.lower() in restaurant.name.lower():
            filtered_restaurants.append(restaurant)
        else:
            for menuitem in restaurant.menu_list:
                if query.lower() in menuitem.name.lower():
                    filtered_restaurants.append(restaurant)
                    break
    return filtered_restaurants