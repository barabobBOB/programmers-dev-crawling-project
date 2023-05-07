from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from django.utils import timezone
from django.urls import reverse
from django.test import RequestFactory
from . import apis
from .models import CoinSymbol
from django_apscheduler.models import DjangoJob

DjangoJob.objects.all().delete()
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default", replace_existing=True)

@register_job(scheduler, "interval", seconds=10)
def run_daily_tasks():
    factory = RequestFactory()

    # MarketCoinListCreateInitalization view 호출
    request = factory.get(reverse('coin_sync'))
    response = apis.MarketCoinListCreateInitalization(request)
    print('MarketCoinListCreateInitalization', response.status_code)

    # UpdateCoinPrice view 호출
    request = factory.get(reverse('update_price'), {"coin_symbol": "ALL"})
    response = apis.UpdateCoinPrice(request)
    print('UpdateCoinPrice', response.status_code)
    
    # RecentNews view 호출
    request = factory.get(reverse('recent_news_crawling'))
    response = apis.RecentNews(request)
    print('RecentNews', response.status_code)
    
    # CoinNews view 호출
    request = factory.get(reverse('coin_news_crawlling'))
    response = apis.CoinNews(request)
    print('CoinNews', response.status_code)

register_events(scheduler)
scheduler.start()
