"""модель аутентифицированного пользователя"""#pylint: disable=E0401
import uuid
from sqlalchemy import Column, String, DateTime, Integer, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from shared.database.database import Base

class AuthUser(Base):
    """модель"""
    __tablename__ = "auth_users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    role = Column(Integer,nullable = False)
    hashed_password = Column(String(255), nullable=True)
    last_login = Column(DateTime, nullable=True)
    password_reset_tokens = relationship("PasswordResetToken", back_populates="user")

    vk_id = Column(BigInteger, unique=True, nullable=True, index=True)
    oauth_provider = Column(String(20), nullable=True)
    yandex_id = Column(String, unique=True, nullable=True, index=True)

    def __repr__(self):
        return f"<AuthUser {self.username}>"

    @property
    def is_oauth_user(self):
        """property checking"""
        return (self.vk_id is not None
                or self.yandex_id is not None) and self.hashed_password is None
