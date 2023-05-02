from .common import *

DEBUG = True
ALLOWED_HOSTS = []

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1", # Redis 접속 주소
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


REST_FRAMEWORK = {
    ###'NON_FIELD_ERRORS_KEY': 'error',###  요거 제외밑에부터       
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework_simplejwt.authentication.JWTAuthentication',
    # ),
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