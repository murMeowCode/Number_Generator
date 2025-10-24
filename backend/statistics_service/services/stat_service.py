import numpy as np
from typing import List, Dict
import math
from statistics_service.services.stat_func import (longest_run_ones_in_a_block_test,
        cumulative_sums_test, runs_test, frequency_within_block_test)

from statistics_service.schemas.statistics import TestResult, TestResultDetail, TestType

class SequenceTester:
    def __init__(self, bits: List[int]):
        self.bits = np.array(bits, dtype=int)
        self.bits_string = ''.join([str(c) for c in bits])
        self.n = len(bits)
    
    def frequency_test(self) -> TestResultDetail:
        """Монобитовый тест (Frequency Test)"""
        try:
            ones = np.sum(self.bits)
            zeros = self.n - ones
            proportion = ones / self.n
            
            chisq, p, success = frequency_within_block_test.test(self.bits_string, self.n)
            
            result = TestResult.PASS if p > 0.01 else TestResult.FAIL
            
            return TestResultDetail(
                p_value=p,
                result=result,
                details={
                    "proportion": proportion,
                    "ones_count": int(ones),
                    "zeros_count": int(zeros)
                }
            )
        except Exception as e:
            return TestResultDetail(
                result=TestResult.FAIL,
                details={"error": str(e)}
            )
    
    def runs_test(self) -> TestResultDetail:
        """Тест серий (Runs Test)"""
        try:
            runs = 1
            for i in range(1, self.n):
                if self.bits[i] != self.bits[i-1]:
                    runs += 1
            
            ones = np.sum(self.bits)
            pi = ones / self.n
            
            expected_runs = 2 * ones * (self.n - ones) / self.n + 1
            variance = (expected_runs - 1) * (expected_runs - 2) / (self.n - 1)
            
            p_value = runs_test.test(self.bits_string, self.n)


            result = TestResult.PASS if p_value > 0.01 else TestResult.FAIL
            
            return TestResultDetail(
                p_value=p_value,
                result=result,
                details={
                    "runs": runs,
                    "expected_runs": expected_runs,
                    "variance": variance
                }
            )
        except Exception as e:
            return TestResultDetail(
                result=TestResult.FAIL,
                details={"error": str(e)}
            )

    def serial_test(self, block_size: int = 2) -> TestResultDetail:
        """Тест на последовательности (Serial Test)"""
        try:
            if block_size == 2:
                return self._serial_test_pairs()
            else:
                return self._serial_test_blocks(block_size)
        except Exception as e:
            return TestResultDetail(
                result=TestResult.FAIL,
                details={"error": str(e)}
            )
    
    def _serial_test_pairs(self) -> TestResultDetail:
        pairs = {"00": 0, "01": 0, "10": 0, "11": 0}
        
        for i in range(self.n - 1):
            pair = f"{self.bits[i]}{self.bits[i+1]}"
            if pair in pairs:
                pairs[pair] += 1
        
        expected = (self.n - 1) / 4
        chi_square = sum((obs - expected)**2 / expected for obs in pairs.values())
        p_value = 1 - self._chi2_cdf(chi_square, 3)
        
        result = TestResult.PASS if p_value > 0.01 else TestResult.FAIL
        
        return TestResultDetail(
            p_value=p_value,
            result=result,
            details={"pairs": pairs, "expected": expected}
        )
    
    def _serial_test_blocks(self, block_size: int) -> TestResultDetail:
        k = self.n // block_size
        patterns = {}
        
        for i in range(k):
            block = tuple(self.bits[i*block_size:(i+1)*block_size])
            patterns[str(block)] = patterns.get(str(block), 0) + 1
        
        expected = k / (2 ** block_size)
        chi_square = sum((obs - expected)**2 / expected for obs in patterns.values())
        p_value = 1 - self._chi2_cdf(chi_square, (2 ** block_size) - 1)
        
        result = TestResult.PASS if p_value > 0.01 else TestResult.FAIL
        
        return TestResultDetail(
            p_value=p_value,
            result=result,
            details={"patterns": patterns, "block_size": block_size}
        )
    
    def autocorrelation_test(self, max_lag: int = 5) -> TestResultDetail:
        """Тест автокорреляции"""
        try:
            correlations = []
            results = []
            
            for lag in range(1, max_lag + 1):
                correlation = 0
                for i in range(self.n - lag):
                    correlation += (self.bits[i] - 0.5) * (self.bits[i + lag] - 0.5)
                
                correlation /= (self.n - lag)
                correlations.append(correlation)
                
                result = TestResult.PASS if abs(correlation) < 0.03 else TestResult.WARNING
                results.append(result)
            
            overall_result = TestResult.PASS if all(r == TestResult.PASS for r in results) else TestResult.WARNING
            
            return TestResultDetail(
                result=overall_result,
                details={
                    "correlations": [
                        {"lag": lag+1, "correlation": corr, "result": res}
                        for lag, (corr, res) in enumerate(zip(correlations, results))
                    ],
                    "max_lag": max_lag
                }
            )
        except Exception as e:
            return TestResultDetail(
                result=TestResult.FAIL,
                details={"error": str(e)}
            )
    
    def poker_test(self, m: int = 4) -> TestResultDetail:
        """Poker Test"""
        try:
            k = self.n // m
            blocks = [tuple(self.bits[i*m:(i+1)*m]) for i in range(k)]
            
            patterns = {}
            for block in blocks:
                patterns[str(block)] = patterns.get(str(block), 0) + 1
            
            expected = k / (2 ** m)
            chi_square = sum((obs - expected)**2 / expected for obs in patterns.values())
            p_value = 1 - self._chi2_cdf(chi_square, (2 ** m) - 1)
            
            result = TestResult.PASS if p_value > 0.01 else TestResult.FAIL
            
            return TestResultDetail(
                p_value=p_value,
                result=result,
                details={
                    "blocks_count": k,
                    "unique_patterns": len(patterns),
                    "block_size": m
                }
            )
        except Exception as e:
            return TestResultDetail(
                result=TestResult.FAIL,
                details={"error": str(e)}
            )
    
    def cumulative_sums_test(self) -> TestResultDetail:
        """Cumulative Sums Test"""
        try:
            if self.n >=1000000:
                x = [2 * bit - 1 for bit in self.bits]
                cumulative = np.cumsum(x)
                
                z_forward = max(abs(cumulative)) / np.sqrt(self.n)
                z_backward = max(abs(np.cumsum(x[::-1]))) / np.sqrt(self.n)
                
                z = max(z_forward, z_backward)
                p_value = 1 - self._ks_cdf(z)
                p_forward, p_backward = cumulative_sums_test.test(self.bits_string[:1000000], 1000000)
                success = ((p_forward >= 0.01) and (p_backward >= 0.01))
                result = TestResult.PASS if success else TestResult.FAIL
                z = max(p_forward,p_backward)
                return TestResultDetail(
                    p_value=p_value,
                    result=result,
                    details={"z_score": z}
                )
            else:
                return TestResultDetail(
                    result=TestResult.SKIP,
                    details={"reason": "Sequence too short"}
                )
        except Exception as e:
            return TestResultDetail(
                result=TestResult.FAIL,
                details={"error": str(e)}
            )
    
    def longest_runs_test(self) -> TestResultDetail:
        """Longest Runs Test"""
        try:
            if self.n >= 38912:
                current_run = 1
                longest_run = 1
                
                for i in range(1, self.n):
                    if self.bits[i] == self.bits[i-1]:
                        current_run += 1
                        longest_run = max(longest_run, current_run)
                    else:
                        current_run = 1
                
                expected_max_run = int(np.log2(self.n)) + 1
                
                p_value = longest_run_ones_in_a_block_test.test(self.bits_string[:38912],38912)
                result = TestResult.PASS if p_value > 0.01 else TestResult.FAIL
                return TestResultDetail(
                    p_value=p_value,
                    result=result,
                    details={
                        "longest_run": longest_run,
                        "expected_max_run": expected_max_run
                    }
                )
            else:
                return TestResultDetail(
                    result=TestResult.SKIP,
                    details={"reason": "Sequence too short"}
                )  
        except Exception as e:
            return TestResultDetail(
                result=TestResult.FAIL,
                details={"error": str(e)}
            )
    
    def binary_matrix_rank_test(self, matrix_rows: int = 32, matrix_cols: int = 32) -> TestResultDetail:
        """Binary Matrix Rank Test"""
        try:
            matrix_size = matrix_rows * matrix_cols
            num_matrices = self.n // matrix_size
            
            if num_matrices == 0:
                return TestResultDetail(
                    result=TestResult.SKIP,
                    details={"reason": "Sequence too short for matrix test"}
                )
            
            full_rank_count = 0
            
            for matrix_idx in range(num_matrices):
                start = matrix_idx * matrix_size
                end = start + matrix_size
                matrix_data = self.bits[start:end]
                
                matrix = np.array(matrix_data).reshape(matrix_rows, matrix_cols)
                rank = self._binary_matrix_rank(matrix)
                
                if rank == min(matrix_rows, matrix_cols):
                    full_rank_count += 1
            
            proportion_full_rank = full_rank_count / num_matrices
            p_value = 2 * min(proportion_full_rank, 1 - proportion_full_rank)
            
            result = TestResult.PASS if p_value > 0.01 else TestResult.FAIL
            
            return TestResultDetail(
                p_value=p_value,
                result=result,
                details={
                    "proportion_full_rank": proportion_full_rank,
                    "matrices_count": num_matrices,
                    "full_rank_count": full_rank_count
                }
            )
        except Exception as e:
            return TestResultDetail(
                result=TestResult.FAIL,
                details={"error": str(e)}
            )
    
    def run_all_tests(self) -> Dict[TestType, TestResultDetail]:
        """Запуск всех тестов и возврат результатов в виде словаря"""
        results = {}
        
        results[TestType.FREQUENCY] = self.frequency_test()
        results[TestType.RUNS] = self.runs_test()
        results[TestType.SERIAL] = self.serial_test()
        results[TestType.AUTOCORRELATION] = self.autocorrelation_test()
        results[TestType.POKER] = self.poker_test()
        results[TestType.CUMULATIVE_SUMS] = self.cumulative_sums_test()
        results[TestType.LONGEST_RUNS] = self.longest_runs_test()
        results[TestType.MATRIX_RANK] = self.binary_matrix_rank_test()
        
        return results
    
    def _binary_matrix_rank(self, matrix):
        """Вычисляет ранг бинарной матрицы над GF(2)"""
        mat = matrix.copy()
        rows, cols = mat.shape
        rank = 0
        
        for col in range(cols):
            pivot_row = -1
            for row in range(rank, rows):
                if mat[row, col] == 1:
                    pivot_row = row
                    break
            
            if pivot_row == -1:
                continue
            
            if pivot_row != rank:
                mat[[rank, pivot_row]] = mat[[pivot_row, rank]]
            
            for row in range(rank + 1, rows):
                if mat[row, col] == 1:
                    mat[row] ^= mat[rank]
            
            rank += 1
        
        return rank
    
    def _erf(self, x):
        """Функция ошибок"""
        return 1 - 1 / (1 + 0.278393 * x + 0.230389 * x**2 + 
                       0.000972 * x**3 + 0.078108 * x**4)**4
    
    def _chi2_cdf(self, x, df):
        """CDF распределения хи-квадрат"""
        if x <= 0:
            return 0.0
        return 1 - np.exp(-x/2) * (x/2)**(df/2) / self._gamma(df/2 + 1)
    
    def _gamma(self, x):
        """Гамма-функция"""
        return math.gamma(x)
    
    def _ks_cdf(self, x):
        """CDF распределения Колмогорова-Смирнова"""
        if x <= 0:
            return 0.0
        return 1 - 2 * sum((-1)**(k-1) * np.exp(-2 * k**2 * x**2) 
                          for k in range(1, 5))
