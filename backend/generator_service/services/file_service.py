"""Файловая служба для сервиса генерации"""#pylint: disable=W0707,W1514,W0718
import json
import uuid
from io import BytesIO
from minio import Minio
from minio.error import S3Error
from fastapi import HTTPException
from shared.config.base import settings

minio_client = Minio(
    endpoint=settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_SECURE
)

class FileService:
    """Класс файловой службы для сервиса генерации"""

    @staticmethod
    async def init_minio():
        """Инициализация MinIO buckets при старте приложения"""
        buckets = [
            settings.MINIO_GENERATED_BUCKET,
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

    @staticmethod
    async def save_json_to_minio(json_document: dict, generation_id: uuid.UUID) -> str:
        """Сохранение JSON документа с результатами генерации в MinIO"""
        try:
            # Формируем путь для сохранения
            filename = f"generation_{generation_id}.json"
            object_path = f"generations/{filename}"

            # Конвертируем JSON в bytes
            json_data = json.dumps(json_document, ensure_ascii=False, indent=2)
            json_bytes = json_data.encode('utf-8')

            # Сохраняем в MinIO
            minio_client.put_object(
                bucket_name=settings.MINIO_GENERATED_BUCKET,
                object_name=object_path,
                data=BytesIO(json_bytes),
                length=len(json_bytes),
                content_type="application/json"
            )

            print(f"✅ JSON document saved to MinIO: {object_path}")
            return object_path

        except S3Error as e:
            print(f"❌ Error saving JSON to MinIO: {e}")
            raise HTTPException(500, f"Failed to save JSON document: {str(e)}")

    @staticmethod
    async def save_temp_sequence(sequence: str, generation_id: uuid.UUID) -> str:
        """Сохранение временного файла с последовательностью для тестов"""
        try:
            filename = f"temp_sequence_{generation_id}.txt"
            object_path = f"temp_sequences/{filename}"

            sequence_bytes = sequence.encode('utf-8')

            minio_client.put_object(
                bucket_name=settings.MINIO_GENERATED_BUCKET,
                object_name=object_path,
                data=BytesIO(sequence_bytes),
                length=len(sequence_bytes),
                content_type="text/plain"
            )

            local_path = f"/tmp/{filename}"
            with open(local_path, 'w') as f:
                f.write(sequence)

            print(f"✅ Temporary sequence saved: {object_path}")
            return local_path

        except S3Error as e:
            print(f"❌ Error saving temporary sequence: {e}")
            raise HTTPException(500, f"Failed to save temporary sequence: {str(e)}")

    @staticmethod
    async def get_json_from_minio(object_path: str) -> dict:
        """Получение JSON документа из MinIO"""
        try:
            response = minio_client.get_object(
                bucket_name=settings.MINIO_GENERATED_BUCKET,
                object_name=object_path
            )

            json_data = response.read().decode('utf-8')
            return json.loads(json_data)

        except S3Error as e:
            print(f"❌ Error reading JSON from MinIO: {e}")
            raise HTTPException(404, f"JSON document not found: {str(e)}")
        finally:
            response.close()
            response.release_conn()

    @staticmethod
    async def upload_external_sequence(user_id: uuid.UUID,
                                       file_content: bytes, filename: str) -> str:
        """Загрузка внешней последовательности для тестирования"""
        try:
            content = file_content.decode('utf-8').strip()
            if not all(c in '01\n\r' for c in content):
                raise HTTPException(400, "File must contain only 0 and 1 characters")

            clean_sequence = ''.join(c for c in content if c in '01')

            object_path = f"user_{user_id}/external_{uuid.uuid4()}_{filename}"
            sequence_bytes = clean_sequence.encode('utf-8')

            minio_client.put_object(
                bucket_name=settings.MINIO_UPLOADED_BUCKET,
                object_name=object_path,
                data=BytesIO(sequence_bytes),
                length=len(sequence_bytes),
                content_type="text/plain"
            )

            print(f"✅ External sequence uploaded: {object_path}")
            return object_path

        except S3Error as e:
            print(f"❌ Error uploading external sequence: {e}")
            raise HTTPException(500, f"Failed to upload sequence: {str(e)}")

    @staticmethod
    async def save_test_results(test_run_id: uuid.UUID, results: dict) -> str:
        """Сохранение детальных результатов тестов в MinIO"""
        try:
            filename = f"test_results_{test_run_id}.json"
            object_path = f"test_results/{filename}"

            json_data = json.dumps(results, ensure_ascii=False, indent=2)
            json_bytes = json_data.encode('utf-8')

            minio_client.put_object(
                bucket_name=settings.MINIO_TEST_RESULTS_BUCKET,
                object_name=object_path,
                data=BytesIO(json_bytes),
                length=len(json_bytes),
                content_type="application/json"
            )

            print(f"✅ Test results saved to MinIO: {object_path}")
            return object_path

        except S3Error as e:
            print(f"❌ Error saving test results: {e}")
            raise HTTPException(500, f"Failed to save test results: {str(e)}")

    @staticmethod
    async def delete_generation_data(generation_id: uuid.UUID):
        """Удаление всех данных связанных с генерацией"""
        try:
            json_path = f"generations/generation_{generation_id}.json"
            minio_client.remove_object(settings.MINIO_GENERATED_BUCKET, json_path)

            temp_path = f"temp_sequences/temp_sequence_{generation_id}.txt"
            minio_client.remove_object(settings.MINIO_GENERATED_BUCKET, temp_path)

            print(f"✅ Generation data deleted: {generation_id}")

        except S3Error as e:
            print(f"⚠️ Error deleting generation data: {e}")

    @staticmethod
    async def get_file_url(bucket: str, object_path: str) -> str:
        """Получение URL файла в MinIO"""
        try:
            if settings.MINIO_SECURE:
                return f"https://{settings.MINIO_ENDPOINT}/{bucket}/{object_path}"
            return f"http://{settings.MINIO_ENDPOINT}/{bucket}/{object_path}"
        except Exception as e:
            print(f"⚠️ Error generating file URL: {e}")
            return None

async def get_file_service() -> FileService:
    """Генератор службы"""
    file_service = FileService()
    return file_service
