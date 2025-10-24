"""главный файл сервиса"""
#pylint: disable=C0413
import sys
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from generator_service.api.generation import router
from generator_service.services.file_service import FileService
from shared.config.base import settings
from shared.messaging.producers import AuthProducer

@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Lifespan менеджер для управления жизненным циклом приложения
    """
    file_service = FileService()
    auth_producer = AuthProducer(settings.RABBITMQ_URL)

    try:
        await file_service.init_minio()
    except Exception as e:
        raise

    await auth_producer.connect()

    yield

app = FastAPI(
    title="Generator Service",
    description="Сервис генерации случайных последовательностей и статистического тестирования",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/health")
async def health_check():
    """
    Health check эндпоинт для мониторинга
    """
    return {
        "status": "healthy",
        "service": "generator",
        "version": "1.0.0"
    }
