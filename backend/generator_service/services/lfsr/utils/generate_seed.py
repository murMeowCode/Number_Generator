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
    
    number_str = str(original_float)
    
    string_bytes = number_str.encode('utf-8')
    bit_string = ''.join(format(byte, '08b') for byte in string_bytes)
    
    if len(bit_string) > 128:
        bit_string = bit_string[:128]
    elif len(bit_string) < 128:
        bit_string = bit_string + '0' * (128 - len(bit_string))
    
    final_number = int(bit_string, 2)
    
    
    return final_number

def get_decimal(num):
    return str(num)[-16:]

def get_seed():
    state = fetch_xray_flares_data()
    seed = get_decimal(state)
    return complete_conversion(seed), state

def get_seed_verify(state):
    seed = get_decimal(state)
    return complete_conversion(seed), state
