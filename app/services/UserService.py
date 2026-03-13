import uuid

from fastapi import HTTPException

from app.models.UserModel import load_all, save_all
from app.schemas.User import User, UserCreate, UserUpdate


class UserService:
    def get_users(self):
        return load_all()

    def get_user_by_username(self, username: str):
        users = load_all()
        for u in users:
            if u.username == username:
                return u
        return None

    def create_user(self, user: UserCreate) -> User:
        new_user = User(user_id=str(uuid.uuid4()), **user.model_dump())
        users = load_all()
        users.append(new_user)
        save_all(users)
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
