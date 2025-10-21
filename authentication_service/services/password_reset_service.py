"""Сервис сброса пароля для обработки запросов и валидации сброса паролей."""
import secrets
from datetime import datetime, timedelta
from typing import Dict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from auth_service.core.security import get_password_hash
from auth_service.messaging.producers import UserProducer
from auth_service.models.password_reset_token import PasswordResetToken
from auth_service.models.user import AuthUser

class PasswordResetService:
    """Класс сервиса для управления функциональностью сброса пароля."""

    def __init__(self, db: AsyncSession, producer: UserProducer = None):
        """Инициализация сервиса сброса пароля с сессией базы данных и опциональным продюсером."""
        self.db = db
        self.producer = producer

    async def request_password_reset(self, email: str) -> Dict[str, str]:
        """Запрос сброса пароля: генерация токена и отправка email-уведомления."""
        # Поиск пользователя по email
        result = await self.db.execute(
            select(AuthUser).where(AuthUser.email == email)
        )
        user = result.scalar_one_or_none()
        if not user:
            return {"success": "False", "error": "Пользователь с таким email не найден"}

        # Генерация уникального токена сброса
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=5)  # Токен действителен 1 час

        # Сохранение токена в БД
        reset_token = PasswordResetToken(
            user_id=user.id,
            token=token,
            expires_at=expires_at
        )
        self.db.add(reset_token)
        await self.db.commit()

        # Отправка email через продюсер
        if self.producer:
            await self.producer.send_notification({
                "type": "password_reset",
                "user_email": email,
                "user_id": str(user.id),
                "data": {
                    "reset_token": token,
                    "reset_link": f"https://yourapp.com/reset-password?token={token}"
                }
            })

        return {"success": "True", "message": "Инструкции по сбросу пароля отправлены на email"}

    async def reset_password(self, token: str, new_password: str) -> Dict[str, str]:
        """Сброс пароля: валидация токена и обновление пароля пользователя."""
        # Поиск токена в БД
        result = await self.db.execute(
            select(PasswordResetToken).where(PasswordResetToken.token == token)
        )
        reset_token = result.scalar_one_or_none()
        if not reset_token:
            return {"success": "False", "message": "Неверный или истекший токен"}

        # Проверка срока действия
        if datetime.utcnow() > reset_token.expires_at:
            await self.db.delete(reset_token)
            await self.db.commit()
            return {"success": "False", "message": "Токен истек"}

        # Обновление пароля пользователя
        result = await self.db.execute(
            select(AuthUser).where(AuthUser.id == reset_token.user_id)
        )
        user = result.scalars().first()
        if not user:
            return {"success": "False", "message": "Пользователь не найден"}

        user.hashed_password = get_password_hash(new_password)
        await self.db.commit()

        # Удаление токена после использования для безопасности
        await self.db.delete(reset_token)
        await self.db.commit()

        return {"success": "True", "message": "Пароль успешно сброшен"}
