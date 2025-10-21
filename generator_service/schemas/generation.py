"""схемы"""
from typing import List
from uuid import UUID
from pydantic import BaseModel

class GenerationRequest(BaseModel):
    length: int = 1000000

class TestResultSummary(BaseModel):
    nist_sts: str
    dieharder: str
    testu01: str

class GenerationResponse(BaseModel):
    generation_id: UUID
    preview: str
    test_results: TestResultSummary
    status: str

class GenerationHistoryItem(BaseModel):
    generation_id: UUID
    length: int
    preview: str
    status: str
    test_summary: TestResultSummary
    created_at: str

class GenerationHistoryResponse(BaseModel):
    generations: List[GenerationHistoryItem]

class GenerationResult(BaseModel):
    """схема результата"""
    initial_state: dict  # начальное заполнение (пока пустой dict)
    final_sequence: str  # полная сгенерированная последовательность (1млн символов)
    test_results: dict  # результаты всех тестов

    # Пример структуры test_results:
    # {
    #   "nist_sts": {
    #     "status": "passed",  # passed/failed
    #     "p_value": 0.234,
    #     "details": {...}
    #   },
    #   "dieharder": {
    #     "status": "failed",
    #     "p_value": 0.001,
    #     "details": {...}
    #   },
    #   "testu01": {
    #     "status": "passed",
    #     "p_value": 0.567,
    #     "details": {...}
    #   }
    # }
