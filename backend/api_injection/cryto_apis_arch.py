from typing import Dict, List, Set
from .api_util import get_json_from_url
from .api_util import BITHUM_API_URL, UPBIT_API_URL


# 코인 심볼 중복 제거
class CoinListDuplicateRemover:
    def __init__(self) -> None:
        self.bithumb_list: Dict = get_json_from_url(BITHUM_API_URL)
        self.upbit_list: Dict = get_json_from_url(UPBIT_API_URL)
        
    def get_krw_coins_from_upbit(self) -> List[str]:
        return [i["market"].split("-")[1] for i in self.upbit_list if i["market"].startswith("KRW-")]

    def get_all_coins_from_bithumb(self) -> List[str]:
        return [i for i in self.bithumb_list["data"]]
    
    def get_all_coins_without_duplicate(self) -> List[str]:
        total: List[str] = self.get_krw_coins_from_upbit() + self.get_all_coins_from_bithumb() 
        total: List[str] = [name for name in set(total)]
        return total
    
