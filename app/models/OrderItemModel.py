import csv
from pathlib import Path
from typing import List

from app.schemas.OrderItem import OrderItem

DATA_DIR = Path(__file__).parent.parent / "db"
ORDER_ITEMS_CSV = DATA_DIR / "orderitems.csv"

def load_all() -> List[OrderItem]:
    order_items = []
    if ORDER_ITEMS_CSV.exists():
        with open(ORDER_ITEMS_CSV, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                order_items.append(OrderItem.model_validate(row))
    return order_items

def save_all(order_items: List[OrderItem]):
    with open(ORDER_ITEMS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(OrderItem.model_fields.keys()))
        writer.writeheader()
        for item in order_items:
            writer.writerow(item.model_dump())
