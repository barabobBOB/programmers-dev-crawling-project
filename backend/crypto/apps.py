from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
    
class CryptoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crypto'

    def ready(self):

        from . import operator
        operator.start()