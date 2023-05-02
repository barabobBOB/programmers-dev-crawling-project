from typing import Any
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api_injection.cryto_apis_arch import CoinListDuplicateRemover
from api_injection.api_util import get_changed_coins

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

    
