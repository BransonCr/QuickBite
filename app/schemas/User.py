from typing import Optional
from pydantic import BaseModel
from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"
    DELIVERY_DRIVER = "DELIVERY_DRIVER"
    RESTAURANT_OWNER = "RESTAURANT_OWNER"


class User(BaseModel):
    user_id: str
    username: str
    email: str
    password_hash: str
    phone: str
    role: UserRole
    location: str
    postal_code: str
    created_at: str


class UserPublic(BaseModel):
    user_id: str
    username: str
    email: str
    phone: str
    role: UserRole
    location: str
    postal_code: str
    created_at: str


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    phone: str
    role: UserRole = UserRole.CUSTOMER
    location: str
    postal_code: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password_hash: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[UserRole] = None
    location: Optional[str] = None
    postal_code: Optional[str] = None
