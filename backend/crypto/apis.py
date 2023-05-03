from typing import *
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api_injection.cryto_apis_arch import (
    CoinListDuplicateRemover, coin_trading_data_concatnate
)
from .models import *
from .serializer import *


# coin symbol 동기화
class MarketCoinListCreateInitalization(APIView):
    queryset = CoinSymbol.objects.all()

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.coin_name_list: List[
            str
        ] = CoinListDuplicateRemover().get_all_coins_without_duplicate()

    def post(self, request, format=None) -> Response:
        if request.data.get("is_sync"):
            for data in self.coin_name_list:
                qs = self.queryset.filter(coin_symbol=data)
                if not qs:
                    self.queryset.create(coin_symbol=data, is_sync=True)
            return Response(
                {"coin_list": self.coin_name_list}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"error": "Not coin list synchronization"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# 모든 코인 거래 데이터 생성
class CoinTradingCreateInitalization(ListCreateAPIView):
    queryset = CoinSymbol.objects.all()
    serializer_class = CoinTradingDataSerializer
    lookup_field: str = "coin_symbol"
    
    def perform_create(self, serializer):
        #{'timestamp': '2023-02-07', 
        # 'coin_symbol': 'DOGE', 
        # 'opening_price': 116.65, 
        # 'trade_price': 115.3,
        # 'high_price': 117.85, 
        # 'low_price': 113.8}
        qs = Q(self.queryset.filter(coin_symbol=serializer) & self.queryset.filter(is_sync=True))  
        if qs:
            data_ = coin_trading_data_concatnate(coin_name=serializer["coin_symbol"])
            for data in data_:
                self.queryset.create(
                    coin_symbol=data["coin_symbol"],
                    price=data["trade_price"],
                    trade_timestamp=data["timestamp"]
                ).save()
      
      
# 코인 리스트 필터
class CoinTotalListViewInitailization(ListAPIView):
    queryset = CoinSymbol.objects.all()
    serializer_class = CoinListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CoinListUpperFilter
    filterset_fields = ["coin_symbol"]

