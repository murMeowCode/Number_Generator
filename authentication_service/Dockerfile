FROM python:3.11-slim

WORKDIR /auth_service

RUN mkdir -p /auth_service/shared

COPY shared/ /auth_service/shared/
COPY requirements.txt /auth_service/

RUN pip install --no-cache-dir -r requirements.txt

COPY auth_service/ /auth_service/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
