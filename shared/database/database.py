"""базовая кофигурация для работы с БД"""#pylint: disable=E0401, E0611, R0903
import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from shared.config.base import settings


logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    """объявление базового класса БД"""

# Создаем engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # Для разработки, в продакшене False
    pool_size=5,
    max_overflow=10
)

# Создаем фабрику сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_db():
    """Зависимость для получения сессии БД"""
    async with AsyncSessionLocal() as async_session:
        yield async_session
