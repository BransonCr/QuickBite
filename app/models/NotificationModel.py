import csv
from pathlib import Path
from typing import List

from app.schemas.Notification import Notification

DATA_DIR = Path(__file__).parent.parent / "db"
NOTIFICATIONS_CSV = DATA_DIR / "notification.csv"

def load_all() -> List[Notification]:
    notifications = []
    with open(NOTIFICATIONS_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            notifications.append(Notification.model_validate(row))
    return notifications

def save_all(notifications: List[Notification]) -> None:
    with open(NOTIFICATIONS_CSV, "w") as f:
        writer = csv.DictWriter(f, fieldnames=list(Notification.model_fields.keys()))
        writer.writeheader()
        for notification in notifications:
            writer.writerow(notifications.model_dump())