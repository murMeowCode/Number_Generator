"""модель запроса """#pylint: disable=E0401
import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from shared.database.database import Base


class RoleChangeRequest(Base):
    """модель запроса на изменение роли"""
    __tablename__ = "role_change_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, ForeignKey("auth_users.username"), nullable=False)
    requested_role = Column(Integer, nullable=False)
    current_role = Column(Integer, nullable=False)
    status = Column(String(20), default="pending")  # pending, approved, rejected
    reason = Column(Text, nullable=True)  # причина запроса

    # Relationships
    user = relationship("AuthUser", foreign_keys=[username], backref="role_change_requests")

    def __repr__(self):
        return f"<RoleChangeRequest {self.username} -> {self.requested_role}>"
