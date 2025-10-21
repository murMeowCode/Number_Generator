"""главный файл сервиса"""#pylint: disable=C0413
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
from shared.utils.redis_client import RedisManager

@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Lifespan менеджер для управления жизненным циклом приложения
    """
    # Startup
    print("🚀 Starting Generator Service...")

    redis_manager = RedisManager()
    redis_client =  await redis_manager.get_celery_client()
    file_service = FileService()
    auth_producer = AuthProducer(settings.RABBITMQ_URL)

    try:
        ping_result = await redis_client.ping()
        print(f"✅ Redis подключен успешно. Ping: {ping_result}")
    except Exception as e:
        print(f"❌ Ошибка подключения к Redis: {e}")
        raise

    # Инициализация MinIO
    try:
        await file_service.init_minio()
        print("✅ MinIO initialized successfully")
    except Exception as e:
        print(f"❌ MinIO initialization failed: {e}")
        raise

    # Инициализация RabbitMQ producer
    await auth_producer.connect()
    print("✅ RabbitMQ producer подключен")

    print("✅ Generator Service started successfully")

    yield  # Здесь приложение работает

    # Shutdown
    print("🛑 Shutting down Generator Service...")

app = FastAPI(
    title="Generator Service",
    description="Сервис генерации случайных последовательностей и статистического тестирования",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
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
