from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from shared.database.database import get_db, AsyncSession
from statistics_service.schemas.statistics import (
    StatisticsRequest, StatisticsResponseSchema, FileStatisticsResponseSchema, ErrorResponse)
from statistics_service.services.statistics_processor import StatisticsProcessor
from statistics_service.storage import get_minio_client, MinIOClient
from statistics_service.schemas.statistics import FileStatisticsRequest

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.post(
    "/sequence",
    response_model=StatisticsResponseSchema,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def analyze_sequence(request: StatisticsRequest,
                           db: AsyncSession=Depends(get_db),
                           minio : MinIOClient=Depends(get_minio_client)):
    """Анализ статистики для строковой последовательности"""
    try:
        processor = StatisticsProcessor(db,minio)
        result = await processor.process_sequence_statistics(request)
        
        return StatisticsResponseSchema(
            statistics_id=result.statistics_id,
            sequence_id=result.sequence_id,
            sequence_length=result.sequence_length,
            ones_count=result.ones_count,
            zeros_count=result.zeros_count,
            ones_proportion=result.ones_proportion,
            tests_passed=result.summary["tests_passed"],
            tests_total=result.summary["tests_total"],
            success_rate=result.summary["success_rate"],
            created_at=result.created_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Statistics processing error: {str(e)}"
        )

@router.post(
    "/file",
    response_model=FileStatisticsResponseSchema,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def analyze_file(file: UploadFile = File(...),
                       db : AsyncSession = Depends(get_db),
                       minio : MinIOClient=Depends(get_minio_client)):
    """Анализ статистики для файла"""
    try:
        processor = StatisticsProcessor(db,minio)
        content = await file.read()
        file_content = content.decode('utf-8')

        request = FileStatisticsRequest(file_content=file_content)
        result = await processor.process_file_statistics(request)
        
        return FileStatisticsResponseSchema(
            statistics_id=result.statistics_id,
            sequence_id=result.sequence_id,
            file_url=result.summary.get("file_url"),
            tests_passed=result.summary["tests_passed"],
            tests_total=result.summary["tests_total"],
            success_rate=result.summary["success_rate"],
            created_at=result.created_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File statistics processing error: {str(e)}"
        )
