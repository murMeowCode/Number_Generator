"""Модель генерации для базы данных"""
# pylint: disable=E0401
import uuid
from shared.database.database import Base
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from shared.database.database import Base


class Generation(Base):
    """
    Модель для хранения результатов генерации последовательностей в SQLAlchemy.
    """
    __tablename__ = "generations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    length = Column(Integer, nullable=False)
    seed = Column(String(255), nullable=True)
    initial_fill = Column(String(255), nullable=False)
    sequence = Column(Text, nullable=False)
    file_url = Column(String(500), nullable=True)
    winer = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Generation(id={self.id}, length={self.length})>"
