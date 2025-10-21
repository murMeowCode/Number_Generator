"""схемы смены ролей"""
from typing import Optional
import uuid
from enum import Enum
from pydantic import BaseModel

class RoleChangeStatus(str, Enum):
    """перечисление статусов заявок"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class RoleChangeRequestCreate(BaseModel):
    """схема запроса на изменение роли"""
    requested_role: int
    reason: Optional[str] = None

class RoleChangeRequestResponse(BaseModel):
    """ответ на запрос"""
    id: uuid.UUID
    username: str
    current_role: int
    requested_role: int
    status: RoleChangeStatus
    reason: Optional[str]

    class Config:
        """переключение в режим ORM"""
        from_attributes = True

class RoleChangeRequestUpdate(BaseModel):
    """изменение роли"""
    status: RoleChangeStatus

class RoleChangeRequestList(BaseModel):
    """список запросов на изменение роли"""
    requests: list[RoleChangeRequestResponse]
    total: int
