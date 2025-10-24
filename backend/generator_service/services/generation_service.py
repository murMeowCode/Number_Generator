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
        seed, state = generate_seed.get_seed()
        lfsr = LFSR(seed=seed)
        sequence = lfsr.get_sequence(len_seq=length)
        return seed, sequence, state

    async def generate_and_save_in_db(self, length: int) -> Generation:
        """
        Генерирует последовательность и сохраняет в БД (без файла).
        Возвращает объект Generation.
        """
        seed, sequence, state = await self.generate_sequence(length)
        generation = Generation(
            seed=str(state),
            length=length,
            initial_fill=str(seed),
            sequence=sequence,
        )
        self.db.add(generation)
        await self.db.commit()
        await self.db.refresh(generation)
        return generation
    
    async def generate_winners_and_save(self, max_number: int, count_of_winning_numbers: int) -> dict:
        """
        Генерирует выигранные билеты, последовательность и сохраняет в БД.
        Возвращает словарь для JSON-ответа.
        """
        seed, state = generate_seed.get_seed()
        lfsr = LFSR(seed=seed)
        winning_comb, sequence = generate_win_comb.extract_unique_digits(lfsr=lfsr, num_digits=count_of_winning_numbers, max_value=max_number)

        generation = Generation(
            seed=str(state),
            length=128,
            initial_fill=str(seed),
            sequence=sequence,
            winer=str(winning_comb),
        )
        self.db.add(generation)
        await self.db.commit()
        await self.db.refresh(generation)

        return {
            'id':str(generation.id),
            "winning_tickets": winning_comb,
            "sequence": sequence,
            "initial_fill": str(seed),
            'seed': str(state)
        }

    async def generate_winners_verify(self, max_number: int, count_of_winning_numbers: int, seed: str) -> dict:
        """
        Генерирует выигранные билеты, последовательность и сохраняет в БД.
        Возвращает словарь для JSON-ответа.
        """
        seed, state = generate_seed.get_seed_verify(state=seed)
        lfsr = LFSR(seed=seed)
        winning_comb, sequence = generate_win_comb.extract_unique_digits(lfsr=lfsr, num_digits=count_of_winning_numbers, max_value=max_number)
        return winning_comb
        
    async def get_generation_by_id(self, generation_id: str) -> Optional[Generation]:
        """
        Получает генерацию по ID из БД.
        """
        
        result = await self.db.execute(
            select(Generation).where(Generation.id == generation_id)
        )
        return result.scalar_one_or_none()
    

    async def get_all_generations_for_dashboard(self):
        """
        Возвращает список ВСЕХ генераций: отсортировано по created_at desc.
        """
        stmt = select(Generation.seed, Generation.created_at).order_by(Generation.created_at.desc())
        result = await self.db.execute(stmt)
        # Изменено: result.all() вернет список кортежей (seed, created_at)
        return result.all()
