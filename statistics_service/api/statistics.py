import logging
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy import func, select
from shared.database.database import get_db, AsyncSession
from statistics_service.models.statistics import StatisticsDB
from statistics_service.schemas.dashboard import DashboardOverviewSchema
from statistics_service.schemas.statistics import (
    StatisticsRequest, StatisticsResponseSchema, FileStatisticsResponseSchema, ErrorResponse)
from statistics_service.services.dashboard_utils import get_bit_distribution_data, get_heatmap_data, get_worst_tests_data
from statistics_service.services.statistics_processor import StatisticsProcessor
from statistics_service.storage import get_minio_client, MinIOClient
from statistics_service.schemas.statistics import FileStatisticsRequest

router = APIRouter(prefix="/statistics", tags=["statistics"])

logger = logging.getLogger(__name__)

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
                           db: AsyncSession = Depends(get_db),
                           minio: MinIOClient = Depends(get_minio_client)):
    """Анализ статистики для строковой последовательности"""
    logger.info(f"Starting sequence analysis for sequence_id: {request.sequence_id}, "
                f"sequence_length: {len(request.sequence)}")
    
    try:
        logger.debug("Creating StatisticsProcessor instance")
        processor = StatisticsProcessor(db, minio)
        
        logger.info("Processing sequence statistics")
        result = await processor.process_sequence_statistics(request)
        
        logger.info(f"Successfully processed statistics. Statistics ID: {result.statistics_id}, "
                   f"Tests passed: {result.summary['tests_passed']}/{result.summary['tests_total']}")
        
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
            created_at=result.created_at,
            tests_results=result.tests_results
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
            created_at=result.created_at,
            tests_results=result.tests_results
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File statistics processing error: {str(e)}"
        )

@router.get(
    "/{sequence_id}",
    response_model=StatisticsResponseSchema,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def get_statistics(
    sequence_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Получение результатов статистики по ID"""
    logger.info(f"Getting statistics by sequence_ID: {sequence_id}")
    
    try:
        logger.debug("Creating StatisticsProcessor instance")
        processor = StatisticsProcessor(db, None)  # MinIO не нужен для чтения
        
        logger.info("Fetching statistics from database")
        result = await processor.get_statistics_by_id(sequence_id)
        
        if not result:
            logger.warning(f"Statistics not found for sequence_ID: {sequence_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Statistics record not found"
            )
        
        logger.info(f"Successfully fetched statistics. Statistics ID: {result.statistics_id}")
        
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
            created_at=result.created_at,
            tests_results=result.tests_results
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching statistics by ID {sequence_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching statistics: {str(e)}"
        )

@router.get(
    "/dashboard/overview",
    response_model=DashboardOverviewSchema,
    status_code=status.HTTP_200_OK
)
async def get_dashboard_overview(db: AsyncSession = Depends(get_db)):
    """Получение обзорной статистики для дашборда"""
    logger.info("Fetching dashboard overview data")
    
    try:
        # 1. Всего последовательностей
        total_sequences_query = select(func.count(StatisticsDB.id))
        total_result = await db.execute(total_sequences_query)
        total_sequences = total_result.scalar()

        # 2. Средняя длина последовательностей
        avg_length_query = select(func.avg(StatisticsDB.sequence_length))
        avg_length_result = await db.execute(avg_length_query)
        avg_sequence_length = round(avg_length_result.scalar() or 0, 2)

        # 3. Общий средний успех прохождения тестов
        avg_success_query = select(func.avg(StatisticsDB.summary['success_rate'].as_float()))
        avg_success_result = await db.execute(avg_success_query)
        avg_success_rate = round(avg_success_result.scalar() or 0, 2)

        # 4. Данные для столбчатой гистограммы распределения 0 и 1
        bit_distribution_data = await get_bit_distribution_data(db)

        # 5. Два самых неуспешных теста
        worst_tests_data = await get_worst_tests_data(db)

        # 6. Данные для хитмапа последних 10 последовательностей
        heatmap_data = await get_heatmap_data(db)

        return DashboardOverviewSchema(
            total_sequences=total_sequences,
            avg_sequence_length=avg_sequence_length,
            avg_success_rate=avg_success_rate,
            bit_distribution=bit_distribution_data,
            worst_tests=worst_tests_data,
            heatmap_data=heatmap_data
        )
        
    except Exception as e:
        logger.error(f"Error fetching dashboard data: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Dashboard data fetching error: {str(e)}"
        )
