from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from generator_service.schemas.generation import (
    GenerateRequest,
    GenerateResponse,
    GenerateFileRequest,
    GenerateFileResponse,
)
from generator_service.services.generation_service import GenerationService
from generator_service.services.file_service import FileService
from shared.database.database import get_db  # Асинхронная зависимость для получения сессии БД

router = APIRouter()

# Эндпоинт для генерации в памяти (с сохранением в БД)
@router.post("/generate", response_model=GenerateResponse)
async def generate_sequence(
    request: GenerateRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Генерирует последовательность, сохраняет в БД и возвращает в ответе.
    """
    file_service = FileService()
    generation_service = GenerationService(db, file_service)
    
    try:
        generation = await generation_service.generate_and_save_in_db(request.length)
        return GenerateResponse(
            initial_fill=generation.initial_fill,
            sequence=generation.sequence
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации: {str(e)}")

# Эндпоинт для генерации в файл (с сохранением в БД и MinIO)
@router.post("/generate-file", response_model=GenerateFileResponse)
async def generate_sequence_to_file(
    request: GenerateFileRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Генерирует, сохраняет в БД и в файл, возвращает ID, начальное заполнение, победителей и URL.
    """
    file_service = FileService()  # Создаем FileService (предполагаем, что он не зависит от db; если зависит, передайте db)
    generation_service = GenerationService(db, file_service)
    
    try:
        generation_id, initial_fill, winner, file_url = await generation_service.generate_and_save_file(request.length, request.num_winners)
        return GenerateFileResponse(
            generation_id=generation_id,
            initial_fill=initial_fill,
            winner=winner,
            file_url=file_url,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации файла: {str(e)}")
