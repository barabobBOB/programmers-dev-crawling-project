import time
import datetime
import requests
import pandas as pd

from typing import *
from .api_util import get_json_from_url
from .api_util import BITHUM_API_URL, UPBIT_API_URL



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


# 코인 심볼 중복 제거
class CoinListDuplicateRemover:
    def __init__(self) -> None:
        self.upbit_list: Dict = get_json_from_url(f"{UPBIT_API_URL}/market/all?isDetails=false")
        self.bithumb_list: Dict = get_json_from_url(f"{BITHUM_API_URL}/ticker/ALL_KRW")
        
    def get_krw_coins_from_upbit(self) -> List[str]:
        return [i["market"].split("-")[1] for i in self.upbit_list if i["market"].startswith("KRW-")]

    def get_all_coins_from_bithumb(self) -> List[str]:
        return [i for i in self.bithumb_list["data"]]
    
    def get_all_coins_without_duplicate(self) -> List[str]:
        total: List[str] = self.get_krw_coins_from_upbit() + self.get_all_coins_from_bithumb() 
        total: List[str] = [name for name in set(total)]
        return total
    

class ApiBasicArchitecture:
    """
        기본 클래스 
        :param name -> 코인 이름 
        :param date -> 날짜 
        :param count -> data를 가져올 개수 
    
        __namespace__ 
            -> coin symbol은 대문자로 취급하기에 소문자가 오더라도 upper로 오류방지 
    """
    def __init__(self,
                 name: Optional[str] = None,
                 date: Optional[datetime.datetime] = None,
                 count:  Optional[int] = None) -> None:
        self.name: Optional[str] = name
        self.date: Optional[str] = date
        self.count: Optional[int] = count
    
    def __namesplit__(self) -> str:
        return self.name.upper()


class BithumCandlingAPI(ApiBasicArchitecture):
    """
    :param minit
        - 차트 간격, 기본값 : 24h {1m, 3m, 5m, 10m, 30m, 1h, 6h, 12h, 24h 사용 가능}
    """

    # 시간별 통합으로 되어 있음
    def bithum_candle_price(self, mint: str) -> List:
        return get_json_from_url(f"{BITHUM_API_URL}/candlestick/{self.name}_KRW/{mint}")


class UpBitCandlingAPI(ApiBasicArchitecture):
    """
    :param time
        minutes, days, weeks, year
        - 분, 일, 주, 년
    :param minit
        - 시간 단위
    :param count
        - 얼마나 가져올것인지
    :param date
        - 시간 단위
    """

    def __init__(self, name: Optional[str] = None,
                 date: Optional[datetime.datetime] = None,
                 count: Optional[int] = None) -> None:
        super().__init__(name, date, count)
        self.name_candle_count = f"market=KRW-{self.name}&count={self.count}"
        self.name_candle_count_date = f"market=KRW-{self.name}&to={self.date}&count={self.count}"

    def upbit_candle_price(self, mint: int) -> List:
        return get_json_from_url(
            f"{UPBIT_API_URL}/candles/minutes/{mint}?{self.name_candle_count}"
        )

    # 상위 200개
    def upbit_candle_day_price(self) -> List:
        return get_json_from_url(f"{UPBIT_API_URL}/candles/days?{self.name_candle_count}")

    # 날짜 커스텀
    def upbit_candle_day_custom_price(self) -> List:
        return get_json_from_url(
            f"{UPBIT_API_URL}/candles/days?{self.name_candle_count_date}"
        )


def api_injectional(api: Any, inject_parmeter: Any) -> pd.DataFrame:
    # API 호출
    api_init = api

    api_init = pd.DataFrame(
        inject_parmeter,
        columns=[
            "timestamp", 
            "opening_price", 
            "trade_price",
            "high_price", 
            "low_price", 
            "candle_acc_trade_volume"
        ]
    )

    api_init["timestamp"] = api_init["timestamp"].apply(
        lambda x: time.strftime(r"%Y-%m-%d %H:%M", time.localtime(x / 1000))
    )
    
    api_init["opening_price"] = api_init["opening_price"].apply(lambda x: float(x))
    api_init["trade_price"] = api_init["trade_price"].apply(lambda x: float(x))
    api_init["high_price"] = api_init["high_price"].apply(lambda x: float(x))
    api_init["low_price"] = api_init["low_price"].apply(lambda x: float(x))

    return api_init


# 결과 출력하기
def upbit_trade_all_list(time_data: List[datetime.datetime]) -> List[pd.DataFrame]:
    timer: List[datetime.datetime] = time_data
    result_upbit_data = []

    for dt in timer:
        try:
            a = dt.strftime("%Y-%m-%d %H:%M:%S")

            upbit_init = UpBitCandlingAPI(
                name="BTC", count=200, date=a
            ).upbit_candle_day_custom_price()

            # API 호출
            market_init = api_injectional(upbit_init, upbit_init)

            if market_init.empty:
                continue
            result_upbit_data.append([market_init])
        except requests.exceptions.JSONDecodeError:
            continue

    return result_upbit_data


# 데이터 병합
def upbit_trade_data_concat(data: List) -> pd.DataFrame:
    result_upbit_data_concat = pd.concat([df for [df] in data], ignore_index=True)
    return result_upbit_data_concat

