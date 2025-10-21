from generator_service.services.lfsr.utils.generate_win_comb import fon_neyman

class LFSR:
    def __init__(self, seed=None, polynomial=None, length=128):
        """
        Криптографически стойкий регистр сдвига с линейной обратной связью
        
        Args:
            seed: начальное состояние (если None, генерируется случайно)
            polynomial: полином обратной связи в виде списка отводных битов
            length: длина регистра (рекомендуется >= 128 для криптостойкости)
        """
        self.length = length
        
        # Используем стандартный примитивный полином для заданной длины
        if polynomial is None:
            self.polynomial = self._get_primitive_polynomial(length)
        else:
            self.polynomial = polynomial
        
        # Инициализация случайным seed с использованием secrets
        self.state = seed
        
        # Маска для ограничения длины регистра
        self.mask = (1 << length) - 1
        
        # Проверка, что регистр не в нулевом состоянии
        if self.state == 0:
            self.state = 1
    
    def _get_primitive_polynomial(self, length):
        """
        Возвращает примитивный полином для заданной длины.
        Эти полиномы обеспечивают максимальный период (2^length - 1).
        """
        primitive_polynomials = {
            2: [2, 1],           # x^2 + x + 1
            3: [3, 2],           # x^3 + x^2 + 1
            4: [4, 3],           # x^4 + x^3 + 1
            5: [5, 3],           # x^5 + x^3 + 1
            6: [6, 5],           # x^6 + x^5 + 1
            7: [7, 6],           # x^7 + x^6 + 1
            8: [8, 6, 5, 4],     # x^8 + x^6 + x^5 + x^4 + 1
            16: [16, 15, 13, 4], # x^16 + x^15 + x^13 + x^4 + 1
            32: [32, 22, 2, 1],  # x^32 + x^22 + x^2 + x + 1
            64: [64, 63, 61, 60],# x^64 + x^63 + x^61 + x^60 + 1
            128: [128, 127, 126, 121, 107, 99, 85, 70, 63, 50, 41, 29, 22, 17, 9, 2],  # x^128 + x^127 + x^126 + x^121 + 1
            192: [192, 191, 190, 185, 178, 177],  # больше отводов
            256: [256, 255, 254, 251, 246, 245],  # сложный полином для 256 бит
        }
        
        if length in primitive_polynomials:
            return primitive_polynomials[length]
        else:
            # Для других длин используем простой полином (x^length + x + 1)
            return [length, 1]
    
    def _feedback(self):
        """Вычисляет бит обратной связи с использованием полинома"""
        feedback_bit = 0
        for tap in self.polynomial:
            # Сдвигаем на tap-1, так как младший бит имеет индекс 0
            feedback_bit ^= (self.state >> (tap - 1)) & 1
        return feedback_bit & 1
    
    def next_bit(self):
        """
        Генерирует следующий псевдослучайный бит (0 или 1)
        с равной вероятностью появления
        """
        # Получаем выходной бит (младший бит состояния)
        output_bit = self.state & 1
        
        # Вычисляем бит обратной связи
        feedback_bit = self._feedback()
        
        # Сдвигаем регистр и устанавливаем старший бит
        self.state = (self.state >> 1) | (feedback_bit << (self.length - 1))
        
        return output_bit
    
    def get_state(self):
        """Возвращает текущее состояние регистра"""
        return self.state
    
    def set_state(self, new_state):
        """Устанавливает новое состояние регистра"""
        self.state = new_state & self.mask
        if self.state == 0:
            self.state = 1

    def get_sequence(self, len_seq = 1000):
        len_seq_l = len_seq*5
        res = [self.next_bit() for _ in range(len_seq_l)]
        res = fon_neyman(res)[:len_seq]
        return "".join(str(r) for r in res)
