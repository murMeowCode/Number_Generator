from sqlalchemy import Column, String, Integer, Float, DateTime, JSON
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from shared.database.database import Base

class StatisticsDB(Base):
    """модель статистической записи о конкретной последовательности"""
    __tablename__ = "statistics"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    sequence_id = Column(PGUUID(as_uuid=True), index=True)
    sequence_length = Column(Integer)
    ones_count = Column(Integer)
    zeros_count = Column(Integer)
    ones_proportion = Column(Float)
    tests_results = Column(JSON)  # JSON поле для результатов тестов
    summary = Column(JSON)  # JSON поле для суммарной статистики
    created_at = Column(DateTime, default=datetime.utcnow)
    file_reference = Column(String, nullable=True)
