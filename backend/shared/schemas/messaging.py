"""схемы общения с очередью"""
from datetime import date
from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    """схема регистрации пользователя"""
    username: str
    email: EmailStr
    password: str
    surname: str
    name: str
    fathername: str
    birth_date: date

class MessageType(str, Enum):
    """класс-перечисление типов сообщений"""
    TOKEN_VERIFY_REQUEST = "token_verify_request"
    TOKEN_VERIFY_RESPONSE = "token_verify_response"

class BaseMessage(BaseModel):
    """базовое сообщение из очереди"""
    message_type: MessageType
    data: dict
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None

class TokenVerifyMessage(BaseModel):
    """сообщение о верификации токена"""
    token: str

class TokenVerifyResponseMessage(BaseModel):
    """ответ на верификацию"""
    valid: bool
    user_id: Optional[str] = None
    error: Optional[str] = None
    role: Optional[int] = None
