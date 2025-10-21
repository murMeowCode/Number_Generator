"""апи для аутентификации""" #pylint: disable=E0401, C0412, W0707
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from authentication_service.schemas.auth import (LoginRequest, LoginResponse, RefreshTokenRequest,
RefreshTokenResponse, UserRegisterResponse, UserResponse)
from authentication_service.services.token_service import TokenService
from authentication_service.services.user_service import UserService
from shared.database.database import get_db
from shared.schemas.messaging import UserRegister

router = APIRouter()



@router.post("/register", response_model=UserRegisterResponse)
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """Регистрация нового пользователя"""
    user_service = UserService(db)
    result = await user_service.create_user(user_data)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )

    return UserRegisterResponse(
        success=True,
        user_id=result["user_id"]
    )

@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Аутентификация пользователя"""
    user_service = UserService(db)
    token_service = TokenService(db)

    # Аутентифицируем пользователя
    user = await user_service.authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    # Обновляем время последнего входа
    await user_service.update_user_last_login(user.id)

    # Создаем токены
    tokens = await token_service.create_token_pair(
        user_id=str(user.id),
        username=user.username
    )

    user_response = UserResponse.from_orm(user)

    return LoginResponse(
        success=True,
        tokens=tokens,
        user=user_response
    )

@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_tokens(refresh_data: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    """Обновление пары токенов"""
    token_service = TokenService(db)
    result = await token_service.refresh_tokens(refresh_data.refresh_token)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )

    return RefreshTokenResponse(
        success=True,
        tokens=result["tokens"]
    )
