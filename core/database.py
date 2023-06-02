from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine,AsyncSession
from core.configs import setting

engine: AsyncEngine = create_async_engine(setting.DB_URL)

Session: AsyncSession = sessionmaker(
    autoflush= False,
    autocommit = False,
    expire_on_commit= False,
    class_= AsyncSession,
    bind= engine
)
