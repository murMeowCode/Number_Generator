"""модель аутентифицированного пользователя"""
# pylint: disable=E0401
import uuid
from sqlalchemy import Column, String, DateTime, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from shared.database.database import Base

class AuthUser(Base):
    """модель аутентифицированного пользователя"""
    __tablename__ = "auth_users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    surname = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    fathername = Column(String(50), nullable=True)  # Отчество может быть не у всех
    birth_date = Column(Date, nullable=True)  # Правильно указано поле даты рождения
    hashed_password = Column(String(255), nullable=True)
    last_login = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<AuthUser {self.username}>"
