import uuid
from datetime import datetime, timezone

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
        users = load_all()
        for u in users:
            if u.username == user.username:
                raise HTTPException(status_code=400, detail="Username already exists")
            if u.email == user.email:
                raise HTTPException(status_code=400, detail="Email already exists")
        new_user = User(
            user_id=str(uuid.uuid4()),
            username=user.username,
            email=user.email,
            password_hash=user.password,
            phone=user.phone,
            role=user.role,
            location=user.location,
            postal_code=user.postal_code,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        users.append(new_user)
        save_all(users)
        return new_user

    def update_user(self, user_id: str, user: UserUpdate) -> User:
        users = load_all()
        for u in users:
            if u.user_id == user_id:
                for k, v in user.model_dump().items():
                    if v is not None:
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

    def get_user_by_email(self, email: str):
        users = load_all()
        for u in users:
            if u.email == email:
                return u
        return None
