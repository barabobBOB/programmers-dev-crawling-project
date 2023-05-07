from crawling.coinness_crawling import *
from crawling.googlenews_crawling import *

from .models import *

# 최신 뉴스 10개 크롤링
def recent_news() -> None:
    coinness_news = coinness_crawling()
    coinness_news.reverse()

    for news in coinness_news:
        CoinnessNews.objects.create(title=news['title'], 
                                    content=news['content'], 
                                    date=news['date'], 
                                    time=news['time'])

# 해당 코인 뉴스 크롤링 
def coin_news() -> None:
    coin_name = CoinSymbol.objects.values("coin_symbol")          
    
    for i in coin_name:
        google_coin_news = news_crawling(i["coin_symbol"])

        for news in google_coin_news:
            CrawlingInformation.objects.create(name=news['name'], 
                                                titles=news['title'], 
                                                dates=news['date'], 
                                                urls=news['url'])
            
            
            