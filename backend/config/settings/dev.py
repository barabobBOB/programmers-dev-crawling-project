from .common import *


DEBUG = True

CORS_ORIGIN_WHITELIST = ['http://127.0.0.1:3000'
                         ,'http://localhost:3000']
CORS_ALLOW_CREDENTIALS = True
ALLOWED_HOSTS = []


APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"  # Default
SCHEDULER_DEFAULT = True

REST_FRAMEWORK = {
    ###'NON_FIELD_ERRORS_KEY': 'error',###  요거 제외밑에부터       
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}