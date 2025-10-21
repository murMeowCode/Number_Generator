"""# generator_service/api/endpoints/generation.py"""#pylint: disable=W0707
from generator_service.schemas.generation import (
    GenerateRequest,
    GenerateResponse,
    GenerateFileRequest,
    GenerateFileResponse,
)
from generator_service.models.generation import Generation
from shared.database.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from generator_service.services.generation_service import GenerationService
from generator_service.services.file_service import FileService
from shared.database.database import get_db  # Используем вашу асинхронную зависимость


router = APIRouter(prefix="/generator", tags=["generator"])



router = APIRouter()

def get_generation_service(db: AsyncSession = Depends(get_db), file_service: FileService = Depends()) -> GenerationService:
    return GenerationService(db, file_service)

# Эндпоинт для генерации в памяти (с сохранением в БД)
@router.post("/generate", response_model=GenerateResponse)
async def generate_sequence(
    request: GenerateRequest,
    service: GenerationService = Depends(get_generation_service),
):
    """
    Генерирует последовательность, сохраняет в БД и возвращает в ответе.
    """
    try:
        generation = await service.generate_and_save_in_db(request.length)
        return GenerateResponse(initial_fill=generation.initial_fill, sequence=generation.sequence)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации: {str(e)}")

# Эндпоинт для генерации в файл (с сохранением в БД и MinIO)
@router.post("/generate-file", response_model=GenerateFileResponse)
async def generate_sequence_to_file(
    request: GenerateFileRequest,
    service: GenerationService = Depends(get_generation_service),
):
    """
    Генерирует, сохраняет в БД и в файл, возвращает ID, начальное заполнение и URL.
    """
    try:
        generation_id, initial_fill, file_url = await service.generate_and_save_file(request.length)
        return GenerateFileResponse(
            generation_id=generation_id,
            initial_fill=initial_fill,
            file_url=file_url,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации файла: {str(e)}")
