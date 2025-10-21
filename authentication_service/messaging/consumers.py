"""модуль потребителя"""#pylint: disable=W1203, E0401, W0718
import json
import logging
from datetime import datetime
import aio_pika
from shared.messaging.consumers import BaseConsumer
from shared.messaging.producers import AuthProducer
from shared.schemas.messaging import (
    BaseMessage, MessageType,
    TokenVerifyMessage
)
from auth_service.services.auth_service import AuthService

logger = logging.getLogger(__name__)

class AuthConsumer(BaseConsumer):
    """Потребитель для обработки событий аутентификации"""

    def __init__(self, rabbitmq_url: str, auth_service: AuthService, producer: AuthProducer):
        super().__init__(rabbitmq_url, "auth_exchange")
        self.auth_service = auth_service
        self.producer = producer

    async def setup_queues(self):
        """Настройка очередей для событий аутентификации"""
        # Очередь для верификации токенов
        verify_queue = await self.declare_and_bind_queue(
            queue_name="auth.verify.request",
            routing_key="auth.verify.request"
        )
        await verify_queue.consume(
            lambda msg: self.process_message(msg, self._handle_verify_request)
        )

    async def _handle_verify_request(self, message: aio_pika.IncomingMessage):
        """Обработка запроса верификации токена"""
        start_time = datetime.utcnow()
        message_id = message.correlation_id or f"msg_{start_time.timestamp()}"

        # Декодирование сообщения
        body = json.loads(message.body.decode())
        base_message = BaseMessage(**body)

        if base_message.message_type != MessageType.TOKEN_VERIFY_REQUEST:
            logger.warning(f"Unexpected message type: {base_message.message_type}")
            return

        # Обработка верификации токена
        verify_message = TokenVerifyMessage(**base_message.data)
        response = await self.auth_service.verify_token_handler(verify_message)

        # Подготовка и отправка ответа
        response_message = BaseMessage(
            message_type=MessageType.TOKEN_VERIFY_RESPONSE,
            data=response.model_dump()
        )

        if base_message.reply_to:
            await self.producer.send_response(
                response_message,
                base_message.reply_to,
                base_message.correlation_id
            )
            logger.info(f"✅ Token verification response sent for message {message_id}")
        else:
            logger.warning(f"⚠️ No reply queue specified for message {message_id}")
