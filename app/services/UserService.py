import uuid

from fastapi import HTTPException

from app.models.UserModel import load_all, save_all
from app.schemas.User import User, UserCreate, UserUpdate
from app.services.UserService import UserService


class UserService:
    def get_users(self):
        return load_all()

    def create_user(self, user: UserCreate) -> User:
        # uuid generates a new userId.
        # also note that user.model_dump() returns a dict with all fields, however passing in
        # user.model_dump() directly as pos argument is not allowed, so we use kwargs instead
        # (**kwargs) to unpack the dict into keyword arguments for the User constructor
        new_user = User(user_id=str(uuid.uuid4()), **user.model_dump())  #
        save_all([new_user])
        return new_user

    def update_user(self, user_id: str, user: UserUpdate):
        users = load_all()
        for u in users:
            if u.user_id == user_id:
                # iterate over updated fields and apply them to the matching user
                for k, v in user.model_dump().items():
                    setattr(u, k, v)
                save_all(users)
                return u
        raise HTTPException(status_code=404, detail="User not found")

    def delete_user(self, user_id: str):
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
