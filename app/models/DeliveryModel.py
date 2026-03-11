import csv
import os
from pathlib import Path
from typing import Optional

from app.schemas.Delivery import Delivery

DATA_DIR = Path(__file__).parent.parent / "db"
DELIVERY_CSV = DATA_DIR / "delivery.csv"

FIELDS = ["delivery_id", "order_id", "driver_id", "status", "address", "instructions"]


def load_all() -> list[Delivery]:
    if not os.path.exists(DELIVERY_CSV):
        return []
    with open(DELIVERY_CSV, newline="") as f:
        reader = csv.DictReader(f)
        return [Delivery.model_validate(row) for row in reader]


def save_all(deliveries: list[Delivery]) -> None:
    with open(DELIVERY_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for d in deliveries:
            writer.writerow(d.model_dump())


def delete_delivery(delivery_id: str) -> bool:
    deliveries = load_all()
    filtered = [d for d in deliveries if d.delivery_id != delivery_id]
    if len(filtered) == len(deliveries):
        return False
    save_all(filtered)
    return True


def get_by_id(delivery_id: str) -> Optional[Delivery]:
    deliveries = load_all()
    for d in deliveries:
        if d.delivery_id == delivery_id:
            return d
    return None
