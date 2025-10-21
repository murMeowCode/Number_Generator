"""Таблица generations"""
from datetime import datetime
from pydantic import BaseModel, Field
from sqlalchemy import UUID

class Generation(BaseModel):
    """Модель пользовательской генерации"""
    id: UUID = Field(primary_key=True)
    user_id: UUID = Field(nullable=True)
    length: int = Field()  # длина последовательности
    seed: str = Field(nullable=True)  # начальное заполнение (пока пустое)
    minio_json_path: str = Field()  # путь к JSON в MinIO
    preview: str = Field()  # первые 10 символов
    created_at: datetime = Field(default=datetime.utcnow())
    test_results: dict = Field()
