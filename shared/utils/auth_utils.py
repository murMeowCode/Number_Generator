"""общий модуль для аутентификации"""#pylint: disable=E0401, E0611, W0707, W0718
import uuid
from aiohttp import ClientResponseError
from fastapi import HTTPException, Depends, Query, WebSocket, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from shared.messaging.producers import AuthProducer
from shared.config.base import settings

class AuthDependency:
    """зависимость аутентификации"""
    def __init__(self, producer: AuthProducer):
        self.producer = producer
        self.security_scheme = HTTPBearer()

    async def get_current_user(
            self,
            credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
        ) -> dict:
        """Проверяет токен и возвращает данные пользователя"""
        token = credentials.credentials

        try:
            # Отправляем запрос на верификацию
            response = await self.producer.verify_token(token)

            if not response.valid:
                raise HTTPException(status_code=401, detail="Invalid token")

            if not response.user_id:
                raise HTTPException(status_code=401, detail="User not found")

            return {
                "user_id": uuid.UUID(response.user_id),
                "role": response.role or 0
            }

        except ClientResponseError as e:
            # Обрабатываем HTTP ошибки от aiohttp
            if e.status == 401:
                raise HTTPException(status_code=401, detail="Invalid token")
            if e.status == 503:
                raise HTTPException(status_code=503, detail="Authentication service unavailable")

            raise HTTPException(status_code=e.status,
                                detail=f"Authentication service error: {e.message}")

        except TimeoutError:
            raise HTTPException(status_code=503, detail="Authentication service unavailable")

        except HTTPException:
            # Пробрасываем уже созданные HTTPException
            raise

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Authentication error: {str(e)}")

    async def require_role(self, required_role: int,
                           user: dict = Depends(get_current_user)) -> dict:
        """Проверяет роль пользователя"""
        if user.get("role", 0) != required_role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user

    async def get_current_user_websocket(self,
        websocket: WebSocket,
        token: str = Query(...),
    ):
        """Аутентификация пользователя для WebSocket"""
        try:
            # Извлекаем токен из query параметров
            user = await self.producer.verify_token(token)
            if not user:
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                return None
            return user
        except Exception:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None

def get_auth_dependency() -> AuthDependency:
    """Фабрика для создания AuthDependency"""
    producer = AuthProducer(rabbitmq_url=settings.RABBITMQ_URL)  # Создаем producer с настройками
    return AuthDependency(producer)
