FROM python:3.11-slim

WORKDIR /authentication_service

RUN mkdir -p /authentication_service/shared

COPY shared/ /authentication_service/shared/
COPY requirements.txt /authentication_service/

RUN pip install --no-cache-dir -r requirements.txt

COPY authentication_service/ /authentication_service/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
