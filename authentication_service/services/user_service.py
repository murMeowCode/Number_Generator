"""служба работы с сущностью пользователя"""#pylint: disable=E0611, E0401
from datetime import datetime
import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from auth_service.models.user import AuthUser
from auth_service.core.security import verify_password, get_password_hash
from shared.schemas.messaging import UserCreatedMessage

class UserService:
    """класс службы"""
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_username(self, username: str) -> Optional[AuthUser]:
        """Получение пользователя по username"""
        stmt = select(AuthUser).where(AuthUser.username == username)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: uuid.UUID) -> Optional[AuthUser]:
        """Получение пользователя по ID"""
        stmt = select(AuthUser).where(AuthUser.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[AuthUser]:
        """Получение пользователя по email"""
        stmt = select(AuthUser).where(AuthUser.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def authenticate_user(self, username: str, password: str) -> Optional[AuthUser]:
        """Аутентификация пользователя"""
        user = await self.get_user_by_username(username)
        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    async def create_user(self, user_data: UserCreatedMessage) -> AuthUser:
        """Создание нового пользователя"""
        # Проверяем, нет ли уже пользователя с таким username или email
        existing_user = await self.get_user_by_username(user_data.username)
        if existing_user:
            raise ValueError("User with this username already exists")

        existing_email = await self.get_user_by_email(user_data.email)
        if existing_email:
            raise ValueError("User with this email already exists")

        # Создаем пользователя
        hashed_password = get_password_hash(user_data.password)
        user = AuthUser(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            role=user_data.role
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def update_user_last_login(self, user_id: uuid.UUID):
        """Обновление времени последнего входа"""
        user = await self.get_user_by_id(user_id)
        if user:
            user.last_login = datetime.utcnow()
            await self.db.commit()

    async def get_user_by_vk_id(self, vk_id: int) -> Optional[AuthUser]:
        """Получение пользователя по VK ID"""
        stmt = select(AuthUser).where(AuthUser.vk_id == vk_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_oauth_user(
        self,
        vk_id: int,
        email: str,
    ) -> AuthUser:
        """Создание пользователя через OAuth"""
        # Генерируем уникальный username
        base_username = f"vk_{vk_id}"
        username = base_username
        counter = 1

        while await self.get_user_by_username(username):
            username = f"{base_username}_{counter}"
            counter += 1

        # Если email не предоставлен VK, создаем временный
        if not email:
            email = f"{username}@temp.vk"

        # Создаем пользователя (только базовые поля)
        user = AuthUser(
            username=username,
            email=email,
            role=1,  # Обычный пользователь
            hashed_password=None,  # Пароль не задан
            vk_id=vk_id,
            oauth_provider="vk"
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def find_or_create_oauth_user(self,
                                        vk_id=None,
                                        yandex_id=None,
                                        email=None):
        """Находим или создаем OAuth пользователя"""
        if vk_id:
            # Существующая логика для VK
            stmt = select(AuthUser).where(AuthUser.vk_id == vk_id)
            result = await self.db.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                data = {"user":user,"new": False}
                return data
            # Создаем нового
            username = f"vk_{vk_id}"
            user = AuthUser(
                username=username,
                email=email or f"{username}@vk.com",
                role=1,  # По умолчанию
                vk_id=vk_id,
                oauth_provider="vk"
            )
            self.db.add(user)
            await self.db.commit()

            data = {"user": user, "new": True}
            return data

        if yandex_id:
            stmt = select(AuthUser).where(AuthUser.yandex_id == yandex_id)
            result = await self.db.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                return user
            username = f"yandex_{yandex_id}"
            user = AuthUser(
                username=username,
                email=email,
                role=1,
                yandex_id=yandex_id,
                oauth_provider="yandex"
            )
            self.db.add(user)
            await self.db.commit()
            return user
        raise ValueError("Either vk_id or yandex_id must be provided")
