from typing import *
from django_filters.rest_framework import DjangoFilterBackend

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
            # 일괄 삭제
            self.queryset.delete()
            
            # 일괄 생성
            for data in self.coin_name_list:
                self.queryset.create(coin_symbol=data, is_sync=True)
            
            return Response(
                {"coin_list": self.coin_name_list}, 
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"error": "Not coin list synchronization"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# 모든 코인 거래 데이터 생성
class CoinTradingCreateInitalization(APIView):
    queryset = CoinSymbol.objects.all()
    
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.coin_name_list: List[
            str
        ] = CoinListDuplicateRemover().get_all_coins_without_duplicate() 
        
    def post(self, request, format=None) -> Response:    
        if request.data.get("is_trading_all_data"):
            for cd in self.coin_name_list:
                qs = self.queryset.filter(coin_symbol=cd, is_sync=True)  
                if not qs:
                    return Response(
                        {"error": "coin symbol목록 에 해당 코인이 없습니다"},
                        status=status.HTTP_204_NO_CONTENT
                    )
                elif qs:
                    data_ = coin_trading_data_concatnate(coin_name=cd)
                    for data in data_:
                        CoinPriceAllChartMarket.objects.create(
                            coin_symbol=qs.first(),
                            price=data["trade_price"],
                            trade_timestamp=data["timestamp"]
                        )
                        
            return Response(
                {"suceess": "good"},
                status=status.HTTP_201_CREATED
            )
        else:
            Response({"Not": "비정상적인 접근입니다"}, status=status.HTTP_400_BAD_REQUEST)


# # 모든 코인 거래 데이터 생성
# class CoinTradingCreateInitalization(ListCreateAPIView):
#     queryset = CoinSymbol.objects.all()
#     serializer_class = CoinTradingDataSerializer
#     lookup_field: str = "coin_symbol"
    
#     def perform_create(self, serializer):
#         qs = self.queryset.filter(coin_symbol=serializer.data["coin_symbol"], is_sync=True)  
#         if qs:
#             data_ = coin_trading_data_concatnate(coin_name=serializer.data["coin_symbol"])
#             for data in data_:
#                 CoinPriceAllChartMarket.objects.create(
#                     coin_symbol=qs.first(),
#                     price=data["trade_price"],
#                     trade_timestamp=data["timestamp"]
#                 )


class AbstractCoinSymbolUpperFilter(ListAPIView):
    queryset = None 
    serializer_class = None 
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["coin_symbol"]  


# 거래 데이터 필터 
class TradeCoinDataViewInitailization(AbstractCoinSymbolUpperFilter):
    queryset = CoinPriceAllChartMarket.objects.all()
    serializer_class = CoinTradingDataSerializer
    lookup_field = 'coin_symbol'
    filterset_fields = ["coin_symbol"]

    def get_queryset(self):
        queryset = CoinPriceAllChartMarket.objects.filter(
            coin_symbol=self.lookup_field).order_by('trade_timestamp')
        return queryset
    

# 코인 리스트 필터
class CoinTotalListViewInitailization(AbstractCoinSymbolUpperFilter):
    queryset = CoinSymbol.objects.all()
    serializer_class = CoinListSerializer
    filterset_class = CoinListUpperFilter

