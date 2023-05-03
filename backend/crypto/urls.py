from django.urls import path, include 
from . import apis

urlpatterns = [
    path("api-v1/coinsync", 
         apis.MarketCoinListCreateViewSet.as_view(), 
         name="coin_sync"),
    
    path("api-v1/coinlist",
         apis.CoinListViewSet.as_view(),
         name="coin_list"),
    
    path("api-v1/updatecoinlist",
         apis.UpdateCoinList.as_view(),
         name='update_coin_list'),
    
    path("api-v1/updateprice/<str:coin_symbol>",
         apis.UpdateCoinPrice.as_view(),
         name='update_price'),
    
    path("api-v1/coinprice/<str:coin_symbol>",
         apis.CoinPriceView.as_view(),
         name="coin_price"),
]
