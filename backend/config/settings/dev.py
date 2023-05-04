from .common import *

DEBUG = True
ALLOWED_HOSTS = []


REST_FRAMEWORK = {
    ###'NON_FIELD_ERRORS_KEY': 'error',###  요거 제외밑에부터       
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 500
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}