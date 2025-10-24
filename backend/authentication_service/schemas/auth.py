"""схемы для аутентификации"""
from datetime import date, datetime
import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserRegisterResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    surname: str
    name: str
    fathername: Optional[str]
    birth_date: Optional[date]
    last_login: Optional[datetime]

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    """схема для записи в локальную таблицу"""
    id: uuid.UUID
    username: str
    email: EmailStr
    last_login: Optional[datetime]

    class Config:
        """переключение в режим ORM"""
        from_attributes = True

class TokenPair(BaseModel):
    """схема токенов"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """данные, зашиваемые в токены"""
    user_id: str
    username: Optional[str] = None

class RefreshTokenRequest(BaseModel):
    """запрос на перевыдачу токенов"""
    refresh_token: str

class RefreshTokenResponse(BaseModel):
    """ответ перевыдачи токенов"""
    success: bool
    tokens: Optional[TokenPair] = None
    error: Optional[str] = None

class LoginRequest(BaseModel):
    """запрос на вход"""
    username: str
    password: str

class LoginResponse(BaseModel):
    """овтет на логин"""
    success: bool
    tokens: Optional[TokenPair] = None
    error: Optional[str] = None
    user: UserResponse
