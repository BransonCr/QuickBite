import uuid
from fastapi import HTTPException

from app.schemas.Restaurant import Restaurant, RestaurantCreate, RestaurantUpdate
from app.models.RestaurantModel import load_all,save_all
from app.schemas.MenuItem import MenuItem
class RestaurantService:
    def get_all(self):
        return load_all()
    
    def create_restaurant(self,restaurant:RestaurantCreate) ->Restaurant:
        new_restaurant = Restaurant(
            restaurant_id =str(uuid.uuid4()),
            owner_id = restaurant.owner_id,
            name = restaurant.name,
            location = restaurant.location,
            postal_code = restaurant.postal_code,
            delivery_radius = restaurant.delivery_radius,
            is_active = True,
            menu_list = list[MenuItem]
        )   
        restaurants = load_all()
        restaurant.append(new_restaurant)
        save_all(restaurants)
        return new_restaurant
        

    def update_restaurant(self,restaurant_id:str,restaurant:RestaurantUpdate)->Restaurant:
        restaurants = load_all()
        for r in restaurants:
            if r.restaurant_id==restaurant_id:
                r.owner_id = restaurant.owner_id
                r.name = restaurant.name
                r.location = restaurant.location
                r.postal_code = restaurant.postal_code
                r.delivery_radius = restaurant.delivery_radius
                r.is_active = restaurant.is_active
                r.menu_list = restaurant.menu_list
                save_all(restaurants)
                return r
        raise HTTPException(status_code=404,detail="restaurant not updated")
    
    def delete_restaurant(self,restaurant_id:str):
         restaurants = load_all()
         for r in restaurants:
            if r.restaurant_id == restaurant_id:
                restaurants.remove(r)
                save_all(restaurants)
                return
            raise HTTPException(status_code=404,detail="restaurant not deleted")
    def get_restaurant(self,restaurant_id:str):
        restaurants = load_all()
        for r in restaurants:
            if r.restaurant_id == restaurant_id:
                return r

        raise HTTPException(status_code=404,detail="restaurant not retrieve")


