from django.urls import path, include 
from . import apis

urlpatterns = [
    path("api-v1/coinsync", 
         apis.MarketCoinListCreateViewSet.as_view(), 
         name="coin_sync"),
    
    path("api-v1/coinlist",
         apis.CoinListViewSet.as_view(),
         name="coin_list"),
    
    path("api-v1/upbit",
         apis.UpbitCoinPricViewInitailzation.as_view(),
         name="upbit_price"),
    
    path("api-v1/bithum",
         apis.BithumCoinPricViewInitailzation.as_view(),
         name="bithum_price"),
]
