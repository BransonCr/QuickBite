from fastapi import APIRouter

from app.schemas.User import UserCreate, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
def create_user(user: UserCreate):
    return {"user": user}


@router.put("/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    return {"user_id": user_id, "user": user}


@router.get("/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}


@router.delete("/{user_id}")
def delete_user(user_id: int):
    return {"user_id": user_id}
