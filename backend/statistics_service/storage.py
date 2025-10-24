from minio import Minio
from minio.error import S3Error
import io
from shared.config.base import settings

# Инициализация MinIO клиента
minio_client = Minio(
    endpoint=settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_SECURE
)

class MinIOClient:
    def __init__(self):
        self.client = minio_client
    
    async def upload_file(self, bucket_name: str, filename: str, content: str) -> str:
        try:
            data = io.BytesIO(content.encode('utf-8'))
            self.client.put_object(
                bucket_name,
                filename,
                data,
                length=len(content),
                content_type='text/plain'
            )
            
            return f"{settings.MINIO_ENDPOINT}/{bucket_name}/{filename}"
        except S3Error as e:
            raise Exception(f"MinIO error: {str(e)}")

    async def init_minio():
        """Инициализация MinIO buckets при старте приложения"""
        buckets = [
            settings.MINIO_UPLOADED_BUCKET,
            "generated"  # добавляем bucket для сгенерированных файлов если нужно
        ]

        try:
            for bucket_name in buckets:
                if not minio_client.bucket_exists(bucket_name):
                    minio_client.make_bucket(bucket_name)
                    print(f"✅ MinIO bucket '{bucket_name}' created")
                else:
                    print(f"✅ MinIO bucket '{bucket_name}' already exists")

        except S3Error as e:
            print(f"❌ MinIO initialization error: {e}")
            raise

def get_minio_client() -> MinIOClient:
    """Фабричная функция для получения MinIO клиента"""
    return MinIOClient()
