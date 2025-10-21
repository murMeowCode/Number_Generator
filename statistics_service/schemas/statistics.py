from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum
from uuid import UUID

class TestResult(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"
    SKIP = "SKIP"

class TestType(str, Enum):
    FREQUENCY = "frequency"
    RUNS = "runs"
    SERIAL = "serial"
    AUTOCORRELATION = "autocorrelation"
    POKER = "poker"
    CUMULATIVE_SUMS = "cumulative_sums"
    LONGEST_RUNS = "longest_runs"
    MATRIX_RANK = "matrix_rank"

# Схемы для запросов
class StatisticsRequest(BaseModel):
    sequence: str = Field(description="Последовательность из 0 и 1")
    sequence_id: UUID = Field(description="ID последовательности")

class FileStatisticsRequest(BaseModel):
    file_content: str = Field(description="Содержимое файла для анализа")

# Схемы для ответов
class TestResultDetail(BaseModel):
    p_value: Optional[float] = None
    result: TestResult
    details: Dict[str, Any] = Field(default_factory=dict)

class StatisticsResponse(BaseModel):
    statistics_id: UUID
    sequence_id: UUID
    sequence_length: int
    ones_count: int
    zeros_count: int
    ones_proportion: float
    tests_results: Dict[TestType, TestResultDetail]
    summary: Dict[str, Any]
    created_at: datetime

class StatisticsResponseSchema(BaseModel):
    statistics_id: UUID
    sequence_id: UUID
    sequence_length: int
    ones_count: int
    zeros_count: int
    ones_proportion: float
    tests_passed: int
    tests_total: int
    success_rate: float
    created_at: datetime

class FileStatisticsResponseSchema(BaseModel):
    statistics_id: UUID
    sequence_id: UUID
    file_url: Optional[str]
    tests_passed: int
    tests_total: int
    success_rate: float
    created_at: datetime

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None