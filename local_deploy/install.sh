#!/bin/bash

set -e

echo "=== Запуск развертывания сервисов ==="

echo "1. Создание сети prod-network..."
docker network create prod-network || true

# 2. PostgreSQL
echo "2. Запуск PostgreSQL..."
docker run -d --name postgres --network prod-network \
  -p 5666:5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=slon_311. \
  -e POSTGRES_DB=postgres \
  postgres:latest

# 3. Redis
echo "3. Запуск Redis..."
docker run -d --name redis --network prod-network \
  -p 6379:6379 \
  -e REDIS_PASSWORD=redis_311. \
  redis:latest redis-server --requirepass "redis_311."

# 4. RabbitMQ
echo "4. Запуск RabbitMQ..."
docker run -d --name rabbitmq --network prod-network \
  -p 5672:5672 \
  -p 15672:15672 \
  -e RABBITMQ_DEFAULT_USER=guest \
  -e RABBITMQ_DEFAULT_PASS=guest \
  rabbitmq:management

# 5. MinIO
echo "5. Запуск MinIO..."
docker run -d --name minio --network prod-network \
  -p 9000:9000 \
  -p 9001:9001 \
  -e MINIO_ROOT_USER=minioadmin \
  -e MINIO_ROOT_PASSWORD=minio_311. \
  quay.io/minio/minio server /data --console-address ":9001"

# 6. PGAdmin
echo "6. Запуск PGAdmin..."
docker run -d --name pgadmin --network prod-network \
  -p 5123:80 \
  -e PGADMIN_DEFAULT_EMAIL=admin@admin.com \
  -e PGADMIN_DEFAULT_PASSWORD=admin \
  dpage/pgadmin4



echo "=== Все сервисы успешно запущены! ==="
echo ""
echo "Доступ к сервисам:"
echo "PostgreSQL: localhost:5666 (postgres/slon_311.)" 
echo "Redis: localhost:6379"
echo "RabbitMQ: http://localhost:15672 (guest/guest)"
echo "MinIO: http://localhost:9001 (minioadmin/minio_311.)"
echo "PGAdmin: http://localhost:5123 (admin@admin.com/admin)"
echo ""
echo "Для проверки статуса выполните: docker ps"
echo "Для просмотра логов: docker logs <имя_контейнера>"
