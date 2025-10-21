"""задачи селери""" #pylint: disable=W1514, W0718
import math
from typing import Any, Dict
from generator_service.gen_celery.app import app


def _nist_sts_test(sequence: str) -> Dict[str, Any]:
    """
    Заглушка теста NIST STS с детализацией по трем подтестам
    """
    bits = [int(bit) for bit in sequence]
    n = len(bits)

    test_details = {}

    # 1. Frequency (Monobit) Test
    ones_count = sum(bits)
    zero_count = n - ones_count
    s = abs(ones_count - zero_count)
    p_value_freq = math.erfc(s / (math.sqrt(n) * math.sqrt(2.0)))
    test_details["frequency_monobit"] = {
        "p_value": p_value_freq,
        "status": "passed" if p_value_freq > 0.01 else "failed",
        "description": "Проверка баланса нулей и единиц в последовательности"
    }

    # 2. Runs Test
    runs = 1
    for i in range(1, n):
        if bits[i] != bits[i-1]:
            runs += 1

    expected_runs = (2 * ones_count * zero_count) / n + 1
    variance = (2 * ones_count * zero_count * (2 * ones_count * zero_count - n)) / (n * n * (n - 1))

    if variance == 0:
        z = 0
    else:
        z = abs(runs - expected_runs) / math.sqrt(variance)

    p_value_runs = math.erfc(z / math.sqrt(2))
    test_details["runs"] = {
        "p_value": p_value_runs,
        "status": "passed" if p_value_runs > 0.01 else "failed",
        "description": "Проверка количества серий одинаковых битов"
    }

    # 3. Cumulative Sums Test
    cumulative_sum = 0
    max_cumulative = 0
    for bit in bits:
        cumulative_sum += (1 if bit == 1 else -1)
        max_cumulative = max(max_cumulative, abs(cumulative_sum))

    p_value_cs = math.exp(-2 * max_cumulative * max_cumulative / n)
    test_details["cumulative_sums"] = {
        "p_value": p_value_cs,
        "status": "passed" if p_value_cs > 0.01 else "failed",
        "description": "Проверка кумулятивных сумм последовательности"
    }

    # Общий результат NIST STS
    passed_tests = sum(1 for test in test_details.values() if test["status"] == "passed")
    overall_status = "passed" if passed_tests >= 2 else "failed"  # 2 из 3 тестов должны пройти

    return {
        "status": overall_status,
        "p_value": min(test["p_value"] for test in test_details.values()),
        "details": test_details,
        "summary": f"Пройдено {passed_tests} из {len(test_details)} тестов"
    }

def _dieharder_test(sequence: str) -> Dict[str, Any]:
    """
    Заглушка теста Dieharder с детализацией по трем подтестам
    """
    bits = [int(bit) for bit in sequence]
    n = len(bits)

    test_details = {}

    # 1. Birthday Spacings Test
    numbers = []
    for i in range(0, n - 7, 8):
        num = int(sequence[i:i+8], 2)
        numbers.append(num)

    if len(numbers) > 1:
        numbers.sort()
        spacings = [numbers[i+1] - numbers[i] for i in range(len(numbers)-1)]
        avg_spacing = sum(spacings) / len(spacings)

        expected_avg = 85
        deviation = abs(avg_spacing - expected_avg) / expected_avg
        p_value_birthday = max(0, 1 - deviation)
    else:
        p_value_birthday = 0.5

    test_details["birthday_spacings"] = {
        "p_value": p_value_birthday,
        "status": "passed" if p_value_birthday > 0.01 else "failed",
        "description": "Тест интервалов между днями рождения"
    }

    # 2. Overlapping Permutations Test
    triplets = {}
    for i in range(n - 2):
        triplet = sequence[i:i+3]
        triplets[triplet] = triplets.get(triplet, 0) + 1

    expected_count = (n - 2) / 8
    chi_square = sum((count - expected_count) ** 2 / expected_count for count in triplets.values())
    p_value_permutations = 1 - chi_square / 100

    test_details["overlapping_permutations"] = {
        "p_value": p_value_permutations,
        "status": "passed" if p_value_permutations > 0.01 else "failed",
        "description": "Тест перекрывающихся перестановок"
    }

    # 3. Binary Rank Test
    matrix_size = 32
    if n >= matrix_size * matrix_size:
        matrix = [bits[i:i+matrix_size] for i in range(0, matrix_size * matrix_size, matrix_size)]
        ones_in_matrix = sum(sum(row) for row in matrix)
        expected_ones = matrix_size * matrix_size / 2
        deviation = abs(ones_in_matrix - expected_ones) / expected_ones
        p_value_rank = max(0, 1 - deviation)
    else:
        p_value_rank = 0.5

    test_details["binary_rank"] = {
        "p_value": p_value_rank,
        "status": "passed" if p_value_rank > 0.01 else "failed",
        "description": "Тест бинарного ранга матриц"
    }

    # Общий результат Dieharder
    passed_tests = sum(1 for test in test_details.values() if test["status"] == "passed")
    overall_status = "passed" if passed_tests >= 2 else "failed"

    return {
        "status": overall_status,
        "p_value": min(test["p_value"] for test in test_details.values()),
        "details": test_details,
        "summary": f"Пройдено {passed_tests} из {len(test_details)} тестов"
    }

def _testu01_test(sequence: str) -> Dict[str, Any]:
    """
    Заглушка теста TestU01 с детализацией по трем подтестам
    """
    bits = [int(bit) for bit in sequence]
    n = len(bits)

    test_details = {}

    # 1. Autocorrelation Test
    autocorr_lag1 = sum(bits[i] == bits[i+1] for i in range(n-1)) / (n-1)
    expected_autocorr = 0.5
    autocorr_deviation = abs(autocorr_lag1 - expected_autocorr) / expected_autocorr
    p_value_autocorr = max(0, 1 - autocorr_deviation)

    test_details["autocorrelation"] = {
        "p_value": p_value_autocorr,
        "status": "passed" if p_value_autocorr > 0.01 else "failed",
        "description": "Тест автокорреляции с лагом 1"
    }

    # 2. Gap Test
    gaps = []
    current_gap = 0
    for i in range(1, n):
        if bits[i] == bits[i-1]:
            current_gap += 1
        else:
            if current_gap > 0:
                gaps.append(current_gap)
            current_gap = 0

    if gaps:
        avg_gap = sum(gaps) / len(gaps)
        gap_deviation = abs(avg_gap - 1) / 1
        p_value_gap = max(0, 1 - gap_deviation)
    else:
        p_value_gap = 0.5

    test_details["gap"] = {
        "p_value": p_value_gap,
        "status": "passed" if p_value_gap > 0.01 else "failed",
        "description": "Тест расстояний между одинаковыми битами"
    }

    # 3. Maximum-of-t Test
    group_size = 8
    groups = [bits[i:i+group_size] for i in range(0, n, group_size) 
              if len(bits[i:i+group_size]) == group_size]
    max_values = [max(group) for group in groups]

    ones_in_max = sum(max_values)
    expected_ones = len(max_values) * 0.996
    deviation = abs(ones_in_max - expected_ones) / expected_ones
    p_value_max = max(0, 1 - deviation)

    test_details["maximum_of_t"] = {
        "p_value": p_value_max,
        "status": "passed" if p_value_max > 0.01 else "failed",
        "description": "Тест максимумов в группах по 8 бит"
    }

    # Общий результат TestU01
    passed_tests = sum(1 for test in test_details.values() if test["status"] == "passed")
    overall_status = "passed" if passed_tests >= 2 else "failed"

    return {
        "status": overall_status,
        "p_value": min(test["p_value"] for test in test_details.values()),
        "details": test_details,
        "summary": f"Пройдено {passed_tests} из {len(test_details)} тестов"
    }

@app.task
def nist_sts_test_task(file_path: str) -> dict:
    """Задача Celery для теста NIST STS"""
    try:
        with open(file_path, 'r') as f:
            sequence = f.read().strip()

        result = _nist_sts_test(sequence)

        return {
            "nist_sts": {
                "status": result["status"],
                "p_value": result["p_value"],
                "details": result["details"],
                "summary": result["summary"]
            }
        }
    except Exception as e:
        return {
            "nist_sts": {
                "status": "failed", 
                "p_value": None,
                "details": str(e)
            }
        }

@app.task
def dieharder_test_task(previous_results: dict, file_path: str) -> dict:
    """Задача Celery для теста Dieharder"""
    try:
        with open(file_path, 'r') as f:
            sequence = f.read().strip()

        result = _dieharder_test(sequence)

        previous_results.update({
            "dieharder": {
                "status": result["status"],
                "p_value": result["p_value"], 
                "details": result["details"],
                "summary": result["summary"]
            }
        })

        return previous_results
    except Exception as e:
        previous_results.update({
            "dieharder": {
                "status": "failed",
                "p_value": None,
                "details": str(e)
            }
        })
        return previous_results

@app.task 
def testu01_test_task(previous_results: dict, file_path: str) -> dict:
    """Задача Celery для теста TestU01"""
    try:
        with open(file_path, 'r') as f:
            sequence = f.read().strip()

        result = _testu01_test(sequence)

        previous_results.update({
            "testu01": {
                "status": result["status"],
                "p_value": result["p_value"],
                "details": result["details"],
                "summary": result["summary"]
            }
        })

        return previous_results
    except Exception as e:
        previous_results.update({
            "testu01": {
                "status": "failed",
                "p_value": None, 
                "details": str(e)
            }
        })
        return previous_results
