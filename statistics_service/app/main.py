import os
import sys
from fastapi import FastAPI

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from statistics_service.api.statistics import router as statistics_router


# Создание FastAPI приложения с lifespan
app = FastAPI(
    title="Statistics Service API",
    description="Микросервис для статистического анализа бинарных последовательностей",
    version="1.0.0",
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
