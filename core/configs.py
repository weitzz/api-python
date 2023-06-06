from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_STR: str = "/api"
    DB_URL: str = "postgresql+asyncpg://postgres:admin@localhost:5432/pharmadb"
    DBBaseModel = declarative_base()

    class Config:
        case_sensitive = True


settings = Settings()
