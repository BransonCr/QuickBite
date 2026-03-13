from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from jose import JWTError, jwt

from app.core.config import settings


# Could use bcrypt hashing but lets just use plain text for now
def verify_password(plain: str, stored: str) -> bool:
    return plain == stored


def create_access_token(data: dict, expires_minutes: int = None) -> str:
    payload = data.copy()
    expire = expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=expire)
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict:
    credentials_error = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        if payload.get("sub") is None:
            raise credentials_error
        return payload
    except JWTError:
        raise credentials_error
