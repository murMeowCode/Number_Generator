"""Продюсер для пользовательских событий"""#pylint:disable=E0401, W1203
import logging

from fastapi import Request
from shared.messaging.producers import BaseProducer
from shared.schemas.messaging import UserCreatedMessage

logger = logging.getLogger(__name__)

class UserProducer(BaseProducer):
    """Продюсер для отправки событий связанных с пользователями"""

    async def send_user_created_event(self, message: UserCreatedMessage):
        """Отправляет событие создания пользователя"""
        await self._send_message(
            message=message,
            routing_key="auth.user.created"
        )
        logger.info(f"User created event sent for user_id: {message.user_id}")

async def get_producer(request: Request) -> UserProducer:
    """Функция для получения глобального продюсера"""
    return request.app.state.producer
