import logging
import uuid
import re
from datetime import datetime
from typing import List, Tuple
from statistics_service.schemas.statistics import (
    StatisticsRequest, FileStatisticsRequest, StatisticsResponse, TestResult
)
from statistics_service.services.stat_service import SequenceTester
from statistics_service.models.statistics import StatisticsDB
from statistics_service.storage import MinIOClient
from shared.database.database import AsyncSession

logger = logging.getLogger(__name__)

class StatisticsProcessor:
    def __init__(self, db : AsyncSession, minio_client : MinIOClient):
        self.db = db
        self.minio_client = minio_client
    
    def _parse_sequence(self, sequence_str: str) -> Tuple[List[int], int, int]:
        """Парсинг последовательности из строки"""
        cleaned = re.sub(r'\s+', '', sequence_str)
        
        if not re.match(r'^[01]+$', cleaned):
            raise ValueError("Sequence must contain only 0s and 1s")
        
        bits = [int(bit) for bit in cleaned]
        ones = sum(bits)
        zeros = len(bits) - ones
        
        return bits, ones, zeros
    
    def _parse_file_content(self, file_content: str) -> Tuple[str, str, List[int]]:
        """Парсинг содержимого файла"""
        try:
            lines = file_content.strip().split('\n')
            
            seed_data = None
            generation_id = None
            sequence_data = None
            
            for line in lines:
                if line.startswith('Seed:'):
                    seed_data = line.replace('Seed:', '').strip()
                elif line.startswith('Generation ID:'):
                    generation_id = line.replace('Generation ID:', '').strip()
                elif line.startswith('Sequence:'):
                    sequence_data = line.replace('Sequence:', '').strip()
                elif sequence_data is not None and line.strip():
                    sequence_data += line.strip()
            
            if not generation_id or not sequence_data:
                generation_id = str(uuid.uuid4())
                sequence_data = re.sub(r'[^01]', '', file_content)
                if not sequence_data:
                    raise ValueError("No binary sequence found in file")
            
            bits, ones, zeros = self._parse_sequence(sequence_data)
            
            return generation_id, seed_data or "unknown", bits
            
        except Exception as e:
            generation_id = str(uuid.uuid4())
            sequence_data = re.sub(r'[^01]', '', file_content)
            if not sequence_data:
                sequence_data = ''.join(['0', '1'] * 100)
            
            bits, ones, zeros = self._parse_sequence(sequence_data)
            return generation_id, "unknown", bits
    
    async def process_sequence_statistics(self, request: StatisticsRequest) -> StatisticsResponse:
        """Обработка статистики для строковой последовательности"""
        bits, ones, zeros = self._parse_sequence(request.sequence)
        sequence_length = len(bits)
        ones_proportion = ones / sequence_length
        
        tester = SequenceTester(bits)
        tests_results = tester.run_all_tests()
        
        passed_tests = sum(1 for result in tests_results.values() 
                         if result.result in [TestResult.PASS, TestResult.WARNING])
        total_tests = len(tests_results)
        success_rate = (passed_tests / total_tests) * 100
        
        statistics_id = str(uuid.uuid4())
        response = StatisticsResponse(
            statistics_id=statistics_id,
            sequence_id=request.sequence_id,
            sequence_length=sequence_length,
            ones_count=ones,
            zeros_count=zeros,
            ones_proportion=ones_proportion,
            tests_results=tests_results,
            summary={
                "tests_passed": passed_tests,
                "tests_total": total_tests,
                "success_rate": success_rate
            },
            created_at=datetime.now()
        )
        
        await self._save_to_database(response)
        
        return response
    
    async def process_file_statistics(self, request: FileStatisticsRequest) -> StatisticsResponse:
        """Обработка статистики для файла"""
        generation_id, seed_data, bits = self._parse_file_content(request.file_content)
        sequence_length = len(bits)
        ones = sum(bits)
        zeros = sequence_length - ones
        ones_proportion = ones / sequence_length
        
        tester = SequenceTester(bits)
        tests_results = tester.run_all_tests()
        
        passed_tests = sum(1 for result in tests_results.values() 
                         if result.result in [TestResult.PASS, TestResult.WARNING])
        total_tests = len(tests_results)
        success_rate = (passed_tests / total_tests) * 100
        
        filename = f"uploaded/{generation_id}_analysis.txt"
        file_url = await self.minio_client.upload_file(
            bucket_name="uploaded",
            filename=filename,
            content=request.file_content
        )
        
        statistics_id = str(uuid.uuid4())
        response = StatisticsResponse(
            statistics_id=statistics_id,
            sequence_id=generation_id,
            sequence_length=sequence_length,
            ones_count=ones,
            zeros_count=zeros,
            ones_proportion=ones_proportion,
            tests_results=tests_results,
            summary={
                "tests_passed": passed_tests,
                "tests_total": total_tests,
                "success_rate": success_rate,
                "seed_data": seed_data,
                "file_url": file_url
            },
            created_at=datetime.now()
        )
        
        await self._save_to_database(response, file_reference=file_url)
        
        return response
    
    async def _save_to_database(self, response: StatisticsResponse, file_reference: str = None):
        """Сохранение результатов в базу данных"""
        try:
            # Проверяем что db инициализирован
            if self.db is None:
                print("Database connection is None in _save_to_database")
                raise ValueError("Database connection is not initialized")
            
            # Логируем начало сохранения
            print(f"Saving statistics to database. Statistics ID: {response.statistics_id}")
            
            # Создаем запись с проверкой данных
            tests_results = {}
            if response.tests_results:
                tests_results = {
                    test_type.value: {
                        "p_value": result.p_value,
                        "result": result.result.value,
                        "details": result.details
                    }
                    for test_type, result in response.tests_results.items()
                    if result and hasattr(result, 'result') and result.result
                }
            
            db_record = StatisticsDB(
                id=response.statistics_id,
                sequence_id=response.sequence_id,
                sequence_length=response.sequence_length,
                ones_count=response.ones_count,
                zeros_count=response.zeros_count,
                ones_proportion=response.ones_proportion,
                tests_results=tests_results,
                summary=response.summary,
                file_reference=file_reference
            )
            
            print(f"Created database record: {db_record}")
            
            # Сохраняем в базу
            self.db.add(db_record)
            await self.db.commit()  # Если нужно явное подтверждение
            
            print(f"Successfully saved statistics to database. Statistics ID: {response.statistics_id}")
            
        except Exception as e:
            print(f"Error saving to database for statistics_id {response.statistics_id}: {str(e)}")
            # Откатываем транзакцию если была начата
            if self.db:
                await self.db.rollback()
            raise
