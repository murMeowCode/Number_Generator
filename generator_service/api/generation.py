from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import FileResponse
import tempfile
import os
from generator_service.schemas.generation import (
    GenerateRequest,
    GenerateResponse,
    GenerateFileRequest,
    GenerateFileResponse,
    GenerateWinnersRequest,  # Добавлено
    GenerateWinnersResponse,  # Добавлено
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
            id=str(generation.id),
            initial_fill=generation.initial_fill,
            sequence=generation.sequence
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации: {str(e)}")

@router.post("/generate-file")
async def generate_sequence_file(
    request: GenerateRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Генерирует последовательность, сохраняет в БД и возвращает данные в файле .txt.
    """
    file_service = FileService()
    generation_service = GenerationService(db, file_service)
    
    try:
        generation = await generation_service.generate_and_save_in_db(request.length)
        
        # Формируем содержимое файла .txt
        content = f"ID: {str(generation.id)}\nInitial Fill: {generation.initial_fill}\nSequence: {generation.sequence}\n"
        
        # Создаём временный файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Возвращаем файл как ответ (клиент скачает его как "generation.txt")
        return FileResponse(
            path=temp_file_path,
            media_type='text/plain',
            filename=f'{generation.id}.txt'  # Имя файла для скачивания
        )
    
    except Exception as e:
        # Очистка в случае ошибки (удаляем временный файл, если он создан)
        if 'temp_file_path' in locals():
            os.unlink(temp_file_path)
        raise HTTPException(status_code=500, detail=f"Ошибка генерации: {str(e)}")

@router.post("/generate-winners", response_model=GenerateWinnersResponse)
async def generate_winners(
    request: GenerateWinnersRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Генерирует выигранные билеты, последовательность, сохраняет в БД и возвращает в ответе.
    """
    file_service = FileService()  # Создаем FileService, как в твоих эндпоинтах
    generation_service = GenerationService(db, file_service)
    
    # Валидация входных данных (добавь, если нужно, но FastAPI сам проверит по схеме)
    if request.max_number < request.count_of_winning_numbers or request.count_of_winning_numbers <= 0:
        raise HTTPException(status_code=400, detail="Неверные параметры: max_number должен быть >= count_of_winning_numbers > 0")
    
    try:
        result = await generation_service.generate_winners_and_save( 
            max_number=request.max_number, count_of_winning_numbers=request.count_of_winning_numbers
        )
        return GenerateWinnersResponse(
            winning_tickets=result["winning_tickets"],
            sequence=result["sequence"],
            initial_fill=result["initial_fill"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации: {str(e)}")
    
@router.get("/generation/{id}", response_model=GenerateResponse)
async def get_generation(
    id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Получает информацию о генерации по ID из БД.
    """
    file_service = FileService()  # Если нужен для сервиса
    generation_service = GenerationService(db, file_service)
    
    try:
        generation = await generation_service.get_generation_by_id(id)  # Новый метод в сервисе
        if not generation:
            raise HTTPException(status_code=404, detail="Генерация не найдена")
        
        return GenerateResponse(
            id=str(generation.id),
            initial_fill=generation.initial_fill,
            sequence=generation.sequence
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения генерации: {str(e)}")