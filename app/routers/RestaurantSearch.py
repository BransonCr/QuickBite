from fastapi import APIRouter, Query
from app.services.RestaurantSearchService import RestaurantSearchService

router = APIRouter(
    prefix="/search",
    tags=["search"],
    responses={404: {"description": "Restaurant not found"}},
)

service = RestaurantSearchService()

@router.get("/")
async def search_restaurants(query: str = Query(default=""), price_category: str = Query(default=None), category: str = Query(default=None)):
    return service.search_restaurants(query, price_category, category)