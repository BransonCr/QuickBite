import csv
from pathlib import Path
from typing import List

from app.schemas.MenuItem import MenuItem

DATA_DIR = Path(__file__).parent.parent / "db"
MENUITEMS_CSV = DATA_DIR / "menuitem.csv"

def load_all() -> List[MenuItem]:
    menu_items = []
    with open(MENUITEMS_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            menu_items.append(MenuItem.model_validate(row))
    return menu_items

def save_all(menu_items: List[MenuItem]) -> None:
    with open(MENUITEMS_CSV, "w") as f:
        writer = csv.DictWriter(f, fieldnames=list(MenuItem.model_fields.keys()))
        writer.writeheader()
        for menu_item in menu_items:
            writer.writerow(menu_item.model_dump())