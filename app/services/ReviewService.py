import uuid
from datetime import datetime, timezone

from fastapi import HTTPException

from app.models.ReviewModel import load_all, save_review, save_all
from app.schemas.Review import Review, ReviewCreate, ReviewUpdate
from app.services.BaseService import BaseService


class ReviewService(BaseService):
    def get_review(self):
        return load_all()

    def get_review_by_id(self, review_id: str):
        return self.find_by_id(load_all(), "review_id", review_id, "Review not found")

    def create_review(self, review: ReviewCreate) -> Review:
        new_review = Review(
            review_id=str(uuid.uuid4()),
            **review.model_dump(),
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        save_review(new_review)
        return new_review

    def update_review(self, review_id: str, update: ReviewUpdate) -> Review:
        reviews = load_all()
        review = self.find_by_id(reviews, "review_id", review_id, "Review not found")
        update_data = update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(review, key, value)
            
        save_all(reviews)
        return review

    def delete_review(self, review_id: str) -> None:
              reviews = load_all()
              filtered = [r for r in reviews if r.review_id != review_id]
              if len(filtered) == len(reviews):
                  raise HTTPException(status_code=404, detail="Review not found")
              save_all(filtered)
