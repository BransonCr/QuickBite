import uuid
from fastapi import HTTPException

from app.schemas.Restaurant import Restaurant, RestaurantCreate, RestaurantUpdate
from app.models.RestaurantModel import load_all, save_all


class RestaurantService:
    def get_all_restaurants(self):
        return load_all()
    
    def _find_restaurant_or_404(self, restaurant_id: str, restaurants: list) -> Restaurant:
        restaurant = next((r for r in restaurants if r.restaurant_id == restaurant_id), None)
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        return restaurant
    
    def create_restaurant(self, restaurant: RestaurantCreate) -> Restaurant:
        restaurants = load_all()
        
        
        if any(r.name.lower() == restaurant.name.lower() and r.location.lower() == restaurant.location.lower() for r in restaurants):
            raise HTTPException(status_code=400, detail="Restaurant with this name and location already exists.")
            
        new_restaurant = Restaurant(
            restaurant_id=str(uuid.uuid4()),
            owner_id=restaurant.owner_id,
            name=restaurant.name,
            location=restaurant.location,
            postal_code=restaurant.postal_code,
            contact_info=restaurant.contact_info,
            operating_hours=restaurant.operating_hours,
            delivery_radius=restaurant.delivery_radius,
            is_active=True,
            menu_list=[]
        )   
        
        restaurants.append(new_restaurant)
        save_all(restaurants)
        return new_restaurant

    def update_restaurant(self, restaurant_id: str, restaurant_update: RestaurantUpdate) -> Restaurant:
        restaurants = load_all()
        restaurant_to_update = self._find_restaurant_or_404(restaurant_id, restaurants)
            
        update_data = restaurant_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(restaurant_to_update, key, value)

        save_all(restaurants)
        return restaurant_to_update
    
    def delete_restaurant(self, restaurant_id: str):
        restaurants = load_all()
        self._find_restaurant_or_404(restaurant_id, restaurants)
        restaurants = [r for r in restaurants if r.restaurant_id != restaurant_id]
        save_all(restaurants)

    def get_restaurant(self, restaurant_id: str) -> Restaurant:
        restaurants = load_all()
        return self._find_restaurant_or_404(restaurant_id, restaurants)
