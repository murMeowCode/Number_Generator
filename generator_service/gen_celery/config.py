# celery/config.py
"""Конфигурация Celery для сервиса статистики"""
from shared.config.base import settings

class CeleryConfig:
    """Конфигурация Celery"""

    broker_url = settings.CELERY_BROKER_URL
    result_backend = settings.CELERY_RESULT_BACKEND

    # Настройки задач
    task_serializer = "json"
    result_serializer = "json"
    accept_content = ["json"]
    timezone = "Europe/Moscow"
    enable_utc = True

    # Настройки воркера
    worker_prefetch_multiplier = 1
    task_acks_late = True
    worker_max_tasks_per_child = 1000

    # Роутинг задач
    task_routes = {
        "celery.tasks.statistics_tasks.*": {"queue": "statistics_queue"},
    }
