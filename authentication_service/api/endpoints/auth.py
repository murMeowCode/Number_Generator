"""апи для аутентификации""" #pylint: disable=E0401, C0412, W0707
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from auth_service.messaging.producers import UserProducer, get_producer
from auth_service.services.registration_service import RegistrationService
from auth_service.schemas.auth import (LoginRequest, LoginResponse, RefreshTokenRequest,
RefreshTokenResponse, UserRegisterResponse, UserResponse, ForgotPasswordRequest,
ForgotPasswordResponse, ResetPasswordRequest, ResetPasswordResponse, VKExchangeRequest)
from auth_service.services.token_service import TokenService
from auth_service.services.user_service import UserService
from auth_service.services.password_reset_service import PasswordResetService
from auth_service.services.oauth_service import OAuthService
from shared.database.database import get_db
from shared.schemas.messaging import UserRegister

router = APIRouter()



@router.post("/register", response_model=UserRegisterResponse)
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db),
    producer: UserProducer = Depends(get_producer)  # Получаем из состояния приложения
):
    """Регистрация нового пользователя"""
    registration_service = RegistrationService(db, producer)
    result = await registration_service.register_user(user_data)

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

@router.post("/forgot-password", response_model=ForgotPasswordResponse)
async def forgot_password(
    request: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db),
    producer: UserProducer = Depends(get_producer)
):
    """Запрос на сброс пароля по email"""
    service = PasswordResetService(db, producer)
    result = await service.request_password_reset(request.email)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )

    return ForgotPasswordResponse(success=True, message=result["message"])

@router.post("/reset-password", response_model=ResetPasswordResponse)
async def reset_password(
    request: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    """Сброс пароля с новым паролем"""
    service = PasswordResetService(db)
    result = await service.reset_password(request.token, request.new_password)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )

    return ResetPasswordResponse(success=True, message=result["message"])

@router.post("/vk/callback")
async def vk_exchange_code(
    request: VKExchangeRequest,
    db: AsyncSession = Depends(get_db),
    producer: UserProducer = Depends(get_producer)
):
    """
    Обмен кода VK ID на токены и авторизацию пользователя
    """
    if not request.code or not request.device_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing code or device_id parameters"
        )

    oauth_service = OAuthService(db, producer)

    try:
        # Обмен кода на токен и создание/авторизация пользователя
        result = await oauth_service.handle_vk_id_callback(
            code=request.code,
            device_id=request.device_id
        )

        return {
            "success": True,
            "tokens": result["tokens"],
            "user": {
                "id": result["user"].id,
                "username": result["user"].username,
                "email": result["user"].email,
            },
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Логируем ошибку для отладки
        print(f"VK ID exchange error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/yandex")
async def yandex_oauth_start(
    request: Request,
    db: AsyncSession = Depends(get_db),
    producer: UserProducer = Depends(get_producer)
):
    """Начало OAuth flow - редирект на Яндекс"""
    oauth_service = OAuthService(db, producer)

    # Создаем state и получаем URL для Яндекса
    state = await oauth_service.create_yandex_oauth_state()
    yandex_auth_url = oauth_service.yandex_oauth.get_auth_url(state)

    # Для фронтенда возвращаем URL
    if request.headers.get("accept") == "application/json":
        return JSONResponse({
            "auth_url": yandex_auth_url,
            "state": state
        })

    # Для прямого доступа - редирект
    return RedirectResponse(yandex_auth_url)

@router.get("/yandex/callback")
async def yandex_oauth_callback(
    code: str = None,
    state: str = None,
    error: str = None,
    db: AsyncSession = Depends(get_db),
    producer: UserProducer = Depends(get_producer)
):
    """Callback от Яндекс OAuth"""
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Yandex OAuth error: {error}"
        )

    if not code or not state:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing code or state parameters"
        )

    oauth_service = OAuthService(db, producer)

    # Валидируем state
    if not await oauth_service.validate_yandex_oauth_state(state):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired state"
        )

    try:
        result = await oauth_service.handle_yandex_oauth_callback(code)

        return {
            "success": True,
            "tokens": result["tokens"],
            "user": {
                "id": result["user"].id,
                "username": result["user"].username,
                "email": result["user"].email,
                "is_oauth": result["user"].is_oauth_user
            },
            "is_new_user": result["is_new_user"]
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
