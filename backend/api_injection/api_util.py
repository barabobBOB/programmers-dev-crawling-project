from typing import * 
import requests


UPBIT_API_URL = "https://api.upbit.com/v1/"
BITHUM_API_URL = "https://api.bithumb.com/public/"


def get_json_from_url(url: str) -> Dict:
    headers: Dict[str, str] = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    info = response.json()
    
    return info


def get_changed_coins(qs, new_coin_list: List[str]) -> List[str]:
    old_coin_list = list(qs.values_list('coin_symbol', flat=True))
    changed_coins = []
    for coin in new_coin_list:
        if coin not in old_coin_list:
            changed_coins.append(coin)
    return changed_coins