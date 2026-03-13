
from fastapi import Depends, HTTPException

from app.core.security import create_access_token, decode_access_token, verify_password
from app.schemas.User import UserUpdate
from app.services.UserService import UserService


class AuthService:
    def __init__(self, user_service: UserService = Depends()):
        self.user_service = user_service

    def login(self, username: str, password: str) -> dict:
        user = self.user_service.get_user_by_username(username)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token({"sub": user.username, "role": user.role})
        return {"access_token": token, "token_type": "bearer"}

    def forgot_password(self, email:str) -> dict:
        user = self.user_service.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="No account found with that email")
        token = create_access_token({"sub": user.username, "role": user.role}, expires_minutes=15)
        return {"reset_token": token}

    def reset_password(self, token: str, new_password: str) -> dict:
        decoded = decode_access_token(token)
        user = self.user_service.get_user_by_username(decoded["sub"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        self.user_service.update_user(user.user_id, UserUpdate(password_hash=new_password))
        return {"message": "Password updated successfully"}
