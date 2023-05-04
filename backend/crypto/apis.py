from typing import Any
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api_injection.cryto_apis_arch import CoinListDuplicateRemover
from api_injection.crypto_apis import *
from .models import * 
from .serializer import *



# bithum_init = BithumCandlingAPI(name="BTC").bithum_candle_price(mint="24h")
# bithum_init = api_injectional(bithum_init, bithum_init.get("data"))

# upbit_init = upbit_trade_all_list(time_data=making_time())
# upbit_init = upbit_trade_data_concat(upbit_init)


# coin symbol 동기화 
class MarketCoinListCreateViewSet(APIView):
    queryset = CoinSymbol.objects.all()
    
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.coin_name_list: List[str] = CoinListDuplicateRemover().get_all_coins_without_duplicate()
        
    def post(self, request, format=None) -> Response: 
        if request.data.get("is_sync"):
            for data in self.coin_name_list:
                qs = self.queryset.filter(coin_symbol=data)
                if not qs:
                    self.queryset.create(coin_symbol=data, is_sync=True)
                
                # 이게 필요있는지는 고민해볼것 
                elif Q(qs.filter(coin_symbol=data) & qs.filter(is_sync=False)):
                    self.queryset.update(is_sync=True)
            return Response({"coin_list": self.coin_name_list}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Not coin list synchronization"}, status=status.HTTP_400_BAD_REQUEST)
            
# 코인 리스트 필터
class CoinListViewSet(ListAPIView):
    queryset = CoinSymbol.objects.all()
    serializer_class = CoinListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CoinListUpperFilter
    filterset_fields = ['coin_symbol']

# 공통된 코인 리스트 업데이트
# 현재 DB에 저장된 코인들 외에 다른 공통된 코인이 생기면 그 코인만 업데이트시킴
# 반대로 DB에 저장되어 있던 코인이 공통된 코인 목록에서 제외되면(한 거래소에서 상폐시켰을때) 그 코인은 DB에서 삭제시켜야함 : 구현
class UpdateCoinList(CreateAPIView):
    serializer_class = CoinListSerializer
    lookup_field = "coin_symbol"
    def post(self, request, format=None):
        
        #upbit = upbitAPI()
        bithumb = bithumbAPI()
        
        #lst = upbit.get_tickers()
        data = bithumb.get_tickers()
        #data = ExchangeAPI.removeDuplication(lst,lst2)

        qs = CoinSymbol.objects.all()
        qsList = [q.coin_symbol for q in qs]
        
        deleteList = list(set(qsList)-set(data))
        addList = list(set(data)-set(qsList))
        addObj = [{"coin_symbol": symbol} for symbol in addList]
        
        dc = CoinSymbol.objects.filter(coin_symbol__in=deleteList).delete()
        serializer = CoinListSerializer(data=addObj, many=True)

        if serializer.is_valid():
            try:
                serializer.save()
                return Response({'success': True, 'update_coin_count': len(serializer.validated_data), 'delete_coin_count':dc, 'error_msg':""})
            except Exception as e:
                return Response({'success': False, 'update_coin_count': 0, 'delete_count':dc, 'error_msg': e})
        else:
            return Response({'success': False, 'update_coin_count': 0, 'delete_count':dc, 'error_msg':serializer.errors[0]})
        
# 특정 코인 가격 업데이트 후, 업데이트 한 데이터 Response
class UpdateCoinPrice(APIView):
    def post(self, request, coin_symbol, format=None):
        bithumb = bithumbAPI()
        
        if coin_symbol == 'ALL':
            coins = CoinSymbol.objects.all()
            
            coinUpdateCnt = 0
            try:
                for coin in coins:
                    c = CoinPriceAllChartMarket.objects.filter(coin_symbol=coin.coin_symbol).last()
                    if c:
                        continue
                    else:
                        candles = bithumb.get_candles(coin.coin_symbol)
                        serializer = CoinPriceSerializer(data=candles, many=True)
                        
                        if serializer.is_valid():
                            serializer.save()
                            coinUpdateCnt += 1
                            print(coin.coin_symbol)
            except Exception as e:
                print(e)
                return Response({'success': False, 'update_coin_count': 0})
            else:
                return Response({'success': True, 'update_count': coinUpdateCnt})
            
        else:
            CoinPriceAllChartMarket.objects.filter(coin_symbol=coin_symbol).delete()

            candles = bithumb.get_candles(coin_symbol)

            serializer = CoinPriceSerializer(data=candles, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 특정 코인의 과거 가격 데이터
class CoinPriceView(ListAPIView):
    serializer_class = CoinPriceSerializer
    lookup_field = 'coin_symbol'

    def get_queryset(self):
        coin_symbol = self.kwargs.get(self.lookup_field)
        queryset = CoinPriceAllChartMarket.objects.filter(coin_symbol=coin_symbol).order_by('trade_timestamp')
        return queryset