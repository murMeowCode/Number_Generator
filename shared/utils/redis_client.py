"""
Redis клиент.
Предоставляет доступ к редис для кеширования и работы с Селери.
"""
from redis.asyncio import Redis
from shared.config.base import settings



class RedisManager:
    """Manager for Redis connections with async support."""

    def __init__(self):
        self.host = settings.REDIS_HOST
        self.port = settings.REDIS_PORT
        self.password = settings.REDIS_PASSWORD
        self._cache_client = None
        self._celery_client = None

    async def get_celery_client(self) -> Redis:
        """Get async Redis client for Celery."""
        if self._celery_client is None:
            self._celery_client = Redis(
                host=self.host,
                port=self.port,
                db=settings.REDIS_DB_CELERY,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True
            )
        return self._celery_client

    async def close_connections(self):
        """Close all Redis connections."""
        if self._cache_client:
            await self._cache_client.close()
        if self._celery_client:
            await self._celery_client.close()


# Global Redis manager instance
redis_manager = RedisManager()

async def get_celery_redis() -> Redis:
    """Dependency function to get Celery Redis client"""
    return await redis_manager.get_celery_client()

async def close_redis():
    """Close Redis connections on application shutdown."""
    await redis_manager.close_connections()
    print("✅ Redis connections closed")
