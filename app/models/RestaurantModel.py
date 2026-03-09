import csv 
from pathlib import Path
from typing import List, Dict, Any


from app.schemas.Restaurant import Restaurant
DATA_DIR = Path(__file__).resolve().parent/"db"

RESTAURANT_CSV = DATA_DIR/"restaurant.csv"



def load_all() ->List[Restaurant]:
    restaurants =[]
    with open(RESTAURANT_CSV,"r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            restaurants.append(Restaurant.model.validate(row))
        return restaurants
    

def save_all(restaurants: List[Restaurant])->None:
    with open( RESTAURANT_CSV,"w") as f:
        writer = csv.DictWriter(f,fieldnames=list(Restaurant.model.field.keys()))
        writer.writeheader()
        for restaurant in restaurants:
            writer.writerow(restaurant.model_dump())