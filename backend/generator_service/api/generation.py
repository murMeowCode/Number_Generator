#pylint: disable=C0413
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import FileResponse
import tempfile
import os
from generator_service.api.side_randoms import get_python_random_sequence, get_random_org_sequence
from generator_service.schemas.generation import (
    GenerateRequest,
    GenerateResponse,
    GenerateWinnersVerifyRequest,
    GenerateWinnersVerifyResponse,
    GenerateWinnersRequest,
    GenerateWinnersResponse,
    GenerationDashboardItem
)
from generator_service.services.generation_service import GenerationService
from generator_service.services.file_service import FileService
from shared.database.database import get_db
from shared.utils.redis_client import (cache_generation_dashboard,
                                       invalidate_generation_dashboard_cache)

router = APIRouter(prefix="/generate")

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
        
        await invalidate_generation_dashboard_cache()
        
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
        
        content = f"ID: {str(generation.id)}\nInitial Fill: {generation.initial_fill}\nSequence: {generation.sequence}\n"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        await invalidate_generation_dashboard_cache()
        
        return FileResponse(
            path=temp_file_path,
            media_type='text/plain',
            filename=f'{generation.id}.txt'
        )
    
    except Exception as e:
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
    file_service = FileService()
    generation_service = GenerationService(db, file_service)

    if request.max_number < request.count_of_winning_numbers or request.count_of_winning_numbers <= 0:
        raise HTTPException(status_code=400, detail="Неверные параметры: max_number должен быть >= count_of_winning_numbers > 0")
    
    try:
        result = await generation_service.generate_winners_and_save( 
            max_number=request.max_number, count_of_winning_numbers=request.count_of_winning_numbers
        )
        
        await invalidate_generation_dashboard_cache()
        
        return GenerateWinnersResponse(
            id=str(result['id']),
            winning_tickets=result["winning_tickets"],
            sequence=result["sequence"],
            initial_fill=result["initial_fill"],
            seed = result['seed']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации: {str(e)}")

@cache_generation_dashboard(ttl=1800)
@router.get("/dashboard/generations", response_model=List[GenerationDashboardItem])
async def get_generations_for_dashboard(
    db: AsyncSession = Depends(get_db),
):
    """
    Получает список генераций для дашборда, адаптированных для фронтенда.
    """
    file_service = FileService()
    generation_service = GenerationService(db, file_service)
    
    try:
        # Изменено: теперь generations — список кортежей (seed, created_at)
        generations = await generation_service.get_all_generations_for_dashboard()
        
        result = []
        for seed, created_at in generations:
            seed_front = seed[:10] if seed else ""
     
            result.append(GenerationDashboardItem(
                created_at=created_at.isoformat() if created_at else None,
                seed=seed_front
            ))
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения генераций для дашборда: {str(e)}")

@router.get("/generation/{id}", response_model=GenerateResponse)
async def get_generation(
    id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Получает информацию о генерации по ID из БД.
    """
    file_service = FileService()
    generation_service = GenerationService(db, file_service)
    
    try:
        generation = await generation_service.get_generation_by_id(id)
        if not generation:
            raise HTTPException(status_code=404, detail="Генерация не найдена")
        
        return GenerateResponse(
            id=str(generation.id),
            initial_fill=generation.initial_fill,
            sequence=generation.sequence
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения генерации: {str(e)}")
    

@router.post("/generate-winners/verify", response_model=GenerateWinnersVerifyResponse)
async def generate_winners(
    request: GenerateWinnersVerifyRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Генерирует выигранные билеты, последовательность, сохраняет в БД и возвращает в ответе.
    """
    file_service = FileService()
    generation_service = GenerationService(db, file_service)

    if request.max_number < request.count_of_winning_numbers or request.count_of_winning_numbers <= 0:
        raise HTTPException(status_code=400, detail="Неверные параметры: max_number должен быть >= count_of_winning_numbers > 0")
    
    try:
        return GenerateWinnersVerifyResponse(
            winning_tickets= await generation_service.generate_winners_verify( 
            max_number=request.max_number, count_of_winning_numbers=request.count_of_winning_numbers,
            seed=request.seed
        )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации: {str(e)}")
    
@router.get("/generate/side/{length}")
async def generate_sequences(length: int):
    """
    Генерация случайных последовательностей
    
    - **length**: Длина последовательности
    """

    random_org_seq = get_random_org_sequence(length)
    python_seq = get_python_random_sequence(length)
    
    return {
        "random_org": random_org_seq,
        "python_random": python_seq
    }
