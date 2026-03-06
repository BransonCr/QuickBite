from pydantic import BaseModel

class Review(BaseModel):
    review_id: str
    customer_id: str
    restaurant_id: str
    order_id: str
    rating: int
    text: str
    created_at: str

class ReviewCreate(BaseModel):
    customer_id: str
    restaurant_id: str
    order_id: str
    rating: int
    text: str

class ReviewUpdate(BaseModel):
    rating: int
    text: str
# update to be changed when needed.