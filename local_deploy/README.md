# Развертывание сервиса локально
[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/Docker_Compose-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/compose/)

Для того, чтобы развернуть сервис локально выполните следующие действия:
---
1. 
```bash
git clone https://github.com/armada-team/random-generator.git
cd random-generator
cd local_deploy
```
2. **Установите** [docker](https://docs.docker.com/engine/install/) и [docker-compose](https://fornex.com/ru/help/install-docker-ubuntu-20-04/)
3. **Выполните**: 
```bash
chmod +x install.sh
sudo ./install.sh
```
4. Скопируйте конфигурацию с `local-deploy/nginx.conf` в `frontend/nginx.conf`
5. В корне проекта выполните `docker-compose up -d`
