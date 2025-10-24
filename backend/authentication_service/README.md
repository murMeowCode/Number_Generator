# Auth Service

Микросервис для управления JWT токенами и аутентификации пользователей.

## 📋 Оглавление

- [Обзор](#обзор)
- [Функциональность](#функциональность)
- [API Endpoints](#api-endpoints)
- [Асинхронная обработка сообщений](#асинхронная-обработка-сообщений)
- [Схемы данных](#схемы-данных)
- [Установка и запуск](#установка-и-запуск)

## 🚀 Обзор

Auth Service предоставляет REST API для регистрации пользователей, аутентификации и управления JWT токенами, а также асинхронный механизм для верификации токенов через RabbitMQ.

![alt text](../../source/auth.png)

## ⚙️ Функциональность

- ✅ Регистрация новых пользователей
- ✅ Аутентификация пользователей
- ✅ Выдача JWT токенов (access + refresh)
- ✅ Обновление пары токенов
- ✅ Верификация токенов через message broker
- ✅ Health check эндпоинт

## 🔌 API Endpoints

### 🔐 Аутентификация

#### Регистрация пользователя
```http
POST /auth/register
```
Регистрация нового пользователя в системе.

**Тело запроса:**
```json
{
  "username": "string",
  "email": "string (email)",
  "password": "string",
  "surname": "string",
  "name": "string",
  "fathername": "string",
  "birth_date": "string (date)"
}
```

**Ответ:**
```json
{
  "id": "uuid",
  "username": "string",
  "email": "string",
  "surname": "string",
  "name": "string",
  "fathername": "string | null",
  "birth_date": "string (date) | null",
  "last_login": "string (datetime) | null"
}
```

#### Вход в систему
```http
POST /auth/login
```
Аутентификация пользователя и выдача токенов.

**Тело запроса:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Ответ:**
```json
{
  "success": "boolean",
  "tokens": "TokenPair | null",
  "error": "string | null",
  "user": {
    "id": "uuid",
    "username": "string",
    "email": "string (email)",
    "last_login": "string (datetime) | null"
  }
}
```

#### Обновление токенов
```http
POST /auth/refresh
```
Обновление пары access/refresh токенов.

**Тело запроса:**
```json
{
  "refresh_token": "string"
}
```

**Ответ:**
```json
{
  "success": "boolean",
  "tokens": "TokenPair | null",
  "error": "string | null"
}
```

### 🩺 Health Check
```http
GET /health
```
Проверка работоспособности сервиса.

## 📨 Асинхронная обработка сообщений

Сервис включает потребитель RabbitMQ для обработки запросов верификации токенов от других сервисов.


### Очереди и маршрутизация

- **Очередь:** `auth.verify.request`
- **Exchange:** `auth_exchange`
- **Routing Key:** `auth.verify.request`

### Типы сообщений

- `TOKEN_VERIFY_REQUEST` - запрос на верификацию токена
- `TOKEN_VERIFY_RESPONSE` - ответ с результатом верификации

### Обработка запросов верификации

```python
# Пример обработки запроса верификации токена
async def _handle_verify_request(self, message: aio_pika.IncomingMessage):
    # Декодирование и валидация сообщения
    # Верификация токена через AuthService
    # Отправка ответа обратно в очередь ответов
```

## 📊 Схемы данных

### TokenPair
```json
{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "string (default: bearer)"
}
```

### UserRegister
Схема для регистрации пользователя со всеми необходимыми полями.

### UserResponse
Упрощенная схема пользователя для ответов API.

### LoginRequest/LoginResponse
Схемы для процесса аутентификации.

## 🛠️ Установка и запуск

### Предварительные требования

- Python 3.8+
- RabbitMQ
- FastAPI
- Pydantic

### Зависимости

```bash
pip install aio-pika fastapi pydantic
```

### Конфигурация

```python
# Настройка подключения к RabbitMQ
RABBITMQ_URL = "amqp://guest:guest@localhost/"
```

### Запуск сервиса

```bash
# Запуск HTTP сервера
uvicorn main:app --host 0.0.0.0 --port 8000

# Инициализация потребителя сообщений
python -m authentication_service.messaging.consumers
```

## 🔧 Интеграция

### Для других сервисов

1. **REST API** - для прямой регистрации и аутентификации
2. **Message Broker** - для верификации токенов в реальном времени

### Пример запроса верификации токена

```python
# Отправка запроса на верификацию
verify_message = TokenVerifyMessage(token="jwt_token_here")
# Ожидание ответа через RabbitMQ
```

## 🐛 Логирование

Сервис использует структурированное логирование для отслеживания:
- Успешной аутентификации
- Ошибок валидации
- Операций с токенами
- Сообщений RabbitMQ

## 🔒 Безопасность

- JWT токены с разделением на access/refresh
- Валидация входных данных
- Безопасное хранение паролей (хэширование)
- Верификация токенов через защищенный канал

---
