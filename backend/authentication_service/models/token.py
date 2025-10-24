"""модель токена"""#pylint: disable=E0401
import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from shared.database.database import Base

class RefreshToken(Base):
    """модель рефреш токена"""
    __tablename__ = "refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    token = Column(Text, nullable=False, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    def is_expired(self) -> bool:
        """проверка жизнеспособности токена"""
        return datetime.utcnow() > self.expires_at
