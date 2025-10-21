"""базовый модуль кролика"""
import aio_pika

class RabbitMQBase:
    """база для наследования"""
    def __init__(self, rabbitmq_url: str):
        self.rabbitmq_url = rabbitmq_url
        self.connection = None
        self.channel = None

    async def connect(self):
        """Установка соединения с RabbitMQ"""
        self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
        self.channel = await self.connection.channel()
        return self.channel

    async def close(self):
        """Закрытие соединения"""
        if self.connection:
            await self.connection.close()
