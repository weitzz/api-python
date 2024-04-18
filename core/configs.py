from pydantic import BaseSettings
from sqlalchemy.orm import declarative_base


class Settings(BaseSettings):
    API_STR: str = '/api'
    DB_URL: str = 'postgresql+asyncpg://postgres:admin@pharmadb:5432/pharmadb'
    DBBaseModel = declarative_base()
    JWT_SECRET: str = 'aouPY_Uv2j3HmXAKZTG_9MComFqhZqKRMKRKie458y8'

    ALGORITHM: str = 'HS256'

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    """
    import secrets
    
    token:str = secrets.token_urlsafe(32)
    '-qyugDKOVP3kdoQY3xw0n-c88KnuYm0APEy7Xa8oM3Y'

    """

    class Config:
        case_sensitive = True


settings: Settings = Settings()
