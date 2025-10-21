"""Служба OAuth""" #pylint: disable=E0401,E0611, W0718
from datetime import datetime, timedelta
from typing import Any, Dict
import httpx
from sqlalchemy import select
from shared.schemas.messaging import UserCreatedMessage
from shared.database.database import AsyncSession
from shared.config.base import settings
from auth_service.models.oauth import OAuthState
from auth_service.messaging.producers import UserProducer
from auth_service.services.token_service import TokenService
from auth_service.services.user_service import UserService
from auth_service.services.yandex_oauth import YandexOAuthService
from auth_service.models.user import AuthUser

class OAuthService:
    """Класс службы"""
    def __init__(self, db: AsyncSession, producer: UserProducer):
        self.db = db
        self.user_service = UserService(db)
        self.token_service = TokenService(db)
        self.yandex_oauth = YandexOAuthService()
        self.producer = producer

    async def create_yandex_oauth_state(self) -> str:
        """Создание и сохранение OAuth state для Яндекса"""
        state = self.yandex_oauth.generate_state()

        state_record = OAuthState(
            state=state,
            expires_at=datetime.utcnow() + timedelta(minutes=10)
        )

        self.db.add(state_record)
        await self.db.commit()
        return state

    async def validate_oauth_state(self, state: str) -> bool:
        """Валидация OAuth state из базы"""
        try:
            stmt = select(OAuthState).where(OAuthState.state == state)
            result = await self.db.execute(stmt)
            state_record = result.scalar_one_or_none()

            if not state_record:
                print(f"State not found: {state}")
                return False

            if state_record.is_expired():
                print(f"State expired: {state}")
                # Удаляем просроченный state
                await self.db.delete(state_record)
                await self.db.commit()
                return False

            # Удаляем использованный state
            await self.db.delete(state_record)
            await self.db.commit()
            return True

        except Exception as e:
            print(f"Error validating state: {e}")
            return False

    async def validate_yandex_oauth_state(self, state: str) -> bool:
        """Валидация OAuth state для Яндекса"""
        return await self.validate_oauth_state(state)

    async def handle_vk_id_callback(self, code: str, device_id: str):
        """Обработка callback от VK ID SDK"""
        # 1. Обмен кода на access token
        vk_tokens = await self._exchange_vk_id_code(code, device_id)

        # 2. Получение информации о пользователе
        user_info = await self._get_vk_user_info(vk_tokens["access_token"])

        # 3. Создание/обновление пользователя в вашей системе
        user = await self._create_or_update_vk_user(user_info)

        # 4. Генерация ваших JWT токенов
        tokens = await self._generate_user_tokens(user)

        return {
            "user": user,
            "tokens": tokens
        }

    async def _exchange_vk_id_code(self, code: str, device_id: str) -> dict:
        """Обмен кода VK ID на access token"""
        url = "https://id.vk.com/oauth2/auth"
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": settings.VK_CLIENT_ID,
            "client_secret": settings.VK_CLIENT_SECRET,
            "redirect_uri": settings.VK_REDIRECT_URI,
            "device_id": device_id
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data)
            if response.status_code != 200:
                raise ValueError(f"VK token exchange failed: {response.text}")

            return response.json()

    async def _get_vk_user_info(self, access_token: str) -> dict:
        """
        Получение информации о пользователе из VK
        """
        url = "https://api.vk.com/method/users.get"
        params = {
            "access_token": access_token,
            "v": "5.131",
            "fields": "email,first_name,last_name,photo_max,bdate"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            if response.status_code != 200:
                raise ValueError(f"Failed to get user info: {response.text}")

            data = response.json()
            if "error" in data:
                raise ValueError(f"VK API error: {data['error']}")

            return data["response"][0]  # первый пользователь в ответе

    async def _create_or_update_vk_user(self, user_info: dict):
        """
        Создание или обновление пользователя в вашей системе
        """
        vk_user_id = user_info["id"]
        email = user_info.get("email")
        first_name = user_info.get("first_name", "")
        last_name = user_info.get("last_name", "")
        avatar_url = user_info.get("photo_200", "")

        # Находим или создаем пользователя в auth service
        data = await self.user_service.find_or_create_oauth_user(
            vk_id=vk_user_id,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        user = data["user"]
        is_new_user = data["new"]

        if is_new_user:
            await self._send_oauth_user_created_event(
                user=user,
                first_name=first_name,
                last_name=last_name,
                avatar_url=avatar_url
            )
        await self.user_service.update_user_last_login(user.id)

        # Создаем токены
        tokens = await self._generate_user_tokens(user)

        return {
            "user": user,
            "tokens": tokens,
            "is_new_user": is_new_user
        }

    async def _generate_user_tokens(self, user):
        """
        Генерация JWT токенов для вашего приложения
        """
        return await self.token_service.create_token_pair(
            user_id=str(user.id),
            username=user.username
        )


    async def handle_yandex_oauth_callback(self, code: str) -> Dict[str, Any]:
        """Обработка callback от Яндекс OAuth"""
        # Получаем access token
        token_data = await self.yandex_oauth.get_access_token(code)
        if not token_data or "access_token" not in token_data:
            raise ValueError("Failed to get access token from Yandex")

        access_token = token_data["access_token"]

        # Получаем информацию о пользователе
        user_info = await self.yandex_oauth.get_user_info(access_token)
        if not user_info:
            raise ValueError("Failed to get user info from Yandex")

        yandex_user_id = user_info.get("id")
        email = user_info.get("default_email") or user_info.get("emails", [None])[0]
        first_name = user_info.get("first_name", "")
        last_name = user_info.get("last_name", "")
        avatar_url = user_info.get("default_avatar_id", "")

        if not yandex_user_id or not email:
            raise ValueError("Incomplete user info from Yandex")

        # Находим или создаем пользователя в auth service
        user = await self.user_service.find_or_create_oauth_user(
            yandex_id=yandex_user_id,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        # Отправляем событие в основной сервис для создания профиля
        is_new_user = user.created_at.date() == datetime.utcnow().date()

        if is_new_user:
            await self._send_oauth_user_created_event(
                user=user,
                first_name=first_name,
                last_name=last_name,
                avatar_url=avatar_url
            )

        # Обновляем время последнего входа
        await self.user_service.update_user_last_login(user.id)

        # Создаем токены
        tokens = await self.token_service.create_token_pair(
            user_id=str(user.id),
            username=user.username
        )

        return {
            "user": user,
            "tokens": tokens,
            "is_new_user": is_new_user
        }

    async def _send_oauth_user_created_event(
        self,
        user: AuthUser,
        first_name: str,
        last_name: str,
        avatar_url: str = None
    ):
        """Отправка события создания OAuth пользователя"""
        user_created_message = UserCreatedMessage(
            user_id=user.id,
            username=user.username,
            email=user.email,
            password=None,  # Пароль отсутствует
            role=user.role,
            first_name=first_name,
            last_name=last_name,
            avatar_url=avatar_url,
            middle_name=None,  # Для VK не предоставляется
            birth_date=None,   # Для VK не предоставляется
            phone=None,        # Для VK не предоставляется
            address=None      # Для VK не предоставляется
        )

        # Отправляем в основной сервис
        await self.producer.send_user_created_event(user_created_message)

        # Отправляем уведомление
        await self.producer.send_notification({
            "type": "user_registered_oauth",
            "username": user.username,
            "user_email": user.email,
            "user_id": str(user.id),
            "oauth_provider": "vk",
            "first_name": first_name,
            "last_name": last_name
        })
