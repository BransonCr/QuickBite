import csv
from pathlib import Path
from typing import List

from app.schemas.User import User

# DATA_DIR points to app/db/ where all CSV files live.
# USERS_CSV is the full path to the users CSV file.
DATA_DIR = Path(__file__).parent.parent / "db"
USERS_CSV = DATA_DIR / "users.csv"


def load_all() -> List[User]:
    users = []
    # only try to open the file if it exists, otherwise return empty list
    if USERS_CSV.exists():
        with open(USERS_CSV, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # reading/append users to list, convert each row to user.dict() in servcies
                # Since the schema is UserRole enum, we use model_validate to convert row to User model
                # and append it to the users list, passing as plain text throws err.
                users.append(User.model_validate(row))
    return users


def save_all(users):
    with open(DATA_DIR / "users.csv", "w") as f:
        # warning just says don't call it on an instance (e.g. user.model_fields). Calling
        # it on the class is totally fine.
        writer = csv.DictWriter(f, fieldnames=list(User.model_fields.keys()))
        writer.writeheader()
        for user in users:
            # Just writing rows to the csv test.
            #  model_dump() serializes the User object back to a plain dict for CSV writing
            writer.writerow(user.model_dump())
