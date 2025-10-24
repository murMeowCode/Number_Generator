import random
import requests
from shared.config.base import settings


def get_python_random_sequence(n: int) -> str:
    """Сгенерировать последовательность через Python random"""
    return ''.join(str(random.randint(0, 1)) for _ in range(n))


def get_random_org_sequence(n: int) -> str:
    """Получить последовательность от Random.org"""
    
    payload = {
        "jsonrpc": "2.0",
        "method": "generateIntegers",
        "params": {
            "apiKey": settings.RANDOM_ORG_API_KEY,
            "n": n,
            "min": 0,
            "max": 1,
            "replacement": True
        },
        "id": 1
    }
    
    try:
        response = requests.post(
            settings.RANDOM_ORG_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'result' in data:
                numbers = data['result']['random']['data']
                return ''.join(str(x) for x in numbers)
                
    except Exception:
        pass
    
    return ""
