import csv
from pathlib import Path
from typing import List

from app.schemas.Review import Review, ReviewCreate

DATA_DIR = Path(__file__).parent.parent / "db"
REVIEWS_CSV = DATA_DIR / "review.csv"

FIELDS = list(Review.model_fields.keys())


def load_all() -> List[Review]:
    reviews = []
    if REVIEWS_CSV.exists():
        with open(REVIEWS_CSV, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                reviews.append(Review.model_validate(row))
    return reviews


def save_review(review: Review) -> None:
    write_header = not REVIEWS_CSV.exists() or REVIEWS_CSV.stat().st_size == 0
    with open(REVIEWS_CSV, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if write_header:
            writer.writeheader()
        writer.writerow(review.model_dump())


def save_all(reviews: List[Review]) -> None:
    with open(REVIEWS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for review in reviews:
            writer.writerow(review.model_dump())
