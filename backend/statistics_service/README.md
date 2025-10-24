
# Statistics Service API

Микросервис для статистического анализа бинарных последовательностей с применением тестов NIST.

## 📊 Обзор сервиса

Сервис предоставляет REST API для анализа бинарных последовательностей (последовательностей из 0 и 1) с использованием стандартных статистических тестов. Поддерживает анализ как строковых последовательностей, так и загружаемых файлов.

![alt text](../../source/stats.png)

## 🚀 Быстрый старт

### Требования

- Python 3.8+
- Redis
- PostgreSQL
- MinIO (опционально, для хранения файлов)

### Установка и запуск

```bash
# Клонирование репозитория
git clone <repository-url>
cd statistics-service

# Установка зависимостей
pip install -r requirements.txt

# Настройка переменных окружения
cp .env.example .env
# отредактируйте .env файл с вашими настройками

# Запуск сервиса
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 📚 API Endpoints

### 🔍 Анализ последовательностей

#### Анализ строковой последовательности
```http
POST /statistics/sequence
Content-Type: application/json
```

**Тело запроса:**
```json
{
  "sequence": "01010101010101010101",
  "sequence_id": "uuid-последовательности"
}
```

**Ответ:**
```json
{
  "statistics_id": "uuid-статистики",
  "sequence_id": "uuid-последовательности",
  "sequence_length": 20,
  "ones_count": 10,
  "zeros_count": 10,
  "ones_proportion": 0.5,
  "tests_passed": 8,
  "tests_total": 8,
  "success_rate": 1.0,
  "created_at": "2024-01-15T10:30:00Z",
  "tests_results": {
    "frequency": {
      "p_value": 0.85,
      "result": "PASS",
      "details": {}
    }
    // ... другие тесты
  }
}
```

#### Анализ файла
```http
POST /statistics/file
Content-Type: multipart/form-data
```

**Параметры:**
- `file`: Бинарный файл с последовательностью

**Ответ:** Аналогично анализу строки + поле `file_url` с ссылкой на сохраненный файл.

### 📈 Получение результатов

#### Получить статистику по ID
```http
GET /statistics/{sequence_id}
```

**Параметры:**
- `sequence_id`: UUID последовательности

**Кэширование:** Результаты кэшируются на 30 минут

### 📊 Дашборд аналитики

#### Обзорная статистика
```http
GET /statistics/dashboard/overview
```

**Ответ:**
```json
{
  "total_sequences": 150,
  "avg_sequence_length": 1024.5,
  "avg_success_rate": 0.78,
  "bit_distribution": [
    {
      "length_range": "0-100",
      "avg_ones": 45.2,
      "avg_zeros": 54.8,
      "sequence_count": 25
    }
  ],
  "worst_tests": [
    {
      "test_name": "serial",
      "success_rate": 0.45,
      "total_sequences": 150
    }
  ],
  "heatmap_data": {
    "sequence_ids": ["uuid1", "uuid2"],
    "test_names": ["frequency", "runs"],
    "results": [{...}]
  }
}
```

**Кэширование:** Данные дашборда кэшируются на 5 минут

### 🩺 Health Check

```http
GET /health
```

Проверка работоспособности сервиса.

## 🔬 Статистические тесты

Сервис выполняет следующие тесты NIST:

### 1. Frequency Test (Частотный тест)
Проверяет баланс между 0 и 1 в последовательности.

### 2. Runs Test (Тест серий)
Анализирует последовательности одинаковых битов.

### 3. Serial Test (Последовательный тест)
Проверяет распределение пар битов.

### 4. Autocorrelation Test (Тест автокорреляции)
Анализирует корреляцию между сдвинутыми версиями последовательности.

### 5. Poker Test (Покер-тест)
Проверяет распределение комбинаций битов.

### 6. Cumulative Sums Test (Тест кумулятивных сумм)
Анализирует накопленные суммы последовательности.

### 7. Longest Runs Test (Тест самых длинных серий)
Проверяет распределение самых длинных последовательностей одинаковых битов.

### 8. Matrix Rank Test (Тест ранга матрицы)
Анализирует ранг бинарных матриц, построенных из последовательности.

## 💾 Кэширование

Сервис использует двухуровневое кэширование:

- **Статистика по ID**: Кэш на 30 минут
- **Дашборд**: Кэш на 5 минут с автоматической инвалидацией при добавлении новых данных

## 🗃️ Модели данных

### StatisticsRequest
```typescript
{
  sequence: string;      // Последовательность из 0 и 1
  sequence_id: UUID;     // Идентификатор последовательности
}
```

### StatisticsResponseSchema
```typescript
{
  statistics_id: UUID;
  sequence_id: UUID;
  sequence_length: number;
  ones_count: number;
  zeros_count: number;
  ones_proportion: number;
  tests_passed: number;
  tests_total: number;
  success_rate: number;
  created_at: DateTime;
  tests_results: Map<TestType, TestResultDetail>;
}
```

### TestResultDetail
```typescript
{
  p_value: number | null;    // Статистическая значимость
  result: "PASS" | "FAIL" | "WARNING" | "SKIP";
  details: object;           // Дополнительная информация
}
```

## 🔧 Конфигурация

Основные переменные окружения:

```env
DATABASE_URL=postgresql://user:pass@localhost/dbname
REDIS_URL=redis://localhost:6379
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=access_key
MINIO_SECRET_KEY=secret_key
```

## 📈 Мониторинг и логирование

Сервис предоставляет:

- Подробное логирование всех операций
- Health check endpoint
- Метрики производительности
- Отслеживание кэш-попаданий/промахов
