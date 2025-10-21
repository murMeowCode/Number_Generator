"""# generator_service/api/endpoints/generation.py"""#pylint: disable=W0707
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import UUID, select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from authentication_service.core.auth import get_current_user
from generator_service.schemas.generation import (GenerationHistoryResponse,
GenerationRequest, GenerationResponse, TestResultSummary, GenerationHistoryItem)
from generator_service.services.gen_service import get_generator_service, GeneratorService
from generator_service.models.generation import Generation
from shared.database.database import get_db

router = APIRouter(prefix="/generator", tags=["generator"])


@router.post("/generate", response_model=GenerationResponse, status_code=status.HTTP_201_CREATED)
async def create_generation(
    request: GenerationRequest,
    current_user: dict = Depends(get_current_user),
    generator_service: GeneratorService = Depends(get_generator_service)
):
    """
    Создание новой генерации случайной последовательности
    """
    try:
        # Валидация длины
        if request.length <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Length must be positive"
            )

        if request.length > 10000000:  # Ограничение на максимальную длину
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Length too large. Maximum allowed is 10,000,000"
            )

        user_id = UUID(current_user["user_id"])
        result = await generator_service.generate_sequence(user_id, request.length)

        return GenerationResponse(
            generation_id=result["generation_id"],
            preview=result["preview"],
            test_results=TestResultSummary(**result["test_results"]),
            status=result["status"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Generation failed: {str(e)}"
        )

@router.get("/history", response_model=GenerationHistoryResponse)
async def get_generation_history(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получение истории генераций текущего пользователя
    """
    try:
        user_id = UUID(current_user["user_id"])

        stmt = select(Generation).where(
            Generation.user_id == user_id
        ).order_by(desc(Generation.created_at))

        result = await db.execute(stmt)
        generations = result.scalars().all()

        history_items = []
        for gen in generations:
            # Преобразуем test_summary из JSONB в словарь если нужно
            test_summary = gen.test_results if gen.test_results else {
                "nist_sts": "unknown",
                "dieharder": "unknown", 
                "testu01": "unknown"
            }

            history_items.append(GenerationHistoryItem(
                generation_id=gen.id,
                length=gen.length,
                preview=gen.preview or "",
                test_summary=TestResultSummary(**test_summary),
                created_at=gen.created_at.isoformat() if gen.created_at else ""
            ))

        return GenerationHistoryResponse(generations=history_items)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch generation history: {str(e)}"
        )
