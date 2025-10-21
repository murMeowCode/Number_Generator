"""основной файл сервиса"""#pylint: disable=E0401, W0621, C0413, C0411
from contextlib import asynccontextmanager
import sys
import os
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.config.base import settings
from shared.database.database import AsyncSessionLocal
from shared.messaging.producers import AuthProducer
from authentication_service.api.endpoints import auth
from authentication_service.services.auth_service import AuthService
from authentication_service.services.token_service import TokenService
from authentication_service.services.user_service import UserService
from authentication_service.messaging.consumers import AuthConsumer
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """инициализация служб при запуске"""
    # Инициализация RabbitMQ producer
    producer = AuthProducer(settings.RABBITMQ_URL)
    await producer.connect()
    print("✅ RabbitMQ producer подключен")

    # Сохраняем producer в состоянии приложения
    app.state.producer = producer

    # Инициализация RabbitMQ consumer
    async with AsyncSessionLocal() as db:
        token_service = TokenService(db)
        print("✅ Служба токенов запущена")
        user_service = UserService(db)
        print("✅ Служба пользователей запущена")
        authentication_service = AuthService(token_service, user_service)
        print("✅ Служба аутентификации запущена")
        consumer = AuthConsumer(settings.RABBITMQ_URL, authentication_service, producer)
        await consumer.connect()
        print("✅ RabbitMQ consumer подключен")

    yield

    # Shutdown
    await producer.close()
    await consumer.close()


app = FastAPI(
    title="Auth Service",
    description="Microservice for JWT token management",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить ВСЕ origins (любой домен)
    allow_credentials=True,  # Разрешить cookies/токены
    allow_methods=["*"],  # Разрешить ВСЕ методы (GET, POST, PUT, DELETE, OPTIONS и т.д.)
    allow_headers=["*"],  # Разрешить ВСЕ заголовки
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/health")
async def health_check():
    """апи для проверки работоспособности сервиса"""
    return {"status": "healthy", "service": "authentication_service"}
