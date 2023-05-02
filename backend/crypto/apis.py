from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import (
    CreateAPIView, ListAPIView, ListCreateAPIView
)
from rest_framework.response import Response
from rest_framework import status

from api_injection.cryto_apis_arch import CoinListDuplicateRemover
from api_injection.api_util import get_changed_coins

from typing import *
from .models import * 
from .serializer import *



# bithum_init = BithumCandlingAPI(name="BTC").bithum_candle_price(mint="24h")
# bithum_init = api_injectional(bithum_init, bithum_init.get("data"))

# upbit_init = upbit_trade_all_list(time_data=making_time())
# upbit_init = upbit_trade_data_concat(upbit_init)


# coin symbol 동기화 
class MarketCoinListCreateViewSet(CreateAPIView):
    serializer_class = CoinSymbolSerializer
    queryset = CoinSymbol.objects.all()
    
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.coin_init_model: List[str] = CoinListDuplicateRemover().get_all_coins_without_duplicate()
    
    def create(self, request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.queryset.all().delete()
        
        self.perform_create(self.coin_init_model)
        headers = self.get_success_headers(serializer.data)
                
        return Response(data={"coin_list": self.coin_init_model}, 
                        status=status.HTTP_201_CREATED, 
                        headers=headers)
    
    def perform_create(self, coin_list: List[str]) -> None:
        # coin: List[CoinSymbol] = [CoinSymbol(coin_symbol=data, in_sync=True) for data  in coin_list]
        # self.queryset.bulk_create(coin)
        for data in coin_list:
            self.queryset.create(
                in_sync=True,
                coin_symbol=data
            )

    
# 코인 리스트 필터
class CoinListViewSet(ListAPIView):
    queryset = CoinSymbol.objects.all()
    serializer_class = CoinListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CoinListUpperFilter
    filterset_fields = ['coin_symbol']

    
# 코인 가격 동기화    
class UpbitCoinPricViewInitailzation(ListCreateAPIView):
    pass


class BithumCoinPricViewInitailzation(ListCreateAPIView):
    pass
