from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from app.core.security import verify_password, create_access_token
from app.services.UserService import UserService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class UserLogin(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(user: UserLogin, userService: UserService = Depends()):
    db_user = userService.get_user_by_username(user.username)
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": db_user.username, "role": db_user.role})
    return {"access_token": token, "token_type": "bearer"}
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from app.services.UserService import UserService
from app.schemas.User import UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "changeme"
ALGORITHM = "HS256"
RESET_TOKEN_EXPIRE_MINUTES = 15

router = APIRouter()
userService = UserService()

class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


def create_reset_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_reset_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, userService: UserService = Depends()):
    user = userService.get_user_by_email(request.email)
    if not user:
        raise HTTPException(status_code=404, detail="No account found with that email")
    token = create_reset_token(user.username)
    return {"reset_token": token}


@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, userService: UserService = Depends()):
    username = decode_reset_token(request.token)
    user = userService.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    userService.update_user(user.user_id, UserUpdate(password_hash=pwd_context.hash(request.new_password)))
    return {"message": "Password updated successfully"}

@router.post("/register", response_model=UserPublic, status_code=201)
async def register(user: UserCreate, userService: UserService = Depends()):
    return userService.create_user(user)
