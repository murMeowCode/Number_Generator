"""Служба OAuth для Яндекса""" #pylint: disable=E0401
import secrets
from typing import Dict, Optional
from shared.config.base import settings
import aiohttp

class YandexOAuthService:
    """Класс для работы с OAuth Яндекса"""
    def __init__(self):
        self.client_id = settings.YANDEX_CLIENT_ID
        self.client_secret = settings.YANDEX_CLIENT_SECRET
        self.redirect_uri = settings.YANDEX_REDIRECT_URI
        self.auth_url = "https://oauth.yandex.ru/authorize"
        self.token_url = "https://oauth.yandex.ru/token"
        self.user_info_url = "https://login.yandex.ru/info"

    def generate_state(self) -> str:
        """Генерация уникального state"""
        return secrets.token_urlsafe(32)

    def get_auth_url(self, state: str) -> str:
        """Формирование URL для редиректа на Яндекс"""
        return (
            f"{self.auth_url}?response_type=code&client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}&state={state}&scope=login:email+login:info"
        )

    async def get_access_token(self, code: str) -> Optional[Dict]:
        """Получение access token по коду"""
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.token_url, data=data) as response:
                if response.status == 200:
                    return await response.json()
                return None

    async def get_user_info(self, access_token: str) -> Optional[Dict]:
        """Получение информации о пользователе"""
        headers = {"Authorization": f"OAuth {access_token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.user_info_url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                return None
