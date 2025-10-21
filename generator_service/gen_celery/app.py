# celery/app.py
"""Инициализация Celery приложения"""
from celery import Celery
from generator_service.gen_celery.config import CeleryConfig

# Создаем Celery приложение
app = Celery('generator_service')

# Загружаем конфигурацию
app.config_from_object(CeleryConfig)

# Автоматически обнаруживаем задачи в папке celery/tasks
app.autodiscover_tasks(['celery.tasks'])
