"""апи для изменения ролей"""#pylint: disable=E0401, C0412, W0707
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.models.user import AuthUser
from auth_service.messaging.producers import UserProducer, get_producer
from auth_service.services.role_change_service import RoleChangeService
from auth_service.schemas.role_change import (
    RoleChangeRequestCreate,
    RoleChangeRequestResponse,
    RoleChangeRequestList
)
from auth_service.core.auth import get_current_user
from shared.database.database import get_db

REQUIRED_ROLE_FOR_REVIEW = 2
router = APIRouter()

@router.post("/request", status_code=status.HTTP_201_CREATED)
async def create_role_change_request(
    request_data: RoleChangeRequestCreate,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user),
    producer: UserProducer = Depends(get_producer)
):
    """Создание заявки на изменение роли"""
    role_change_service = RoleChangeService(db, producer)

    try:
        request = await role_change_service.create_role_change_request(current_user.username,
                                                                        request_data)

        return RoleChangeRequestResponse(
            id=request.id,
            username=request.username,
            current_role=request.current_role,
            requested_role=request.requested_role,
            status=request.status,
            reason=request.reason,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/requests", response_model=RoleChangeRequestList)
async def get_pending_requests(
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user),
    producer: UserProducer = Depends(get_producer)
):
    """Получение списка pending заявок (только для пользователей с достаточными правами)"""
    if current_user.role < REQUIRED_ROLE_FOR_REVIEW:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    role_change_service = RoleChangeService(db, producer)

    requests = await role_change_service.get_pending_requests()

    # Формируем ответ с username'ами
    response_requests = []
    for req in requests:

        response_requests.append(RoleChangeRequestResponse(
            id=req.id,
            username=req.username,
            current_role=req.current_role,
            requested_role=req.requested_role,
            status=req.status,
            reason=req.reason,
        ))

    return RoleChangeRequestList(
        requests=response_requests,
        total=len(response_requests)
    )

@router.post("/{request_id}/approve")
async def approve_role_change_request(
    request_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user),
    producer: UserProducer = Depends(get_producer)
):
    """Одобрение заявки на изменение роли"""
    role_change_service = RoleChangeService(db, producer)

    if current_user.role != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN
        )

    result = await role_change_service.approve_request(request_id)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )

    return {"success": True, "message": result["message"]}

@router.post("/{request_id}/reject")
async def reject_role_change_request(
    request_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user),
    producer: UserProducer = Depends(get_producer)
):
    """Отклонение заявки на изменение роли"""
    role_change_service = RoleChangeService(db, producer)

    if current_user.role != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN
        )

    result = await role_change_service.reject_request(request_id)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )

    return {"success": True, "message": result["message"]}
