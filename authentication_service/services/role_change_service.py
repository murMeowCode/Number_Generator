"""сервис смены ролей"""#pylint: disable=E0611, E0401
import uuid
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from auth_service.models.user import AuthUser
from auth_service.models.role_change_request import RoleChangeRequest
from auth_service.schemas.role_change import RoleChangeRequestCreate, RoleChangeStatus
from auth_service.messaging.producers import UserProducer

class RoleChangeService:
    """класс сервиса"""
    def __init__(self, db: AsyncSession, producer: UserProducer):
        self.producer = producer
        self.db = db

    async def create_role_change_request(self, username: str,
        request_data: RoleChangeRequestCreate) -> RoleChangeRequest:
        """Создание заявки на изменение роли"""
        # Получаем пользователя
        stmt = select(AuthUser).where(AuthUser.username == username)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise ValueError("User not found")

        # Проверяем, что запрашиваемая роль отличается от текущей
        if user.role == request_data.requested_role:
            raise ValueError("Requested role is the same as current role")

        # Проверяем, есть ли уже pending заявка у пользователя
        existing_pending_stmt = select(RoleChangeRequest).where(
            and_(
                RoleChangeRequest.username == username,
                RoleChangeRequest.status == RoleChangeStatus.PENDING
            )
        )
        existing_pending = await self.db.execute(existing_pending_stmt)
        if existing_pending.scalar_one_or_none():
            raise ValueError("User already has a pending role change request")

        # Создаем заявку
        role_request = RoleChangeRequest(
            username=username,
            current_role=user.role,
            requested_role=request_data.requested_role,
            reason=request_data.reason,
            status=RoleChangeStatus.PENDING
        )

        self.db.add(role_request)
        await self.db.commit()
        await self.db.refresh(role_request)

        return role_request

    async def get_pending_requests(self) -> List[RoleChangeRequest]:
        """Получение списка pending заявок"""
        stmt = select(RoleChangeRequest).where(
            RoleChangeRequest.status == RoleChangeStatus.PENDING
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_request_by_id(self, request_id: uuid.UUID) -> Optional[RoleChangeRequest]:
        """Получение заявки по ID"""
        return await self.db.get(RoleChangeRequest, request_id)

    async def approve_request(self, request_id: uuid.UUID) -> Dict:
        """Одобрение заявки на изменение роли"""
        role_request = await self.get_request_by_id(request_id)
        if not role_request:
            return {"success": False, "error": "Request not found"}

        if role_request.status != RoleChangeStatus.PENDING:
            return {"success": False, "error": "Request is not pending"}

        # Получаем пользователя
        stmt = select(AuthUser).where(AuthUser.username == role_request.username)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            return {"success": False, "error": "User not found"}

        # Обновляем роль пользователя
        user.role = role_request.requested_role

        # Обновляем заявку
        role_request.status = RoleChangeStatus.APPROVED

        await self.db.commit()

        await self.producer.send_notification({
                "type": "role_approved",
                "username": user.username,
                "user_email": user.email,
                "user_id": str(user.id)
            })

        return {
            "success": True, 
            "message": f"Role changed to {role_request.requested_role}"
        }

    async def reject_request(self, request_id: uuid.UUID) -> Dict:
        """Отклонение заявки на изменение роли"""
        role_request = await self.get_request_by_id(request_id)
        if not role_request:
            return {"success": False, "error": "Request not found"}

        if role_request.status != RoleChangeStatus.PENDING:
            return {"success": False, "error": "Request is not pending"}

        # Обновляем заявку
        role_request.status = RoleChangeStatus.REJECTED

        await self.db.commit()

        stmt = select(AuthUser).where(AuthUser.username == role_request.username)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        await self.producer.send_notification({
                "type": "role_rejected",
                "username": user.username,
                "user_email": user.email,
                "user_id": str(user.id)
            })

        return {"success": True, "message": "Request rejected"}
