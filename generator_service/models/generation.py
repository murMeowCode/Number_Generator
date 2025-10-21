"""Модель генерации для базы данных"""
import uuid
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from shared.database.database import Base


class Generation(Base):
    """
    Модель для хранения информации о генерациях случайных последовательностей.
    
    Attributes:
        id (UUID): Уникальный идентификатор генерации
        user_id (UUID): Идентификатор пользователя, создавшего генерацию
        length (int): Длина сгенерированной последовательности в битах
        seed (str): Начальное значение (seed) для генератора
        minio_json_path (str): Путь к JSON файлу с результатами в MinIO
        preview (str): Преview первых 10 символов последовательности
        created_at (DateTime): Дата и время создания генерации
        test_results (JSON): Результаты статистических тестов в формате JSON
    """
    __tablename__ = "generations"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PGUUID(as_uuid=True), nullable=True)
    length = Column(Integer, nullable=False)
    seed = Column(String, nullable=True)
    minio_json_path = Column(String, nullable=False)
    preview = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    test_results = Column(JSON, nullable=True)
