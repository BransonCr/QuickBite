import csv
from pathlib import Path
from typing import List
from app.schemas.Order import Order

DATA_DIR = Path(__file__).parent.parent / "db"
ORDERS_CSV = DATA_DIR / "orders.csv"

def load_all() -> List[Order]:
    orders = []
    if ORDERS_CSV.exists():
        with open(ORDERS_CSV, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                orders.append(Order.model_validate(row))
    return orders

def save_all(orders: List[Order]):
    with open(ORDERS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(Order.model_fields.keys()))
        writer.writeheader()
        for order in orders:
            writer.writerow(order.model_dump())