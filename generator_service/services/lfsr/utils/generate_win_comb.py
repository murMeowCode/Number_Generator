def fon_neyman(bits):
    corrected_bits = []
    i = 0
    while i < len(bits) - 1:
        pair = (bits[i], bits[i+1])
        if pair == (0, 1):
            corrected_bits.append(0)
        elif pair == (1, 0):
            corrected_bits.append(1)
        i += 2

    return corrected_bits

def extract_unique_digits(lfsr, num_digits:int,
                           min_value:int = 0, max_value:int = 255):
    """
    Извлекает уникальные цифры из списка битов.
    
    Args:
        bit_list: список битов (0 и 1)
        num_digits: количество нужных цифр
        min_value: минимальное значение цифры (по умолчанию 0)
        max_value: максимальное значение цифры (по умолчанию 255)
    
    Returns:
        список уникальных цифр в заданном диапазоне
    """
    count_bit = num_digits*8*500
    bit_list = lfsr.get_sequence(count_bit)
    bit_list = fon_neyman(bit_list)
    print(len(bit_list))


    # Проверяем, что список битов достаточно длинный
    if len(bit_list) < num_digits * 8:
        raise ValueError("Недостаточно битов для извлечения нужного количества цифр")
    
    unique_digits = set()
    result = []
    
    # Обрабатываем биты группами по 8
    for i in range(0, len(bit_list), 8):
        if len(result) >= num_digits:
            break
            
        # Берем 8 бит
        byte_bits = bit_list[i:i+8]
        if len(byte_bits) < 8:
            break
            
        # Преобразуем биты в число
        digit = 0
        for bit in byte_bits:
            digit = (digit << 1) | bit
        
        # Проверяем условия
        if (min_value <= digit <= max_value and 
            digit not in unique_digits and 
            len(result) < num_digits):
            unique_digits.add(digit)
            result.append(digit)
    
    # Если не набрали достаточно уникальных цифр
    if len(result) < num_digits:
        print(f"Предупреждение: найдено только {len(result)} уникальных цифр из {num_digits}")
    
    return result