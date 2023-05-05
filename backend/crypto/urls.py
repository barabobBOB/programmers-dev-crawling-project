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
    
    path("api-v1/updateprice/<str:coin_symbol>",
         apis.UpdateCoinPrice.as_view(),
         name='update_price'
    ),
    
    path("api-v1/coinprice/<str:coin_symbol>",
         apis.CoinPriceView.as_view(),
         name="coin_price"
    ),

    path("api-v1/recentnews/crawling",
         apis.RecentNews.as_view(),
         name="recent_news_crawling"
         ),

    path("api-v1/recentnews",
         apis.RecentNewsView.as_view(),
         name="recent_news"
         ),
]
