from pydantic import BaseModel
from typing import List, Dict, Any

class BitDistributionItem(BaseModel):
    length_range: str
    avg_ones: float
    avg_zeros: float
    sequence_count: int

class WorstTestInfo(BaseModel):
    test_name: str
    success_rate: float
    total_sequences: int

class HeatmapData(BaseModel):
    sequence_ids: List[str]
    test_names: List[str]
    results: List[Dict[str, Any]]

class DashboardOverviewSchema(BaseModel):
    total_sequences: int
    avg_sequence_length: float
    avg_success_rate: float
    bit_distribution: List[BitDistributionItem]
    worst_tests: List[WorstTestInfo]
    heatmap_data: HeatmapData