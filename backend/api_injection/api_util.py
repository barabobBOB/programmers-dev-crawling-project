from typing import * 
import requests


UPBIT_API_URL = "https://api.upbit.com/v1/"
BITHUM_API_URL = "https://api.bithumb.com/public/"


def get_json_from_url(url: str) -> Dict:
    headers: Dict[str, str] = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    info = response.json()
    
    return info
