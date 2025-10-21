"""служба генерации"""#pylint: disable=W0706
import uuid
import requests
import random
from sqlalchemy.ext.asyncio import AsyncSession
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
        # Генерируем seed (initial_fill)
        seed = generate_seed.get_seed()
        lfsr = LFSR(seed=seed)
        winning_comb = generate_win_comb.extract_unique_digits(lfsr=lfsr, num_digits=count_of_winning_numbers, max_value=max_number)

        # Генерируем sequence с помощью LFSR (длина 128, как в твоём примере)
        
        sequence = lfsr.get_sequence(len_seq=128)

        # Сохраняем в БД (используем поле winer для winning_tickets_str)
        generation = Generation(
            length=128,  # Фиксированная длина для sequence
            initial_fill=str(seed),  # Конвертация seed в строку
            sequence=sequence,
            winer=winning_comb,  # Сохраняем выигранные билеты в поле winer
        )
        self.db.add(generation)
        await self.db.commit()
        await self.db.refresh(generation)

        # Возвращаем данные для JSON-ответа
        return {
            "winning_tickets": winning_comb,
            "sequence": sequence,
            "initial_fill": str(seed),
        }
