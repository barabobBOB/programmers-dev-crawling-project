from crawling.coinness_crawling import *
from crawling.googlenews_crawling import *

from .models import *

# 최신 뉴스 10개 크롤링
def recent_news():
    coinness_news = coinness_crawling()
    coinness_news.reverse()

    for news in coinness_news:
        CoinnessNews.objects.create(title=news['title'], 
                                    content=news['content'], 
                                    date=news['date'], 
                                    time=news['time'])

# 해당 코인 뉴스 크롤링 
def coin_news():
    coin_name = ['BTC', 'ETH', 'MTL', 'XRP', 'ETC', 'SNT', 'WAVES', 'QTUM', 'STEEM', 
                 'XLM', 'REP', 'ADA', 'POWR', 'BTG', 'ICX', 'EOS', 'TRX', 'ONT',
                 'ZIL', 'ZRX', 'LOOM', 'BCH', 'BAT', 'LOST', 'ONG', 'ELF', 'KNC', 
                 'BSV', 'THETA', 'QKC', 'BTT', 'ENJ', 'TFUEL', 'MANA', 'ANKR',
                 'AERGO', 'ATOM', 'MBL', 'WAXP', 'MED', 'MLK', 'STPT', 'ORBS', 'VET', 
                 'CHZ', 'HIVE', 'LINK', 'XTZ', 'BORA', 'JST', 'CRO', 'SXP', 'PLA', 
                 'DOT', 'STRAX', 'AQT', 'GLM', 'SSX', 'META', 'FCT2', 'SAND', 'DOGE', 
                 'PUNDIX', "FLOW", "AXS", "XEC", "SOL", "MATIC", "AAVE", "1INCH"
                 ,'ALGO', 'AVAX', 'T', 'GMT', 'APT', 'SHIB', 'ARB', 'EGLD', 'SUI']
                 
    for i in coin_name:
        google_coin_news = news_crawling(i)

        for news in google_coin_news:
            CrawlingInformation.objects.create(name=news['name'], 
                                                titles=news['title'], 
                                                dates=news['date'], 
                                                urls=news['url'])