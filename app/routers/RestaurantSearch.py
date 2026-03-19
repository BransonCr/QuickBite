from fastapi import APIRouter
from app.services.RestaurantSearchService import RestaurantSearchService

router = APIRouter(
    prefix="/search",
    tags=["search"],
    responses={404: {"description": "Restaurant not found"}},
)

service = RestaurantSearchService()

@router.get("/{query}")
async def get_search_restaurants(query: str):
    return service.search_restaurants(query)

@router.get("/")
async def get_all_restaurants():
    return service.return_all_restaurants()