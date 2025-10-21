from contextlib import asynccontextmanager
import os
import sys
from sqlalchemy import text
from fastapi import FastAPI

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.database.database import get_db
from statistics_service.api.statistics import router as statistics_router


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # Startup
    print("Starting application...")
    
    # Инициализация подключения к БД
    try:
        # Проверяем подключение к БД
        async for db in get_db():
            # Выполняем простой запрос для проверки подключения
            await db.execute(text("SELECT 1"))
            print("✅ Database connection established")
            break
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        raise
    
    yield
    
    # Shutdown
    print("Application shutting down...")

# Создание FastAPI приложения с lifespan
app = FastAPI(
    title="Statistics Service API",
    description="Микросервис для статистического анализа бинарных последовательностей",
    version="1.0.0",
    lifespan=app_lifespan
)

# Подключаем роутеры
app.include_router(statistics_router)

# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint для мониторинга состояния сервиса
    """
    return {
        "status": "healthy",
        "service": "statistics-service",
        "version": "1.0.0"
    }
