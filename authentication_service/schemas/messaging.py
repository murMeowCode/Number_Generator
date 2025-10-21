"""схемы для общения с очередями"""
from typing import Optional
from pydantic import BaseModel

class TokenRefreshMessage(BaseModel):
    """схема перевыдачи токена в очереди"""
    refresh_token: str

class TokenRefreshResponseMessage(BaseModel):
    """ответ на перевыдачу"""
    success: bool
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    error: Optional[str] = None
