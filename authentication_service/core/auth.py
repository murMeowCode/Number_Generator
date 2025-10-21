"""функции для получения информации о пользователе из заголовка"""#pylint: disable=E0401
import logging
from shared.database.database import get_db
from auth_service.services.user_service import UserService
from auth_service.services.token_service import TokenService
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

security = HTTPBearer()


logger = logging.getLogger(__name__)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """получение пользователя из заголовка """
    logger.info(
        "Начало аутентификации пользователя по токену",
        extra={"token_length": len(credentials.credentials) if credentials.credentials else 0}
    )

    token_service = TokenService(db)

    # Валидируем access token
    logger.debug("Валидация access токена")
    result = await token_service.verify_access_token(credentials.credentials)

    # Логируем результат валидации токена
    logger.info(
        "Результат валидации токена",
        extra={
            "validation_success": result.get("valid", False),
            "user_id": result.get("user_id"),
            "username": result.get("username"),
            "error": result.get("error")
        }
    )

    if not result["valid"]:
        logger.warning(
            "Неуспешная валидация токена",
            extra={
                "error": result.get("error"),
                "token_preview": credentials.credentials[:20] + "..." if credentials.credentials 
                else "None"
            }
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result.get("error", "Invalid token")
        )

    logger.debug(
        "Токен успешно валидирован, поиск пользователя в БД",
        extra={"user_id": result["user_id"]}
    )

    user_service = UserService(db)
    user = await user_service.get_user_by_id(result["user_id"])

    # Логируем результат поиска пользователя
    logger.info(
        "Результат поиска пользователя",
        extra={
            "user_found": user is not None,
            "user_id": result["user_id"],
            "user_email": getattr(user, 'email', None) if user else None,
            "user_active": getattr(user, 'is_active', None) if user else None
        }
    )

    if not user:
        logger.error(
            "Пользователь не найден в БД",
            extra={
                "user_id": result["user_id"],
                "username": result.get("username")
            }
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    logger.info(
        "Успешная аутентификация пользователя",
        extra={
            "user_id": user.id,
            "email": getattr(user, 'email', 'N/A'),
            "username": getattr(user, 'username', 'N/A')
        }
    )

    return user
