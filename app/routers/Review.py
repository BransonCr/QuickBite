from fastapi import APIRouter

from app.schemas.Review import Review, ReviewCreate, ReviewUpdate
from app.services.ReviewService import ReviewService

router = APIRouter(
    prefix="/review",
    tags=["review"],
    responses={404: {"description": "Review not found"}},
)

service = ReviewService()


@router.get("/")
async def get_reviews():
    return service.get_review()


@router.get("/{review_id}")
async def get_review(review_id: str):
    return service.get_review_by_id(review_id)


@router.post("/")
async def create_review(review: ReviewCreate):
    return service.create_review(review)


@router.put("/{review_id}")
async def update_review(review_id: str, review: ReviewUpdate):
    return service.update_review(review_id, review)


@router.delete("/{review_id}")
async def delete_review(review_id: str):
    return service.delete_review(review_id)
