import uuid
from fastapi import HTTPException

from app.schemas.Restaurant import Restaurant, RestaurantCreate, RestaurantUpdate
from app.models.RestaurantModel import load_all,save_all
from app.schemas.MenuItem import MenuItem
class RestaurantService:
    def get_all(self):
        return load_all()
    
    def create_restaurant(self,restaurant:RestaurantCreate) ->Restaurant:
        restaurants = load_all()
        for r in restaurants:
            if r.name.lower() == restaurant.name.lower() and r.location.lower() == restaurant.location.lower():
                raise HTTPException(status_code=400, detail="Restaurant with this name and location already exists.")
            
        new_restaurant = Restaurant(
            restaurant_id =str(uuid.uuid4()),
            owner_id = restaurant.owner_id,
            name = restaurant.name,
            location = restaurant.location,
            postal_code = restaurant.postal_code,
            contact_info=restaurant.contact_info,
            operating_hours=restaurant.operating_hours,
            delivery_radius = restaurant.delivery_radius,
            is_active = True,
            menu_list = []
        )   
        restaurants.append(new_restaurant)
        save_all(restaurants)
        return new_restaurant
        

    def update_restaurant(self, restaurant_id: str, restaurant_update: RestaurantUpdate) -> Restaurant:
        restaurants = load_all()
        for r in restaurants:
            if r.restaurant_id == restaurant_id:
                update_data = restaurant_update.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(r, key, value)

                save_all(restaurants)
                return r
                
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    def delete_restaurant(self, restaurant_id: str):
        restaurants = load_all()
        for r in restaurants:
            if r.restaurant_id == restaurant_id:
                restaurants.remove(r)
                save_all(restaurants)
                return
        
        raise HTTPException(status_code=404, detail="Restaurant not found")
    def get_restaurant(self,restaurant_id:str):
        restaurants = load_all()
        for r in restaurants:
            if r.restaurant_id == restaurant_id:
                return r

        raise HTTPException(status_code=404,detail="restaurant not retrieve")

