import ast
import csv 
from pathlib import Path
from typing import List, Dict, Any


from app.schemas.Restaurant import Restaurant
DATA_DIR = Path(__file__).parent.parent/"db"

RESTAURANT_CSV = DATA_DIR/"restaurant.csv"



def load_all() ->List[Restaurant]:
    restaurants =[]
    if RESTAURANT_CSV.exists():
        with open(RESTAURANT_CSV,"r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'menu_list' in row and isinstance(row['menu_list'], str):
                    try:
                        row['menu_list'] = ast.literal_eval(row['menu_list'])
                    except (ValueError, SyntaxError):
                        row['menu_list'] = []
                restaurants.append(Restaurant.model_validate(row))
    return restaurants
    

def save_all(restaurants: List[Restaurant]) -> None:
    with open(RESTAURANT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(Restaurant.model_fields.keys()))
        writer.writeheader()
        for restaurant in restaurants:
            row = restaurant.model_dump()
            if 'menu_list' in row:
                row['menu_list'] = str(row['menu_list'])
            writer.writerow(row)