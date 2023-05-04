from django.urls import path
from . import apis

urlpatterns = [
    path(
        "api-v1/coinsync",
        apis.MarketCoinListCreateInitalization.as_view(),
        name="coin_sync"
    ),
    
    path(
        "api-v1/coinlist", 
        apis.CoinTotalListViewInitailization.as_view(), 
        name="coin_list"
    ),    
]
