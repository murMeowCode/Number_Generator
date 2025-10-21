"""служба токенов"""#pylint: disable=E0611, E0401, C0121, W0718
from datetime import datetime, timedelta
import uuid
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from auth_service.models.token import RefreshToken
from auth_service.core.security import create_access_token, create_refresh_token, verify_token
from shared.config.base import settings

# Настройка логгера
logger = logging.getLogger(__name__)

class TokenService:
    """класс службы токенов"""

    def __init__(self, db: AsyncSession):
        self.db = db
        logger.debug("Инициализирован TokenService для сессии БД")

    async def create_token_pair(self, user_id: str, username: str) -> dict:
        """Создание пары access/refresh токенов"""
        logger.info(
            "Создание пары токенов для пользователя",
            extra={"user_id": user_id, "username": username}
        )

        try:
            # Создаем access token
            access_token = create_access_token(
                data={"sub": user_id, "username": username}
            )
            logger.debug("Access токен создан успешно")

            # Создаем refresh token
            refresh_token_data = {"sub": user_id, "token_id": str(uuid.uuid4())}
            refresh_token = create_refresh_token(refresh_token_data)
            logger.debug("Refresh токен создан успешно",
                         extra={"token_id": refresh_token_data["token_id"]})

            # Сохраняем refresh token в БД
            expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
            db_refresh_token = RefreshToken(
                user_id=uuid.UUID(user_id),
                token=refresh_token,
                expires_at=expires_at
            )

            self.db.add(db_refresh_token)
            await self.db.commit()
            await self.db.refresh(db_refresh_token)

            logger.info(
                "Пара токенов успешно создана и сохранена",
                extra={
                    "user_id": user_id,
                    "token_id": db_refresh_token.id,
                    "expires_at": expires_at.isoformat()
                }
            )

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }

        except Exception as e:
            logger.error(
                "Ошибка при создании пары токенов",
                extra={"user_id": user_id, "error": str(e)},
                exc_info=True
            )
            raise

    async def verify_access_token(self, token: str) -> dict:
        """Проверка access token"""
        logger.debug("Проверка access токена")

        try:
            payload = verify_token(token)
            if not payload:
                logger.warning("Невалидный токен: верификация не пройдена")
                return {"valid": False, "error": "Invalid token"}

            token_type = payload.get("type")
            if token_type != "access":
                logger.warning(
                    "Неверный тип токена",
                    extra={"expected": "access", "actual": token_type}
                )
                return {"valid": False, "error": "Not an access token"}

            user_id = payload.get("sub")
            username = payload.get("username")

            logger.info(
                "Access токен успешно верифицирован",
                extra={"user_id": user_id, "username": username}
            )

            return {
                "valid": True, 
                "user_id": user_id,
                "username": username
            }

        except Exception as e:
            logger.error(
                "Ошибка при верификации access токена",
                extra={"error": str(e)},
                exc_info=True
            )
            return {"valid": False, "error": "Token verification error"}

    async def refresh_tokens(self, refresh_token: str) -> dict:
        """Обновление пары токенов"""
        logger.info("Запрос на обновление пары токенов")

        try:
            # Проверяем refresh token
            payload = verify_token(refresh_token)
            if not payload:
                logger.warning("Невалидный refresh токен")
                return {"success": False, "error": "Invalid refresh token"}

            token_type = payload.get("type")
            if token_type != "refresh":
                logger.warning(
                    "Получен токен неверного типа для обновления",
                    extra={"expected": "refresh", "actual": token_type}
                )
                return {"success": False, "error": "Not a refresh token"}

            token_id = payload.get("token_id")
            user_id = payload.get("sub")

            logger.debug(
                "Поиск refresh токена в БД",
                extra={"token_id": token_id, "user_id": user_id}
            )

            # Проверяем наличие в БД
            stmt = select(RefreshToken).where(
                RefreshToken.token == refresh_token,
                RefreshToken.is_active == True
            )
            result = await self.db.execute(stmt)
            db_token = result.scalar_one_or_none()

            if not db_token:
                logger.warning("Refresh токен не найден в БД или не активен")
                return {"success": False, "error": "Refresh token expired or revoked"}

            if db_token.is_expired():
                logger.warning(
                    "Refresh токен просрочен",
                    extra={"expires_at": db_token.expires_at.isoformat()}
                )
                return {"success": False, "error": "Refresh token expired or revoked"}

            # Деактивируем старый токен
            db_token.is_active = False
            await self.db.commit()

            logger.info(
                "Старый refresh токен деактивирован",
                extra={"token_id": db_token.id, "user_id": user_id}
            )

            # Создаем новую пару токенов
            new_tokens = await self.create_token_pair(user_id, "")

            logger.info(
                "Пара токенов успешно обновлена",
                extra={"user_id": user_id, "old_token_id": db_token.id}
            )

            return {
                "success": True,
                "tokens": new_tokens
            }

        except Exception as e:
            logger.error(
                "Ошибка при обновлении токенов",
                extra={"error": str(e)},
                exc_info=True
            )
            return {"success": False, "error": "Token refresh error"}

    async def cleanup_expired_tokens(self):
        """Очистка просроченных токенов"""
        logger.info("Запуск очистки просроченных токенов")

        try:
            stmt = delete(RefreshToken).where(
                RefreshToken.expires_at < datetime.utcnow()
            )
            result = await self.db.execute(stmt)
            deleted_count = result.rowcount
            await self.db.commit()

            if deleted_count > 0:
                logger.info(
                    "Очистка просроченных токенов завершена",
                    extra={"deleted_tokens_count": deleted_count}
                )
            else:
                logger.debug("Просроченные токены для очистки не найдены")

        except Exception as e:
            logger.error(
                "Ошибка при очистке просроченных токенов",
                extra={"error": str(e)},
                exc_info=True
            )
            raise

    async def revoke_user_tokens(self, user_id: str) -> int:
        """Отзыв всех токенов пользователя"""
        logger.info(
            "Отзыв всех токенов пользователя",
            extra={"user_id": user_id}
        )

        try:
            stmt = delete(RefreshToken).where(
                RefreshToken.user_id == uuid.UUID(user_id)
            )
            result = await self.db.execute(stmt)
            revoked_count = result.rowcount
            await self.db.commit()

            logger.info(
                "Токены пользователя отозваны",
                extra={"user_id": user_id, "revoked_tokens_count": revoked_count}
            )

            return revoked_count

        except Exception as e:
            logger.error(
                "Ошибка при отзыве токенов пользователя",
                extra={"user_id": user_id, "error": str(e)},
                exc_info=True
            )
            raise
