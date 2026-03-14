from fastapi import APIRouter
from app.services.RestaurantSearchService import search_restaurants

router = APIRouter(
    prefix="/search",
    tags=["search"],
    responses={404: {"description": "Review not found"}},
)

@router.get("/{query}")
async def get_search_restaurants(query: str):
    return await search_restaurants(query)