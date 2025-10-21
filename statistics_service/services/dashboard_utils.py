from typing import Any, Dict, List
from sqlalchemy import func, select
from statistics_service.models.statistics import StatisticsDB
from shared.database.database import AsyncSession


async def get_bit_distribution_data(db: AsyncSession) -> List[Dict[str, Any]]:
    """Данные для столбчатой гистограммы распределения 0 и 1"""
    # Группируем по диапазонам длин и считаем средние значения 0 и 1
    query = select(
        func.floor(StatisticsDB.sequence_length / 100).label("length_group"),
        func.avg(StatisticsDB.ones_count).label("avg_ones"),
        func.avg(StatisticsDB.zeros_count).label("avg_zeros"),
        func.count(StatisticsDB.id).label("sequence_count")
    ).group_by("length_group").order_by("length_group")
    
    result = await db.execute(query)
    rows = result.all()
    
    distribution_data = []
    for row in rows:
        length_range = f"{row.length_group * 100}-{(row.length_group + 1) * 100 - 1}"
        distribution_data.append({
            "length_range": length_range,
            "avg_ones": round(row.avg_ones, 2),
            "avg_zeros": round(row.avg_zeros, 2),
            "sequence_count": row.sequence_count
        })
    
    return distribution_data


async def get_worst_tests_data(db: AsyncSession) -> List[Dict[str, Any]]:
    """Данные о двух самых неуспешных тестах"""
    # Получаем все записи для анализа тестов
    query = select(StatisticsDB.tests_results)
    result = await db.execute(query)
    all_tests_results = result.scalars().all()
    
    # Анализируем успешность тестов
    test_stats = {}
    
    for test_result in all_tests_results:
        if not test_result:
            continue
            
        for test_name, test_data in test_result.items():
            if test_name not in test_stats:
                test_stats[test_name] = {"total": 0, "passed": 0}
            
            test_stats[test_name]["total"] += 1
            if test_data.get("result") == "PASS":
                test_stats[test_name]["passed"] += 1
    
    # Считаем процент успеха для каждого теста
    test_success_rates = []
    for test_name, stats in test_stats.items():
        success_rate = (stats["passed"] / stats["total"]) * 100 if stats["total"] > 0 else 0
        test_success_rates.append({
            "test_name": test_name,
            "success_rate": round(success_rate, 2),
            "total_sequences": stats["total"]
        })
    
    # Сортируем по успешности (от наименьшей) и берем два самых неуспешных
    test_success_rates.sort(key=lambda x: x["success_rate"])
    return test_success_rates[:2]


async def get_heatmap_data(db: AsyncSession) -> Dict[str, Any]:
    """Данные для хитмапа последних 10 последовательностей"""
    # Получаем последние 10 записей
    query = select(StatisticsDB).order_by(StatisticsDB.created_at.desc()).limit(10)
    result = await db.execute(query)
    recent_sequences = result.scalars().all()
    
    heatmap_data = {
        "sequence_ids": [],
        "test_names": set(),
        "results": []
    }
    
    for seq in recent_sequences:
        if not seq.tests_results:
            continue
            
        heatmap_data["sequence_ids"].append(str(seq.sequence_id))
        
        for test_name, test_data in seq.tests_results.items():
            heatmap_data["test_names"].add(test_name)
            heatmap_data["results"].append({
                "sequence_id": str(seq.sequence_id),
                "test_name": test_name,
                "result": test_data.get("result", "UNKNOWN"),
                "p_value": test_data.get("p_value")
            })
    
    heatmap_data["test_names"] = list(heatmap_data["test_names"])
    return heatmap_data