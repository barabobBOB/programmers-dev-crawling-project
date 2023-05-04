from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api_injection.cryto_apis_arch import CoinListDuplicateRemover
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


class CoinTotalListViewInitailization(ListAPIView):
    queryset = CoinSymbol.objects.all()
    serializer_class = CoinListSerializer
    filterset_class = CoinListUpperFilter
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["coin_symbol"]  
