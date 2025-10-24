FROM python:3.11-slim

WORKDIR /generator_service

RUN mkdir -p /generator_service/shared

COPY shared/ /generator_service/shared/
COPY requirements.txt /generator_service/

RUN pip install --no-cache-dir -r requirements.txt

COPY generator_service/ /generator_service/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]