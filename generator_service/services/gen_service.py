"""служба генерации"""#pylint: disable=W0706
import random
from sqlalchemy import UUID
from celery import chain
from generator_service.models.generation import Generation
from generator_service.schemas.generation import GenerationResult
from generator_service.services.file_service import FileService
from generator_service.gen_celery.tasks.statistics_tasks import (dieharder_test_task,
                                                nist_sts_test_task, testu01_test_task)
from shared.database.database import AsyncSessionLocal


class GeneratorService:
    """Служба генерации"""
    async def _create_generation_record(self, user_id: UUID, length: int) -> UUID:
        """Создание записи о генерации в БД"""
        async with AsyncSessionLocal() as db:
            generation = Generation(
                user_id=user_id,
                length=length,
                status="pending"
            )
            db.add(generation)
            await db.commit()
            await db.refresh(generation)
            return generation.id

    async def _update_generation_completed(self, generation_id: UUID, preview: str,
                                         minio_path: str, test_results: dict):
        """Обновление записи о завершенной генерации"""
        async with AsyncSessionLocal() as db:
            generation = await db.get(Generation, generation_id)
            if generation:
                generation.preview = preview
                generation.minio_json_path = minio_path
                generation.test_results = test_results
                await db.commit()

    async def _save_json_to_minio(self, json_document: GenerationResult,
                                  generation_id: UUID) -> str:
        """Сохранение JSON документа в MinIO"""
        file_service = FileService()
        return await file_service.save_json_to_minio(
            json_document.dict(),  # конвертируем Pydantic модель в dict
            generation_id
        )

    async def _save_temp_sequence(self, sequence: str, generation_id: UUID) -> str:
        """Сохранение временной последовательности для тестов"""
        file_service = FileService()
        return await file_service.save_temp_sequence(sequence, generation_id)

    async def generate_sequence(self, user_id: UUID, length: int) -> dict:
        """Основной метод генерации"""

        # 1. Создаем запись в БД
        generation_id = await self._create_generation_record(user_id, length)

        try:
            # 2. Генерируем последовательность (заглушка)
            sequence = await self._generate_random_sequence(length)
            preview = sequence[:10]

            # 3. Сохраняем в MinIO временный файл для тестов
            temp_file_path = await self._save_temp_sequence(sequence, generation_id)

            # 4. Запускаем синхронное тестирование
            test_results = await self._run_statistical_tests(temp_file_path)

            # 5. Формируем итоговый JSON документ
            json_document = GenerationResult(
                initial_state={},  # пока пустое, будет добавлено позже
                final_sequence=sequence,
                test_results=test_results
            )

            # 6. Сохраняем JSON в MinIO
            minio_path = await self._save_json_to_minio(json_document, generation_id)

            # 7. Обновляем запись в БД
            await self._update_generation_completed(generation_id,
                                                    preview, minio_path, test_results)

            return {
                "generation_id": generation_id,
                "preview": preview,
                "test_results": test_results,
                "status": "completed"
            }

        except Exception as e:
            raise e

    async def _generate_random_sequence(self, length: int) -> str:
        """Заглушка генератора - равномерное распределение 0 и 1"""
        return ''.join(str(random.randint(0, 1)) for _ in range(length))

    async def _run_statistical_tests(self, file_path: str) -> dict:
        """Запуск всех статистических тестов через Celery синхронно"""

        # Создаем цепочку задач для выполнения всех тестов
        task_chain = chain(
            nist_sts_test_task.s(file_path),
            dieharder_test_task.s(),
            testu01_test_task.s()
        )

        # Запускаем синхронно (ждем завершения)
        result = task_chain.apply()

        return result.get()  # ждем результат

async def get_generator_service() -> GeneratorService:
    """
    Зависимость для получения сервиса генерации
    """
    return GeneratorService()
