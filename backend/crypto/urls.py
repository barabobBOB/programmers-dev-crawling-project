from django.urls import path, include 
from . import apis

urlpatterns = [
    path("api-v1/coinsync", 
         apis.MarketCoinListCreateViewSet.as_view(), 
         name="coin_sync"),
    
    path("api-v1/coinlist",
         apis.CoinListViewSet.as_view(),
         name="coin_list"),
    
]
