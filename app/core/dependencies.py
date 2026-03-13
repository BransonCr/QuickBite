# FastAPI dependencies: get_current_user, require_role
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from app.core.security import decode_access_token
from app.schemas.User import User, UserRole
from app.services.UserService import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class TokenData(BaseModel):
    username: str
    role: UserRole


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_access_token(token)
    token_data = TokenData(username=payload["sub"], role=payload["role"])
    user = UserService().get_user_by_username(token_data.username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def require_role(allowed_roles: list[UserRole]):
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user

    return role_checker
