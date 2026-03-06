from fastapi import APIRouter

from app.schemas.Review import Review, ReviewCreate, ReviewUpdate

router = APIRouter(
    prefix="/review",
    tags=["review"],
    responses={404: {"description": "Review not found"}},
)


@router.get("/")
async def get_reviews():
    return []


@router.get("/{review_id}")
async def get_review(review_id: int):
    return {"review_id": review_id}


@router.post("/")
async def create_review(review: ReviewCreate):
    return review


@router.put("/{review_id}")
async def update_review(review_id: int, review: ReviewUpdate):
    return {"message": f"Review {review_id} updated"}


@router.delete("/{review_id}")
async def delete_review(review_id: int):
    return {"message": f"Review {review_id} deleted"}