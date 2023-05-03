import requests
from datetime import datetime, timedelta
from typing import Dict, List
from collections import deque
import time

class ExchangeAPI:
    API_URL = None

    def __init__(self):
        # api_key, api_secret 필요한 API 호출이면 구현
        pass

    def getHeaders(self) -> dict :
        headers = {"accept": "application/json"}
        return headers

    def get(self, endpoint, params=None):
        url = self.API_URL + endpoint
        headers = self.getHeaders()
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
            return None
        return response.json()
    
    def removeDuplication(lst : List,lst2 : List) -> List[Dict]:
        res = list(set(lst)&set(lst2))
        result = []
        for r in res:
            obj = {
                "coin_symbol": r
            }
            result.append(obj)
        
        return result
    
    
class bithumbAPI(ExchangeAPI):
    API_URL = "https://api.bithumb.com"

    def __init__(self):
        super().__init__()
        
        
    def get_tickers(self) -> List[str]:
        endpoint = "/public/ticker/ALL_KRW"
        res = self.get(endpoint)['data']
        
        result = []
        
        for k in res.keys():
            if k == 'date':
                continue
            result.append(k)
            
        return result
    
    # symbol = 'ALL', 'BTC' ,'ETH' ...
    def get_current_price(self, symbol: str='ALL') -> List[Dict]:
        try:
            endpoint = f"/public/ticker/{symbol}_KRW"
            res = self.get(endpoint)['data']
            
            result = []
            
            if symbol == 'ALL':
                date = datetime.fromtimestamp(int(res['date'])/1000).strftime("%Y-%m-%d")
                for k,v in res.items():
                    if k == 'date': continue
                    obj = {
                        'coin_symbol' : "",
                        'trade_timestamp' : "",
                        'price' : 0
                    }
                    obj['coin_symbol'] = k
                    obj['trade_timestamp'] = date
                    obj['price'] = float(v['closing_price'])
                    result.append(obj)
            else:
                obj = {
                        'coin_symbol' : "",
                        'trade_timestamp' : "",
                        'price' : 0
                    }
                date = datetime.fromtimestamp(int(res['date'])/1000).strftime("%Y-%m-%d")
                obj['coin_symbol'] = symbol
                obj['trade_timestamp'] = date
                obj['price'] = float(res['closing_price'])
                result.append(obj)
                
        except Exception as e:
            print(e)
            return None
        
        return result
        
        
    # symbol = 'BTC', 'ETH' ...
    # interval = 1m, 3m, 5m, 10m, 30m, 1h, 6h, 12h, 24h
    # args : _from, _to = 'yyyy-mm-dd'
    def get_candles(self, symbol: str, _from: str = None , _to: str = None, interval: str = '24h') -> List[Dict]:
        try:
            endpoint = f"/public/candlestick/{symbol}_KRW/{interval}"
            _from = datetime.strptime(_from,'%Y-%m-%d') if _from else datetime(2000,1,1)
            _to = datetime.strptime(_to,'%Y-%m-%d') if _to else datetime.now()
            res = self.get(endpoint)['data']
            time.sleep(0.02) # rps 135
            result = []
            
            for r in res:
                date = datetime.fromtimestamp(r[0]/1000)
                if _from<=date<=_to:
                    obj = {
                        'coin_symbol' : "",
                        'trade_timestamp' : "",
                        'price' : 0
                    }
                    obj['coin_symbol'] = symbol
                    obj['trade_timestamp'] = datetime.fromtimestamp(r[0]/1000).strftime("%Y-%m-%d")
                    obj['price'] = float(r[2])
                    
                    result.append(obj)
                else:
                    continue
        except Exception as e:
            print(e)
            return None
            
        return result
    

class upbitAPI(ExchangeAPI):
    API_URL = "https://api.upbit.com"

    def __init__(self):
        super().__init__()
    
    
    def get_tickers(self) -> List[str]:
        endpoint = "/v1/market/all"
        res = self.get(endpoint)
        
        result = []
        
        for r in res:
            result.append(r["market"].split('-')[1])
            
        return result
    
    
    # symbol = 'BTC' ,'ETH' ...
    def get_current_price(self, symbol: str='BTC') -> List[Dict]:
        try:
            query_param = f"?markets=KRW-{symbol}" if symbol!='ALL' else ""
            endpoint = f"/v1/ticker{query_param}"
            res = self.get(endpoint)
            
            result = []
            
            for r in res:
                obj = {
                        'coin_symbol' : "",
                        'trade_timestamp' : "",
                        'price' : 0
                    }
                obj['coin_symbol'] = symbol
                obj['trade_timestamp'] = datetime.fromtimestamp(r['timestamp']/1000).strftime("%Y-%m-%d")
                obj['price'] = r['trade_price']
                result.append(obj)
        except Exception as e:
            print(e)
            return None
    
        return result
        
        
    # symbol = 'BTC', 'ETH' ...
    # interval = days (미구현 :weeks, months / 1m, 3m, 5m, 10m, 15m, 30m, 60m, 240m)
    # args : _from, _to = 'yyyy-mm-dd'
    def get_candles(self, symbol: str='BTC', _from: str = None , _to: str = None, interval: str = 'days') -> List[Dict]:
        try: 
            if interval[-1] == 'm':
                endpoint = f"/v1/candles/minutes/{interval[:-1]}?market=KRW-{symbol}"
            else:
                endpoint = f"/v1/candles/{interval}?market=KRW-{symbol}"
            _from = datetime.strptime(_from + " 00:00:00",'%Y-%m-%d %H:%M:%S') if _from else datetime(2000,1,1)
            _to = datetime.strptime(_to + " 00:00:00",'%Y-%m-%d %H:%M:%S') if _to else datetime.fromtimestamp(int(time.time()))
            
            result = deque([])
            
            while True:
                query = "&to=%s&count=200"%(_to)
                endpoint_ = endpoint + query
                    
                res = self.get(endpoint_)

                for r in res:
                    if datetime.strptime(r['candle_date_time_utc'].replace('T'," "),'%Y-%m-%d %H:%M:%S') < _from:
                        break
                    obj = {
                        'coin_symbol' : "",
                        'trade_timestamp' : "",
                        'price' : 0
                    }
                    obj['coin_symbol'] = symbol
                    obj['trade_timestamp'] = r['candle_date_time_utc'].replace('T'," ")[:11]
                    obj['price'] = r['trade_price']
                    result.appendleft(obj)
                
                if _from>_to:
                    break
                _to -= timedelta(days=200)
                time.sleep(0.2)
        except Exception as e:
            print(e)
            return None
        
        return result

if __name__ == "__main__":
    bithumb = bithumbAPI()
    upbit = upbitAPI()
    
    btickers = bithumb.get_tickers()
    bprice = bithumb.get_current_price('BTC')
    bcandles = bithumb.get_candles('BTC', _from='2022-01-01')
    
    utickers = upbit.get_tickers()
    uprice = upbit.get_current_price('BTC')
    ucandles = upbit.get_candles('BTC',_from='2022-01-01')
    
    res = ExchangeAPI.removeDuplication(btickers, utickers)

    print(ucandles['datetime'])
