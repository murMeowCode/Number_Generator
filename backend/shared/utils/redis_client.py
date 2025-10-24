# services/redis_service.py
from functools import wraps
import json
import redis
from typing import Callable, Optional, Any, Dict
from uuid import UUID
import logging
from shared.config.base import settings

logger = logging.getLogger(__name__)

class RedisCacheService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB_CACHE,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True
        )
        self.cache_ttl = 1800  # 30 минут в секундах

    def _get_cache_key_stat(self, sequence_id: UUID) -> str:
        return f"statistics:{sequence_id}"

    # Базовые методы для работы с произвольными ключами
    async def get(self, key: str) -> Optional[str]:
        """Получить значение по ключу"""
        try:
            return self.redis_client.get(key)
        except redis.RedisError as e:
            logger.warning(f"Redis error when getting key {key}: {str(e)}")
            return None

    async def setex(self, key: str, ttl: int, value: str) -> bool:
        """Сохранить значение с TTL"""
        try:
            result = self.redis_client.setex(key, ttl, value)
            return bool(result)
        except redis.RedisError as e:
            logger.error(f"Redis error when setting key {key}: {str(e)}")
            return False

    async def delete(self, key: str) -> int:
        """Удалить ключ"""
        try:
            return self.redis_client.delete(key)
        except redis.RedisError as e:
            logger.error(f"Redis error when deleting key {key}: {str(e)}")
            return 0

    # Специфичные методы для статистики
    async def get_cached_statistics(self, sequence_id: UUID) -> Optional[Dict[str, Any]]:
        """Получить статистику из кэша по ID"""
        try:
            cache_key = self._get_cache_key_stat(sequence_id)
            cached_data = self.redis_client.get(cache_key)
            
            if cached_data:
                logger.info(f"Cache hit for statistics_id: {sequence_id}")
                return json.loads(cached_data)
            return None
                
        except (redis.RedisError, json.JSONDecodeError) as e:
            logger.warning(f"Redis error when getting cache for {sequence_id}: {str(e)}")
            return None

    async def set_cached_statistics(self, sequence_id: UUID, data: Dict[str, Any]) -> bool:
        """Сохранить статистику в кэш"""
        try:
            cache_key = self._get_cache_key_stat(sequence_id)
            serialized_data = json.dumps(data, default=str)
            
            result = self.redis_client.setex(cache_key, self.cache_ttl, serialized_data)
            
            if result:
                logger.info(f"Successfully cached statistics for {sequence_id}")
            return bool(result)
            
        except (redis.RedisError, TypeError, ValueError) as e:
            logger.error(f"Redis error when setting cache for {sequence_id}: {str(e)}")
            return False

    async def delete_cached_statistics(self, sequence_id: UUID) -> bool:
        """Удалить статистику из кэша"""
        try:
            cache_key = self._get_cache_key_stat(sequence_id)
            result = self.redis_client.delete(cache_key)
            
            if result:
                logger.info(f"Successfully deleted cache for {sequence_id}")
            return bool(result)
            
        except redis.RedisError as e:
            logger.error(f"Redis error when deleting cache for {sequence_id}: {str(e)}")
            return False

# Создаем глобальный экземпляр сервиса
redis_cache = RedisCacheService()

async def get_redis_cache():
    return redis_cache

def cache_statistics(
    key_param: str = "sequence_id",
    ttl: int = 1800
):
    """
    Декоратор для кэширования результатов эндпоинтов статистики
    
    Args:
        key_param: Название параметра, содержащего statistics_id
        ttl: Время жизни кэша в секундах
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # Извлекаем statistics_id из параметров
            sequence_id = None
            
            # Ищем statistics_id в kwargs
            if key_param in kwargs:
                sequence_id = kwargs[key_param]
            # Или в args (по позиции)
            else:
                # Получаем сигнатуру функции для определения позиции параметра
                import inspect
                sig = inspect.signature(func)
                params = list(sig.parameters.keys())
                
                if key_param in params:
                    param_index = params.index(key_param)
                    if param_index < len(args):
                        sequence_id = args[param_index]
            
            if not sequence_id:
                print(f"Parameter {key_param} not found in function call")
                return await func(*args, **kwargs)
            
            # Пытаемся получить данные из кэша
            try:
                cached_data = await redis_cache.get_cached_statistics(sequence_id)
                if cached_data:
                    print(f"Cache hit for {key_param}: {sequence_id}")
                    return cached_data
            except Exception as e:
                print(f"Cache check failed for {sequence_id}: {str(e)}")
            
            # Если в кэше нет, выполняем функцию
            print(f"Cache miss for {key_param}: {sequence_id}")
            result = await func(*args, **kwargs)
            
            # Сохраняем результат в кэш
            try:
                if hasattr(result, 'dict'):
                    # Если это Pydantic модель
                    cache_data = result.dict()
                else:
                    # Если это уже dict
                    cache_data = result
                
                await redis_cache.set_cached_statistics(sequence_id, cache_data)
                print(f"Successfully cached result for {sequence_id}")
            except Exception as e:
                print(f"Failed to cache result for {sequence_id}: {str(e)}")
            
            return result
        
        return wrapper
    return decorator

def cache_dashboard(ttl: int = 300):
    """
    Декоратор для кэширования данных дашборда
    Использует фиксированный ключ 'dashboard:overview'
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = "dashboard:overview"
            
            # Пытаемся получить данные из кэша
            cached_data = await redis_cache.get(cache_key)
            if cached_data:
                logger.info(f"✅ ДАШБОРД - КЭШ-ПОПАДАНИЕ")
                return json.loads(cached_data)
            else:
                logger.info(f"❌ ДАШБОРД - КЭШ-ПРОМАХ")
            
            # Выполняем функцию, если данных нет в кэше
            result = await func(*args, **kwargs)
            
            # Сохраняем результат в кэш
            if result:
                serialized_data = json.dumps(
                    result.dict() if hasattr(result, 'dict') else result, 
                    default=str
                )
                success = await redis_cache.setex(cache_key, ttl, serialized_data)
                if success:
                    logger.info(f"💾 ДАННЫЕ ДАШБОРДА СОХРАНЕНЫ В КЭШ (TTL: {ttl}сек)")
                else:
                    logger.error("❌ НЕ УДАЛОСЬ СОХРАНИТЬ ДАННЫЕ ДАШБОРДА В КЭШ")
            
            return result
        return wrapper
    return decorator

async def invalidate_dashboard_cache():
    """
    Функция для инвалидации (очистки) кэша дашборда
    Вызывается при добавлении новых статистик
    """
    cache_key = "dashboard:overview"
    
    try:
        deleted_count = await redis_cache.delete(cache_key)
        if deleted_count > 0:
            logger.info("🗑️ КЭШ ДАШБОРДА УСПЕШНО ОЧИЩЕН")
            return True
        else:
            logger.info("ℹ️ КЭШ ДАШБОРДА УЖЕ БЫЛ ПУСТЫМ")
            return False
    except Exception as e:
        logger.error(f"❌ ОШИБКА ПРИ ОЧИСТКЕ КЭША ДАШБОРДА: {str(e)}")
        return False

def cache_generation_dashboard(ttl: int = 1800):
    """
    Декоратор для кэширования данных дашборда генераций
    Использует фиксированный ключ 'generation_dashboard'
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = "generation_dashboard"
            
            # Пытаемся получить данные из кэша
            cached_data = await redis_cache.get(cache_key)
            if cached_data:
                logger.info(f"✅ GENERATION DASHBOARD - КЭШ-ПОПАДАНИЕ")
                return json.loads(cached_data)
            else:
                logger.info(f"❌ GENERATION DASHBOARD - КЭШ-ПРОМАХ")
            
            # Выполняем функцию, если данных нет в кэше
            result = await func(*args, **kwargs)
            
            # Сохраняем результат в кэш
            if result:
                serialized_data = json.dumps(
                    [item.dict() if hasattr(item, 'dict') else item for item in result]
                    if isinstance(result, list) 
                    else result.dict() if hasattr(result, 'dict') else result, 
                    default=str
                )
                success = await redis_cache.setex(cache_key, ttl, serialized_data)
                if success:
                    logger.info(f"💾 ДАННЫЕ GENERATION DASHBOARD СОХРАНЕНЫ В КЭШ (TTL: {ttl}сек)")
                else:
                    logger.error("❌ НЕ УДАЛОСЬ СОХРАНИТЬ ДАННЫЕ GENERATION DASHBOARD В КЭШ")
            
            return result
        return wrapper
    return decorator

async def invalidate_generation_dashboard_cache():
    """
    Функция для инвалидации (очистки) кэша дашборда генераций
    Вызывается при добавлении новых генераций
    """
    cache_key = "generation_dashboard"
    
    try:
        deleted_count = await redis_cache.delete(cache_key)
        if deleted_count > 0:
            logger.info("🗑️ КЭШ GENERATION DASHBOARD УСПЕШНО ОЧИЩЕН")
            return True
        else:
            logger.info("ℹ️ КЭШ GENERATION DASHBOARD УЖЕ БЫЛ ПУСТЫМ")
            return False
    except Exception as e:
        logger.error(f"❌ ОШИБКА ПРИ ОЧИСТКЕ КЭША GENERATION DASHBOARD: {str(e)}")
        return False
