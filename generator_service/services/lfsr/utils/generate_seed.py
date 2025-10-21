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


def get_last_12_digits_int(number):
    """
    Извлекает последние 12 цифр как целое число
    """
    num_str = str(number).replace('.', '')
    last_12 = num_str[-12:] if len(num_str) >= 12 else num_str.zfill(12)
    
    return int(last_12)


def float_to_128bit_int(number):
    """
    Преобразует float в 128-битное целое число
    """
    # Масштабируем число до большого значения
    scaled = number * (2**128)/1000
    
    # Берем целую часть и обрезаем до 128 бит
    int_128 = int(scaled) & ((1 << 128) - 1)
    
    return int_128


def get_seed():
    state = fetch_xray_flares_data()
    return float_to_128bit_int(get_last_12_digits_int(state))