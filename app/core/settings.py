from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DEBUG: bool = True
    APP_ENV: str = "development"

    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    FERNET_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()