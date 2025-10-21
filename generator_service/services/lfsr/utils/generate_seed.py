import requests

def fetch_xray_flares_data():
    url = "https://services.swpc.noaa.gov/json/goes/primary/xray-flares-latest.json"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if not data:
            print("Ошибка: Получены пустые данные.")
            return None
        
        current_ratio = data[0].get('current_ratio', 'Поле не найдено')
        
        return current_ratio
    
    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети или HTTP: {e}")
        return None
    except ValueError as e:
        print(f"Ошибка парсинга JSON: {e}")
        return None
    except IndexError as e:
        print(f"Ошибка: Список данных пуст или индекс вне диапазона: {e}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None


def complete_conversion(original_float):
    
    # Шаг 1: в строку
    number_str = str(original_float)
    
    # Шаг 2: в биты
    string_bytes = number_str.encode('utf-8')
    bit_string = ''.join(format(byte, '08b') for byte in string_bytes)
    
    # Шаг 3: до 128 бит
    if len(bit_string) > 128:
        bit_string = bit_string[:128]
    elif len(bit_string) < 128:
        bit_string = bit_string + '0' * (128 - len(bit_string))
    
    # Шаг 4: в число
    final_number = int(bit_string, 2)
    
    
    return final_number


def get_seed():
    state = fetch_xray_flares_data()
    return complete_conversion(state), state