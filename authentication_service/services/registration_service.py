"""сервис регистрации"""#pylint: disable=E0611, E0401, W0718
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from shared.schemas.messaging import UserCreatedMessage
from shared.schemas.messaging import UserRegister
from auth_service.services.user_service import UserService
from auth_service.messaging.producers import UserProducer

class RegistrationService:
    """класс сервиса регистрации"""
    def __init__(self, db: AsyncSession, producer: UserProducer):
        self.db = db
        self.producer = producer
        self.user_service = UserService(db)

    async def register_user(self, user_data: UserRegister):
        """Регистрация нового пользователя"""
        try:
            # Создаем пользователя в auth базе
            user = await self.user_service.create_user(user_data)

            # Подготавливаем данные для отправки в основной сервис
            user_created_message = UserCreatedMessage(
                user_id=user.id,
                username=user.username,
                email=user.email,
                password=user_data.password,
                role=user_data.role,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                middle_name=user_data.middle_name,
                birth_date=user_data.birth_date,
                phone=user_data.phone,
                address=user_data.address,
                created_at=datetime.utcnow(),
                avatar_url=None
            )

            # Отправляем событие в RabbitMQ
            await self.producer.send_user_created_event(user_created_message)
            await self.producer.send_notification({
                "type": "user_registered",
                "username": user.username,
                "user_email": user.email,
                "user_id": str(user.id)
            })

            return {
                "success": True,
                "user_id": user.id
            }

        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Registration failed: {str(e)}"
            }
