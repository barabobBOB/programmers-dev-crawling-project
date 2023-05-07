from apscheduler.schedulers.background import BackgroundScheduler
from .views import coin_news, recent_news
from django_apscheduler.jobstores import register_events, DjangoJobStore
from .views import *


def start():
    scheduler=BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)
    @scheduler.scheduled_job('interval', seconds=30, name='news_crawling')
    def auto_check():
        recent_news()
        coin_news()
    scheduler.start()