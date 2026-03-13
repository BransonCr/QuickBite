from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_current_user
from app.schemas.User import User, UserCreate, UserRole, UserUpdate
from app.services.UserService import UserService
router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


user_service = UserService()


@router.get("/")
async def get_users():
    return user_service.get_users()


@router.get("/{user_id}")
async def get_user(user_id: str):
    return user_service.get_user(user_id)


@router.post("/")
async def create_user(user: UserCreate):
    return user_service.create_user(user)


@router.put("/{user_id}")
async def update_user(user_id: str, user: UserUpdate):
    return user_service.update_user(user_id, user)


@router.delete("/{user_id}")
async def delete_user(user_id: str):
    return user_service.delete_user(user_id)
