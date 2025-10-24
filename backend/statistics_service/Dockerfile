FROM python:3.11-slim

WORKDIR /statistics_service

RUN mkdir -p /statistics_service/shared

COPY shared/ /statistics_service/shared/
COPY requirements.txt /statistics_service/

RUN pip install --no-cache-dir -r requirements.txt

COPY statistics_service/ /statistics_service/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]