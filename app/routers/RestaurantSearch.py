from fastapi import APIRouter
from app.services.RestaurantSearchService import RestaurantSearchService

router = APIRouter(
    prefix="/search",
    tags=["search"],
    responses={404: {"description": "Review not found"}},
)

service = RestaurantSearchService()

@router.get("/{query}")
async def get_search_restaurants(query: str):
    return await service.search_restaurants(query)