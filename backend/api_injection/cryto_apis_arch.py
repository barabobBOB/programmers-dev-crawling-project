<<<<<<< HEAD
from typing import List, Dict
from collections import Counter
from .api_util import get_json_from_url
from .api_util import BITHUM_API_URL, UPBIT_API_URL
=======
import time
import datetime
import requests
import pandas as pd
from typing import *
from api_injection.api_util import get_json_from_url
from api_injection.api_util import BITHUM_API_URL, UPBIT_API_URL



def making_time() -> List:
    # 현재 시간 구하기
    now = datetime.datetime.now()

    # 목표 날짜 구하기
    # 현재 시간으로부터 200일씩 뒤로 가면서 datetime 객체 생성하기
    target_date = datetime.datetime(2013, 12, 27, 0, 0, 0)
    result = []
    while now >= target_date:
        result.append(now)
        now -= datetime.timedelta(days=200)

    return result
>>>>>>> feat/#4


# 코인 심볼 중복 제거
class CoinListDuplicateRemover:
    def __init__(self) -> None:
        self.upbit_list: Dict = get_json_from_url(
            f"{UPBIT_API_URL}/market/all?isDetails=false"
        )
        self.bithumb_list: Dict = get_json_from_url(f"{BITHUM_API_URL}/ticker/ALL_KRW")

    def get_krw_coins_from_upbit(self) -> List[str]:
        return [
            i["market"].split("-")[1]
            for i in self.upbit_list
            if i["market"].startswith("KRW-")
        ]

    def get_all_coins_from_bithumb(self) -> List[str]:
        return [i for i in self.bithumb_list["data"]]

    def get_all_coins_without_duplicate(self) -> List[str]:
        total: List[str] = self.get_krw_coins_from_upbit() + self.get_all_coins_from_bithumb()
        return [elemt for elemt, index in Counter(total).most_common() if index >= 2]
