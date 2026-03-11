import uuid
from datetime import datetime, timezone

from fastapi import HTTPException

from app.models.ReviewModel import load_all, save_review, save_all
from app.schemas.Review import Review, ReviewCreate, ReviewUpdate


class ReviewService:
    def get_review(self):
        return load_all()

    def get_review_by_id(self, review_id: str):
        reviews = load_all()
        # iterate through reviews to find the one with the matching review_id
        review = next((r for r in reviews if r.review_id == review_id), None)
        if review is None:
            raise HTTPException(status_code=404, detail="Review not found")
        return review

    def create_review(self, review: ReviewCreate) -> Review:
        new_review = Review(
            review_id=str(uuid.uuid4()),
            customer_id=review.customer_id,
            restaurant_id=review.restaurant_id,
            order_id=review.order_id,
            rating=review.rating,
            text=review.text,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        save_review(new_review)
        return new_review

    def update_review(self, review_id: str, update: ReviewUpdate) -> Review:
        reviews = load_all()
        for review in reviews:
            if review.review_id == review_id:
                review.rating = update.rating
                review.text = update.text
                save_all(reviews)
                return review
        raise HTTPException(status_code=404, detail="Review not found")

    def delete_review(self, review_id: str) -> None:
              reviews = load_all()
              filtered = [r for r in reviews if r.review_id != review_id]
              if len(filtered) == len(reviews):
                  raise HTTPException(status_code=404, detail="Review not found")
              save_all(filtered)
