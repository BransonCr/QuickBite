import csv
from pathlib import Path
from typing import List

from app.schemas.User import User

DATA_DIR = Path(__file__).parent.parent / "db"
USERS_CSV = DATA_DIR / "users.csv"


def load_all() -> List[User]:
    users = []
    if USERS_CSV.exists():
        with open(USERS_CSV, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                users.append(User.model_validate(row))
    return users


def save_all(users):
    with open(DATA_DIR / "users.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=list(User.model_fields.keys()))
        writer.writeheader()
        for user in users:
            writer.writerow(user.model_dump())
