# loads .env vars (SECRET_KEY, ALGORITHM, TOKEN_EXPIRE_MINUTES)
# load .env vars (SECRET_KEY, ALGORITHM, TOKEN_EXPIRE_MINUTES)
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
