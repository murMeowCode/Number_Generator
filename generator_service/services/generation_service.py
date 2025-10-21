"""служба генерации"""#pylint: disable=W0706
from typing import Optional
import uuid
import requests
import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
from generator_service.services.file_service import FileService
from generator_service.models.generation import Generation
from generator_service.services.lfsr.lfsr_base import LFSR
from generator_service.services.lfsr.utils import generate_seed, generate_win_comb

class GenerationService:
    def __init__(self, db: AsyncSession, file_service: FileService):
        self.db = db
        self.file_service = file_service

    async def generate_sequence(self, length: int) -> tuple[str, str]:
        """
        Генерирует начальное заполнение и последовательность (заглушки).
        """
        seed = generate_seed.get_seed()
        lfsr = LFSR(seed=seed)
        sequence = lfsr.get_sequence(len_seq=length)
        return seed, sequence

    async def generate_and_save_in_db(self, length: int) -> Generation:
        """
        Генерирует последовательность и сохраняет в БД (без файла).
        Возвращает объект Generation.
        """
        seed, sequence = await self.generate_sequence(length)
        generation = Generation(
            length=length,
            initial_fill=str(seed),
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
    
    async def generate_winners_and_save(self, max_number: int, count_of_winning_numbers: int) -> dict:
        """
        Генерирует выигранные билеты, последовательность и сохраняет в БД.
        Возвращает словарь для JSON-ответа.
        """
        seed = generate_seed.get_seed()
        lfsr = LFSR(seed=seed)
        winning_comb, sequence = generate_win_comb.extract_unique_digits(lfsr=lfsr, num_digits=count_of_winning_numbers, max_value=max_number)

        generation = Generation(
            length=128,
            initial_fill=str(seed),
            sequence=sequence,
            winer=str(winning_comb),
        )
        self.db.add(generation)
        await self.db.commit()
        await self.db.refresh(generation)

        return {
            "winning_tickets": winning_comb,
            "sequence": sequence,
            "initial_fill": str(seed),
        }

    async def get_generation_by_id(self, generation_id: str) -> Optional[Generation]:
        """
        Получает генерацию по ID из БД.
        """
        
        result = await self.db.execute(
            select(Generation).where(Generation.id == generation_id)
        )
        return result.scalar_one_or_none()