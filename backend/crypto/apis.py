from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from api_injection.cryto_apis_arch import CoinListDuplicateRemover
from .models import * 
from .serializer import *
from typing import *



# coin symbol 동기화 
class MarketCoinListCreateViewSet(ListCreateAPIView, DestroyAPIView):
    serializer_class = CoinSymbolSerializer
    coin_init_model = CoinListDuplicateRemover().get_all_coins_without_duplicate()
    queryset = CoinSymbol.objects.all()
    
    def perform_destroy(self):
        return self.queryset.delete()
    
    def create(self, request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_destroy()
        coin_list: List[Dict[str, str]] = self.coin_init_model
        self.perform_create(coin_list)
        headers = self.get_success_headers(serializer.data)
                
        return Response(data={"coin_list": coin_list}, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        for data in serializer:
            self.queryset.create(coin_symbol=data)


# 코인 가격 동기화    
class CoinPricViewInitailzation(ListCreateAPIView):
    pass