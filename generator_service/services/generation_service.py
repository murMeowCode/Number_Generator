"""служба генерации"""#pylint: disable=W0706
import uuid
import requests
import random
from sqlalchemy.ext.asyncio import AsyncSession
from generator_service.services.file_service import FileService
from generator_service.models.generation import Generation


class GenerationService:
    def __init__(self, db: AsyncSession, file_service: FileService):
        self.db = db
        self.file_service = file_service

    async def generate_sequence(self, length: int) -> tuple[str, str]:
        """
        Генерирует начальное заполнение и последовательность (заглушки).
        """
        url = "https://services.swpc.noaa.gov/json/goes/primary/xray-flares-latest.json"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if not data:
            print("Ошибка: Получены пустые данные.")
            return None
            
        current_ratio = data[0].get('current_ratio', 'Поле не найдено')
        initial_fill = f"seed_{length}"
        sequence = ''.join(random.choice('01') for _ in range(length))
        return initial_fill, sequence

    async def generate_and_save_in_db(self, length: int) -> Generation:
        """
        Генерирует последовательность и сохраняет в БД (без файла).
        Возвращает объект Generation.
        """
        initial_fill, sequence = await self.generate_sequence(length)
        generation = Generation(
            length=length,
            initial_fill=initial_fill,
            sequence=sequence,
        )
        self.db.add(generation)
        await self.db.commit()
        await self.db.refresh(generation)
        return generation

    async def generate_and_save_file(self, length: int) -> tuple[str, str, str]:
        """
        Генерирует последовательность, сохраняет в БД и в файл в MinIO.
        """
        initial_fill, sequence = await self.generate_sequence(length)
        generation_id = str(uuid.uuid4())

        # Содержимое файла
        file_content = f"Generation ID: {generation_id}\nInitial Fill: {initial_fill}\nSequence: {sequence}"
        file_name = f"{generation_id}.txt"
        bucket_name = "generated"

        # Загружаем файл в MinIO (асинхронно)
        await self.file_service.upload_file(bucket_name, file_name, file_content.encode('utf-8'))
        file_url = f"{settings.MINIO_ENDPOINT}/{bucket_name}/{file_name}"  # Адаптируйте под ваши настройки

        # Сохраняем в БД с file_url
        generation = Generation(
            id=generation_id,
            length=length,
            initial_fill=initial_fill,
            sequence=sequence,
            file_url=file_url,
        )
        self.db.add(generation)
        await self.db.commit()

        return generation_id, initial_fill, file_url
