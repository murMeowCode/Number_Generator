"""служба верификации токенов с возвращением роли"""
# pylint: disable=E0611, E0401, W1203, W0718
import logging
from auth_service.services.token_service import TokenService
from auth_service.services.user_service import UserService
from shared.schemas.messaging import (
    TokenVerifyMessage,
    TokenVerifyResponseMessage
)

logger = logging.getLogger(__name__)

class AuthService:
    """класс обработки сообщений верификации"""
    def __init__(self, token_service: TokenService, user_service: UserService):
        self.token_service = token_service
        self.user_service = user_service

    async def verify_token_handler(self, message: TokenVerifyMessage) -> TokenVerifyResponseMessage:
        """Обработчик верификации токена"""
        logger.info(f"Starting token verification for token: {message.token[:10]}...")

        try:
            # Верифицируем токен
            result = await self.token_service.verify_access_token(message.token)
            logger.debug(f"Token verification result: {result}")

            if not result["valid"]:
                logger.warning(f"Token verification failed: {result.get('error')}")
                return TokenVerifyResponseMessage(
                    valid=False,
                    user_id=None,
                    error=result.get("error"),
                    role=None
                )

            user_id = result.get("user_id")
            logger.info(f"Token valid for user_id: {user_id}")

            # Получаем пользователя и его роль
            user = await self.user_service.get_user_by_id(user_id)

            if not user:
                logger.error(f"User not found for user_id: {user_id}")
                return TokenVerifyResponseMessage(
                    valid=False,
                    user_id=user_id,
                    error="User not found",
                    role=None
                )

            role = user.role
            logger.info(f"User role retrieved: {role} for user_id: {user_id}")

            response = TokenVerifyResponseMessage(
                valid=True,
                user_id=user_id,
                error=None,
                role=role
            )

            logger.info(f"Token verification successful for user_id: {user_id}, role: {role}")
            return response

        except Exception as e:
            logger.error(f"Unexpected error during token verification: {str(e)}", exc_info=True)
            return TokenVerifyResponseMessage(
                valid=False,
                user_id=None,
                error=f"Internal server error: {str(e)}",
                role=None
            )
