import uuid

from fastapi import HTTPException

from app.models.UserModel import load_all, save_all
from app.schemas.User import User, UserCreate, UserUpdate


class UserService:
    def get_users(self):
        return load_all()

    def create_user(self, user: UserCreate) -> User:
        new_user = User(user_id=str(uuid.uuid4()), **user.model_dump())
        new_userEmail, new_username = new_user.email, new_user.username
        if new_userEmail or new_username:
            existing_users = load_all()
            for u in existing_users:
                if u.email == new_userEmail or u.username == new_username:
                    raise HTTPException(status_code=400, detail="Email or username already exists")
        save_all([new_user])
        return new_user

    def update_user(self, user_id: str, user: UserUpdate) -> User:
        users = load_all()
        for u in users:
            if u.user_id == user_id:
                for k, v in user.model_dump().items():
                    setattr(u, k, v)
                save_all(users)
                return u
        raise HTTPException(status_code=404, detail="User not found")

    def delete_user(self, user_id: str) -> None:
        users = load_all()
        for u in users:
            if u.user_id == user_id:
                users.remove(u)
                save_all(users)
                return
        raise HTTPException(status_code=404, detail="User not found")

    def get_user(self, user_id: str) -> User:
        users = load_all()
        for u in users:
            if u.user_id == user_id:
                return u
        raise HTTPException(status_code=404, detail="User not found")
