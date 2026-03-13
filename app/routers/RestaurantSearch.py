from fastapi import APIRouter
from app.core.search_and_filter import filter_restaurants

router = APIRouter(
    prefix="/search",
    tags=["search"],
    responses={404: {"description": "Review not found"}},
)

@router.get("/{query}")
async def search_restaurants(query: str):
    return await filter_restaurants(query)