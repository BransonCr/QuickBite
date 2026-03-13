from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from app.schemas.Auth import ForgotPasswordRequest, ResetPasswordRequest, UserLogin
from app.schemas.User import UserCreate, UserPublic
from app.services.AuthService import AuthService
from app.services.UserService import UserService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/login")
async def login(user: UserLogin, auth_service: AuthService = Depends()):
    return auth_service.login(user.username, user.password)


@router.post("/register", response_model=UserPublic, status_code=201)
async def register(user: UserCreate, user_service: UserService = Depends()):
    return user_service.create_user(user)


@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, auth_service: AuthService = Depends()):
    return auth_service.forgot_password(request.email)


@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, auth_service: AuthService = Depends()):
    return auth_service.reset_password(request.token, request.new_password)
