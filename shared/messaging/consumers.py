"""модуль потребителя"""#pylint: disable=W1203, E0401, W0718
import json
import logging
from abc import ABC, abstractmethod
from typing import Optional
import aio_pika
from shared.messaging.base import RabbitMQBase

logger = logging.getLogger(__name__)

class BaseConsumer(RabbitMQBase, ABC):
    """Базовый класс для всех потребителей RabbitMQ"""

    def __init__(self, rabbitmq_url: str, exchange_name: str = "auth_exchange"):
        super().__init__(rabbitmq_url)
        self.exchange_name = exchange_name
        self.exchange: Optional[aio_pika.Exchange] = None

    async def connect(self):
        """Базовое подключение к RabbitMQ и настройка exchange"""
        await super().connect()

        # Создаем/получаем exchange
        self.exchange = await self.channel.declare_exchange(
            name=self.exchange_name,
            type=aio_pika.ExchangeType.TOPIC,
            durable=True
        )

        # Настраиваем конкретного потребителя
        await self.setup_queues()

    @abstractmethod
    async def setup_queues(self):
        """Абстрактный метод для настройки очередей (реализуется в потомках)"""

    async def declare_and_bind_queue(self, queue_name: str, routing_key: str):
        """Вспомогательный метод для объявления и привязки очереди"""
        queue = await self.channel.declare_queue(
            name=queue_name,
            durable=True
        )
        await queue.bind(self.exchange, routing_key=routing_key)
        return queue

    async def process_message(self, message: aio_pika.IncomingMessage, handler_func) -> bool:
        """Базовый обработчик сообщений с обработкой ошибок"""
        async with message.process():
            try:
                await handler_func(message)
                return True
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error in {handler_func.__name__}: {e}")
            except Exception as e:
                logger.error(f"Error in {handler_func.__name__}: {e}")
                logger.exception("Detailed exception:")
            return False
